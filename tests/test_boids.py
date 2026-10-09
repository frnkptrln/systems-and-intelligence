"""Geometry and reproducibility checks for the standalone boids simulation."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

import numpy as np
import pytest


SOURCE = Path(__file__).resolve().parents[1] / "simulation-models/emergent-dynamics/boids-flocking/boids.py"
SPEC = importlib.util.spec_from_file_location("standalone_boids", SOURCE)
boids = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(boids)


def test_isolated_boid_keeps_its_velocity_and_wraps():
    flock = boids.Flock(1, np.random.default_rng(1))
    flock.pos[:] = [99.5, 30.0]
    flock.vel[:] = [1.0, 0.0]
    for _ in range(100):
        flock.step()
        np.testing.assert_array_equal(flock.vel, [[1.0, 0.0]])
    np.testing.assert_allclose(flock.pos, [[99.5, 30.0]], atol=1e-12)


@pytest.mark.parametrize("rule", ["W_SEPARATION", "W_ALIGNMENT", "W_COHESION"])
def test_empty_neighbourhood_does_not_apply_a_braking_force(rule):
    weights = {key: 0.0 for key in ("W_SEPARATION", "W_ALIGNMENT", "W_COHESION")}
    weights[rule] = 1.0
    with patch.multiple(boids, **weights):
        flock = boids.Flock(2, np.random.default_rng(1))
        flock.pos[:] = [[25., 25.], [75., 75.]]
        velocity = np.array([[1., 0.], [0., -1.]])
        flock.vel[:] = velocity
        flock.step()
        np.testing.assert_array_equal(flock.vel, velocity)


def test_cohesion_follows_local_displacements_across_the_seam():
    with patch.multiple(boids, W_SEPARATION=0., W_ALIGNMENT=0., W_COHESION=1.):
        flock = boids.Flock(3, np.random.default_rng(1))
        flock.pos[:] = [[.5, 50.], [99., 50.], [1., 50.]]
        flock.vel[:] = [0., 1.]
        flock.step()
        # Neighbours are 1.5 left and .5 right: the local centre is to the left.
        assert flock.vel[0, 0] < 0


def test_translation_across_world_edges_does_not_change_dynamics():
    first = boids.Flock(12, np.random.default_rng(3))
    second = boids.Flock(12, np.random.default_rng(3))
    first.pos[:] = np.random.default_rng(11).uniform(-6, 6, (12, 2)) % boids.WORLD_SIZE
    shift = np.array([47., 62.])
    second.pos[:] = (first.pos + shift) % boids.WORLD_SIZE
    for _ in range(10):
        first.step(); second.step()
        np.testing.assert_allclose(first.vel, second.vel, atol=1e-11)
        np.testing.assert_allclose(boids.torus_diff(second.pos, first.pos + shift, boids.WORLD_SIZE), 0, atol=1e-11)


def test_coincident_positions_stay_finite_and_speeds_stay_bounded():
    flock = boids.Flock(8, np.random.default_rng(5))
    flock.pos[:] = [0., 0.]
    for _ in range(50):
        flock.step()
        assert np.isfinite(flock.pos).all() and np.isfinite(flock.vel).all()
        assert ((flock.pos >= 0) & (flock.pos < boids.WORLD_SIZE)).all()
        assert np.all(np.linalg.norm(flock.vel, axis=1) <= boids.MAX_SPEED + 1e-12)


def test_report_replays_the_same_final_state_and_samples_endpoints():
    report = boids.run_report(n=9, seed=123, steps=17, sample_every=5)
    assert report == boids.run_report(n=9, seed=123, steps=17, sample_every=5)
    assert [sample["step"] for sample in report["samples"]] == [0, 5, 10, 15, 17]
    flock = boids.Flock(9, np.random.default_rng(123))
    for _ in range(17): flock.step()
    np.testing.assert_array_equal(report["final_state"]["positions"], flock.pos)
    np.testing.assert_array_equal(report["final_state"]["velocities"], flock.vel)
    assert report["numpy_version"] == np.__version__
    assert len(report["source_sha256"]) == 64


def test_zero_steps_and_stationary_observables_are_defined():
    report = boids.run_report(n=1, seed=0, steps=0)
    assert len(report["samples"]) == 1 and report["samples"][0]["step"] == 0
    flock = boids.Flock(1, np.random.default_rng(0)); flock.vel[:] = 0
    assert boids.observables(flock, 0) == {"step": 0, "mean_speed": 0., "maximum_speed": 0., "polarization": 0.}


@pytest.mark.parametrize("kwargs", [{"n": 0}, {"n": True}, {"steps": -1}, {"seed": -1}, {"sample_every": 0}])
def test_invalid_run_sizes_are_rejected(kwargs):
    with pytest.raises(ValueError): boids.run_report(**kwargs)


def test_cli_writes_new_json_and_refuses_to_overwrite(tmp_path):
    output = tmp_path / "run.json"
    command = [sys.executable, str(SOURCE), "--headless", "--boids", "3", "--steps", "4", "--seed", "7", "--output", str(output)]
    subprocess.run(command, check=True, capture_output=True, text=True)
    original = output.read_bytes()
    assert json.loads(original)["steps"] == 4
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode != 0 and "already exists" in result.stderr
    assert output.read_bytes() == original


def test_headless_import_does_not_load_matplotlib():
    code = "import runpy, sys; runpy.run_path(sys.argv[1], run_name='boids_check'); assert 'matplotlib.pyplot' not in sys.modules"
    subprocess.run([sys.executable, "-c", code, str(SOURCE)], check=True)
