"""CLI entry-point tests."""

import json
import math
import runpy
import sys

import pytest

from cli import main
from model import DUAL_PAIRS


def _run(monkeypatch, capsys, argv: list[str]):
    monkeypatch.setattr(sys, "argv", ["model", *argv])
    main()
    return capsys.readouterr()


def test_python_m_model_timeline(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["model", "timeline"])
    runpy.run_module("model", run_name="__main__")
    assert "milestone_date" in capsys.readouterr().out


def test_validate_subcommand_runs_from_any_cwd(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["model", "validate"])
    main()


def test_duality_lists_all_pairs(monkeypatch, capsys):
    payload = json.loads(_run(monkeypatch, capsys, ["duality"]).out)
    assert payload["count"] == len(DUAL_PAIRS) == 8
    assert payload["pairs"][0] == {"name": "scale", "left": "UV", "right": "IR"}
    assert payload["pairs"][-1] == {
        "name": "information",
        "left": "reprocessed",
        "right": "erased",
    }


def test_duality_flips_a_pole(monkeypatch, capsys):
    payload = json.loads(_run(monkeypatch, capsys, ["duality", "--pole", "UV"]).out)
    assert payload == {"pole": "UV", "dual": "IR"}


def test_duality_reports_a_pair(monkeypatch, capsys):
    payload = json.loads(_run(monkeypatch, capsys, ["duality", "--pair", "time"]).out)
    assert payload == {"name": "time", "left": "becoming", "right": "block"}


def test_duality_rejects_unknown_pole(monkeypatch, capsys):
    with pytest.raises(SystemExit) as excinfo:
        _run(monkeypatch, capsys, ["duality", "--pole", "visible"])
    assert excinfo.value.code == 2
    assert "unknown pole" in capsys.readouterr().err


def test_duality_rejects_unknown_pair(monkeypatch, capsys):
    with pytest.raises(SystemExit) as excinfo:
        _run(monkeypatch, capsys, ["duality", "--pair", "unknown"])
    assert excinfo.value.code == 2
    assert "unknown dual pair" in capsys.readouterr().err


def test_antithesis_reports_three_regimes(monkeypatch, capsys):
    payload = json.loads(_run(monkeypatch, capsys, ["antithesis"]).out)
    assert payload["initial"] == 2.0
    assert payload["steps"] == 3
    assert payload["involution"] == [2.0, 0.5, 2.0, 0.5]
    assert payload["contraction"] == [2.0, 1.0, 0.5, 0.25]
    assert payload["translation"] == [2.0, 3.0, 4.0, 5.0]
    assert payload["periods"] == {
        "involution": 2,
        "contraction": None,
        "translation": None,
    }
    assert payload["entropy"] == pytest.approx(-math.log(2.0))
    assert payload["information_loss"] == pytest.approx(3.0 * math.log(2.0))
    assert payload["lyapunov_exponent"] == pytest.approx(math.log(0.5))


def test_antithesis_honours_options(monkeypatch, capsys):
    payload = json.loads(
        _run(
            monkeypatch,
            capsys,
            ["antithesis", "--x", "4", "--steps", "2", "--rate", "0.25", "--shift", "-1"],
        ).out
    )
    assert payload["involution"] == [4.0, 0.25, 4.0]
    assert payload["contraction"] == [4.0, 1.0, 0.25]
    assert payload["translation"] == [4.0, 3.0, 2.0]
    assert payload["lyapunov_exponent"] == pytest.approx(math.log(0.25))


def test_antithesis_omits_nilpotent_by_default(monkeypatch, capsys):
    payload = json.loads(_run(monkeypatch, capsys, ["antithesis"]).out)
    assert "nilpotent" not in payload


def test_antithesis_reports_nilpotent_collapse(monkeypatch, capsys):
    payload = json.loads(
        _run(
            monkeypatch,
            capsys,
            ["antithesis", "--x", "3", "--steps", "3", "--nilpotent", "--y", "4"],
        ).out
    )
    assert payload["nilpotent"] == {
        "seed": [3.0, 4.0],
        "orbit": [[3.0, 4.0], [0.0, 3.0], [0.0, 0.0], [0.0, 0.0]],
        "n_squared": [0.0, 0.0],
    }


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        (["--x", "0"], "x must be finite"),
        (["--x", "-1"], "x must be finite"),
        (["--steps", "-1"], "steps must be >= 0"),
        (["--rate", "1"], "rate must be finite"),
        (["--rate", "0"], "rate must be finite"),
        (["--shift", "0"], "shift must be nonzero"),
        (["--nilpotent", "--y", "nan"], "x and y must be finite"),
    ],
)
def test_antithesis_rejects_invalid_input(monkeypatch, capsys, argv, message):
    with pytest.raises(SystemExit) as excinfo:
        _run(monkeypatch, capsys, ["antithesis", *argv])
    assert excinfo.value.code == 2
    assert message in capsys.readouterr().err
