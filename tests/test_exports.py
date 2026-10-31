"""Invariants that keep the public package coherent."""

import re

import model


def test_public_exports_are_unique_and_resolve():
    assert len(model.__all__) == len(set(model.__all__))
    missing = [name for name in model.__all__ if not hasattr(model, name)]
    assert missing == []


def test_version_is_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", model.__version__)
