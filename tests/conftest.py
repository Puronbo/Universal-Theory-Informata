"""Shared pytest configuration.

Tests must never open a GUI window: many CI runners and headless shells have no
display, and an interactive Tk/Qt backend makes plotting tests fail with
``TclError``. Force the non-interactive Agg backend before matplotlib is
imported anywhere in the suite.
"""

import os

os.environ.setdefault("MPLBACKEND", "Agg")
