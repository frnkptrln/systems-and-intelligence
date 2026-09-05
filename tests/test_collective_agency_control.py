"""Pin the analytic counterexample, including the observation/intervention split."""

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "lab/experiments/collective-agency-control"
SPEC = importlib.util.spec_from_file_location("collective_agency_control", CONTROL / "run_control.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_exact_control_separates_information_from_coupling_and_repair():
    result = MODULE.run()
    assert result == json.loads((CONTROL / "result.json").read_text())
    assert result["initial_entropy_bits"] == 2
    assert result["states_enumerated_per_causal_graph"] == 64
    expected = {
        "uncoupled_toggle": (0, 1, 0, 16, 0),
        "local_repair": (12, 3, 24, 24, 0),
        "cross_group_repair": (18, 6, 24, 24, 1),
    }
    for name, (edges, component, repair, representative, local_entropy) in expected.items():
        model = result["models"][name]
        assert model["interventions"] == 24
        assert model["causal_graph"]["off_diagonal_edges"] == edges
        assert model["causal_graph"]["largest_strongly_connected_component"] == component
        assert model["state_restored_after_error"] == repair
        assert model["mean_local_next_bit_conditional_entropy_bits"] == local_entropy
        for reading in model["readings"].values():
            assert reading["next_macro_entropy_bits"] == 1
            assert reading["triplet_information_bits"] == [0, 0]
            assert reading["joint_information_bits"] == 1
            assert reading["macro_temporal_information_bits"] == 1
        assert model["readings"]["representative_parity"]["macro_preserved_after_error"] == representative
        assert model["readings"]["majority_parity"]["macro_preserved_after_error"] == 24


if __name__ == "__main__":
    test_exact_control_separates_information_from_coupling_and_repair()
    print("Exact control headline and committed result: passed")
