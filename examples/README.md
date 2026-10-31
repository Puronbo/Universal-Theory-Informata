# Examples

Run from the repository root after `python -m pip install -e ".[dev]"`.

| Example | Command | Output |
|---|---|---|
| Ternary erosion | `python examples/erosion_demo.py` | before/after states, net-zero check |
| Multi-agent closure | `python examples/multi_agent_demo.py` | per-step closure and states |
| Dark-energy plot | `python examples/plot_delta.py` | writes `delta_plot.png` (git-ignored) |
| Notebook | `jupyter lab demo.ipynb` | end-to-end walkthrough |

For headless runs (CI), set `MPLBACKEND=Agg`.

See `simulate.py` for the full pipeline and `python -m model --help` for the
CLI. Examples are smoke-tested in CI; keep them importable and deterministic.
