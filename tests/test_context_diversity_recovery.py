import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "lab/experiments/context-attractor"
SPEC = importlib.util.spec_from_file_location("diversity_recovery", BENCHMARK / "prepare_diversity_recovery.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(BENCHMARK))
try:
    SPEC.loader.exec_module(MODULE)
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


if __name__ == "__main__":
    unittest.main()
