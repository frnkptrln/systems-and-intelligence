import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "lab" / "benchmarks" / "collective-agency"
SPEC = importlib.util.spec_from_file_location(
    "collective_agency_freeze_contract", BENCHMARK / "freeze_contract.py"
)
assert SPEC is not None and SPEC.loader is not None
CONTRACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTRACT)


class CollectiveAgencyFreezeTests(unittest.TestCase):
    def test_documented_candidate_is_valid_but_fully_blocked(self):
        candidate = CONTRACT.load_candidate(BENCHMARK / "freeze-candidate.json")
        self.assertEqual(CONTRACT.candidate_errors(candidate), [])
        blockers = CONTRACT.execution_blockers(candidate)
        self.assertIn("status is not frozen_implementation_authorized", blockers)
        self.assertIn("implementation is not authorized", blockers)
        self.assertIn("execution is not authorized", blockers)
        self.assertIn("maintainer questions remain unresolved", blockers)

    def test_reviewed_shape_can_clear_without_changing_the_scientific_defaults(self):
        candidate = copy.deepcopy(CONTRACT.load_candidate(BENCHMARK / "freeze-candidate.json"))
        candidate["status"] = "frozen_implementation_authorized"
        candidate["implementation_authorized"] = True
        candidate["execution_authorized"] = True
        candidate["open_questions"] = []
        candidate["intervention"]["outcome_horizon"] = 10
        candidate["viability"]["recovery_epsilon"] = 0.05
        self.assertEqual(CONTRACT.execution_blockers(candidate), [])

    def test_default_drift_is_detected(self):
        candidate = CONTRACT.load_candidate(BENCHMARK / "freeze-candidate.json")
        candidate["synergy"]["option"] = "4B"
        self.assertIn(
            "synergy.option changed from the documented default",
            CONTRACT.candidate_errors(candidate),
        )


if __name__ == "__main__":
    unittest.main()
