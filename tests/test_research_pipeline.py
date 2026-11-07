"""Smoke tests for the public synthetic-data RSM demonstration.

These tests do not validate the original undergraduate experimental study.
"""
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_runs_and_generates_outputs():
    script = ROOT / "rsm_soap_optimization.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr

    outputs = ROOT / "outputs"
    expected = (
        "design_and_results.csv",
        "model_coefficients.csv",
        "model_summary.txt",
        "optimum_conditions.txt",
        "response_surface_and_contour.png",
    )
    for name in expected:
        file = outputs / name
        assert file.is_file(), f"Missing output: {file}"
        assert file.stat().st_size > 0, f"Empty output: {file}"


def test_source_marks_data_as_representative():
    source = (ROOT / "rsm_soap_optimization.py").read_text(encoding="utf-8")
    assert "REPRESENTATIVE" in source
    assert "not a" in source.lower() and "original" in source.lower()
