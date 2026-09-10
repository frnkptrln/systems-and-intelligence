import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "lab/experiments/context-attractor"
SPEC = importlib.util.spec_from_file_location("diversity_recovery", BENCHMARK / "prepare_diversity_recovery.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(BENCHMARK))
try:
    SPEC.loader.exec_module(MODULE)
    import complete_diversity_recovery as COMPLETION
    import aggregate_diversity_recovery as AGGREGATION
finally:
    sys.path.pop(0)


class DiversityRecoveryTests(unittest.TestCase):
    def test_packet_has_only_allowed_bytes_and_is_deterministic(self):
        for evaluator in ("E3", "E4"):
            first = MODULE.packet_bytes(evaluator)
            self.assertEqual(first, MODULE.packet_bytes(evaluator))
            with zipfile.ZipFile(io.BytesIO(first)) as packet:
                self.assertEqual(set(packet.namelist()), {
                    "items.jsonl", "instructions.md", "clusters.schema.json", "manifest.json",
                })
                self.assertEqual(packet.read("items.jsonl"), MODULE.ITEMS.read_bytes())
                manifest = json.loads(packet.read("manifest.json"))
                self.assertEqual(manifest["evaluator_id"], evaluator)
                for name, digest in manifest["files"].items():
                    self.assertEqual(MODULE.sha256(packet.read(name)), digest)

    def test_original_evaluators_and_tampered_items_are_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.packet_bytes("E1")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "items.jsonl"
            path.write_bytes(MODULE.ITEMS.read_bytes() + b"\n")
            with self.assertRaises(ValueError):
                MODULE.packet_bytes("E3", path)

    def test_structural_pass_does_not_claim_semantic_qc_or_unblinding(self):
        _, ids = MODULE.load_items(MODULE.ITEMS)
        ordered = sorted(ids)
        payload = {"families": [{"name": f"Test category {i}", "item_ids": ordered[i::8]}
                                for i in range(8)]}
        # Mechanical unit-test partition, never used as a scientific evaluation.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clusters.json"
            path.write_text(json.dumps(payload))
            report = MODULE.validate_partition(path)
            self.assertFalse(report["unblinding_ready"])
            self.assertEqual(report["semantic_qc"], "pending_blind_review")
            payload["families"][1]["name"] = payload["families"][0]["name"]
            path.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                MODULE.validate_partition(path)
            payload["families"][1]["name"] = "Distinct"
            payload["families"][1]["item_ids"].append(ordered[0])
            path.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                MODULE.validate_partition(path)

    def test_export_never_overwrites_an_existing_packet_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "new"
            MODULE.prepare(output)
            before = (output / "E3.zip").read_bytes()
            with self.assertRaises(FileExistsError):
                MODULE.prepare(output)
            self.assertEqual((output / "E3.zip").read_bytes(), before)


class ReceivedDiversityTests(unittest.TestCase):
    def test_recovered_partitions_match_published_intake_hashes(self):
        provenance = json.loads((COMPLETION.RECEIVED / "provenance.json").read_bytes())
        for evaluator, count in (("E3", 16), ("E4", 15)):
            path = COMPLETION.RECEIVED / evaluator / "clusters.json"
            report = MODULE.validate_partition(path)
            self.assertEqual(report["partition_sha256"], COMPLETION.PARTITION_HASHES[evaluator])
            self.assertEqual(len(json.loads(path.read_bytes())["families"]), count)
            source_id = provenance["submissions"][evaluator]["source_url"].split("issuecomment-")[1]
            comment = (COMPLETION.RECEIVED / "source-comments" / f"{source_id}.md").read_text()
            recorded = json.loads(comment.split("```json\n")[1].split("\n```", 1)[0])
            self.assertEqual(json.loads(path.read_bytes()), recorded)
        for name, digest in provenance["source_comment_sha256"].items():
            self.assertEqual(MODULE.sha256((COMPLETION.RECEIVED / "source-comments" / name).read_bytes()), digest)

    def test_qc_packet_contains_one_unchanged_partition_and_no_context(self):
        for evaluator in ("E3", "E4"):
            raw = COMPLETION.qc_packet_bytes(evaluator)
            self.assertEqual(raw, COMPLETION.qc_packet_bytes(evaluator))
            with zipfile.ZipFile(io.BytesIO(raw)) as packet:
                self.assertEqual(set(packet.namelist()), {
                    "items.jsonl", "clusters.json", "instructions.md", "manifest.json",
                })
                self.assertEqual(packet.read("items.jsonl"), MODULE.ITEMS.read_bytes())
                self.assertEqual(packet.read("clusters.json"),
                                 (COMPLETION.RECEIVED / evaluator / "clusters.json").read_bytes())
                manifest = json.loads(packet.read("manifest.json"))
                self.assertEqual(set(manifest), {"files"})
                for name, digest in manifest["files"].items():
                    self.assertEqual(MODULE.sha256(packet.read(name)), digest)

    def test_qc_export_rejects_changed_submission_before_creating_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for evaluator in ("E3", "E4"):
                (root / evaluator).mkdir()
                raw = (COMPLETION.RECEIVED / evaluator / "clusters.json").read_bytes()
                (root / evaluator / "clusters.json").write_bytes(raw + b"\n")
            with self.assertRaisesRegex(ValueError, "recorded intake hash"):
                COMPLETION.prepare_qc(root / "output", root)
            self.assertFalse((root / "output").exists())

    def make_qc_fixture(self, directory, decision="pass"):
        # Synthetic review receipt for gate tests; never scientific QC evidence.
        receipt = {"frozen_at_utc": "2026-09-05T12:00:01Z", "reviews": {}}
        for evaluator in ("E3", "E4"):
            folder = directory / evaluator
            folder.mkdir()
            raw = json.dumps({"decision": decision, "rationale": "Mechanical test fixture only",
                              "observations": []}).encode()
            (folder / "review.json").write_bytes(raw)
            receipt["reviews"][evaluator] = {
                "reviewer_id": f"synthetic-{evaluator}", "model": "no model run",
                "fresh_context": True, "completed_at_utc": "2026-09-05T12:00:00Z",
                "input_packet_sha256": MODULE.sha256(COMPLETION.qc_packet_bytes(evaluator)),
                "output_sha256": MODULE.sha256(raw),
            }
        (directory / "receipt.json").write_text(json.dumps(receipt))
        return receipt

    def test_failed_qc_never_opens_the_condition_key_or_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_qc_fixture(root, decision="fail")
            with mock.patch.object(AGGREGATION, "condition_metrics", side_effect=AssertionError("unblinded")):
                result = AGGREGATION.analyze(root, run=root / "must-not-be-opened")
            self.assertEqual(result["status"], "blind_semantic_qc_failed")
            self.assertFalse(result["condition_key_accessed"])
            self.assertFalse(result["P3_P4_evaluable"])

    def test_qc_gate_rejects_tampering_and_shared_contexts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self.make_qc_fixture(root)
            self.assertTrue(AGGREGATION.review_gate(root)["passed"])
            path = root / "E3/review.json"
            raw = path.read_bytes()
            path.write_bytes(raw + b"\n")
            with self.assertRaisesRegex(ValueError, "changed after"):
                AGGREGATION.review_gate(root)
            path.write_bytes(raw)
            receipt["reviews"]["E4"]["reviewer_id"] = "synthetic-E3"
            (root / "receipt.json").write_text(json.dumps(receipt))
            with self.assertRaisesRegex(ValueError, "separate reviewer contexts"):
                AGGREGATION.review_gate(root)

    def test_recorded_failed_qc_disposition_reproduces_without_changing_evidence(self):
        expected = json.loads((COMPLETION.RECEIVED / "recovery-result.json").read_bytes())
        self.assertEqual(AGGREGATION.analyze(COMPLETION.RECEIVED / "blind-qc"), expected)
        evidence = json.loads((COMPLETION.RECEIVED / "preserved-evidence.json").read_bytes())
        self.assertEqual(len(evidence["files_sha256"]), 46)
        for name, digest in evidence["files_sha256"].items():
            self.assertEqual(MODULE.sha256((AGGREGATION.RUN / name).read_bytes()), digest)

    def test_zero_versus_positive_sign_disagreement_is_not_averaged(self):
        # Entirely synthetic IDs/conditions; the real key is not consulted.
        b, r = [f"B{i}" for i in range(40)], [f"R{i}" for i in range(40)]
        keys = {item: {"condition": condition} for condition, ids in (("B", b), ("R", r)) for item in ids}
        equal = {"families": [{"name": str(i), "item_ids": b[i::8] + r[i::8]} for i in range(8)]}
        positive = {"families": [{"name": "0", "item_ids": r[:5]}] + [
            {"name": str(i + 1), "item_ids": b[i::7] + r[5:][i::7]} for i in range(7)]}
        result = AGGREGATION.diversity_counts(keys, {"E3": equal, "E4": positive}, 0.1, 0.0)
        self.assertEqual(result["per_evaluator"]["E3"]["difference_R_minus_B"], 0)
        self.assertEqual(result["per_evaluator"]["E4"]["difference_R_minus_B"], 1)
        self.assertFalse(result["P3_P4_evaluable"])
        self.assertTrue(all(value is None for value in result["directional_checks"].values()))
        agreeing = AGGREGATION.diversity_counts(keys, {"E3": positive, "E4": positive}, 0.1, 0.0)
        self.assertTrue(agreeing["P3_P4_evaluable"])
        self.assertTrue(agreeing["directional_checks"]["P4_R_bridge_pattern"])


if __name__ == "__main__":
    unittest.main()
