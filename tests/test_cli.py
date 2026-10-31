"""CLI entry-point tests."""

import runpy
import sys

from cli import main


def test_python_m_model_timeline(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["model", "timeline"])
    runpy.run_module("model", run_name="__main__")
    assert "milestone_date" in capsys.readouterr().out


def test_validate_subcommand_runs_from_any_cwd(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["model", "validate"])
    main()
