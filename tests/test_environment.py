"""Smoke tests: can a student's environment install and run the course stack?"""
import importlib
from pathlib import Path

import nbformat
import pytest

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted(p for p in ROOT.rglob("*.ipynb") if "env" not in p.parts)

PACKAGES = [
    "numpy", "pandas", "scipy", "matplotlib",
    "gymnasium", "renderlab", "torch", "tensorflow", "keras",
]


@pytest.mark.parametrize("name", PACKAGES)
def test_import(name):
    importlib.import_module(name)


def test_cartpole_runs():
    import gymnasium as gym

    env = gym.make("CartPole-v1", render_mode="rgb_array")
    env.reset(seed=0)
    for _ in range(10):
        _, _, terminated, truncated, _ = env.step(env.action_space.sample())
        if terminated or truncated:
            env.reset()
    assert env.render() is not None
    env.close()


def test_renderlab_wraps_cartpole(tmp_path):
    import gymnasium as gym
    import renderlab

    env = renderlab.RenderFrame(gym.make("CartPole-v1", render_mode="rgb_array"), str(tmp_path))
    env.reset(seed=0)
    env.step(env.action_space.sample())
    env.close()


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: str(p.relative_to(ROOT)))
def test_notebook_is_valid(path):
    nbformat.validate(nbformat.read(path, as_version=4))
