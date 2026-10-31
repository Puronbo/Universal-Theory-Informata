"""Tests for model.search."""

from model import search_text


def test_search_text():
    res = search_text(".", "Rolling-Fold", include="*.md")
    assert len(res) > 0
    assert any("CONNECTIONS" in r[0] or "AXIOMS" in r[0] for r in res)


def test_search_text_regex():
    res = search_text(".", "A\\d+\\.\\d+", include="*.md", regex=True)
    assert len(res) > 0


def test_search_text_nonexistent():
    res = search_text(".", "nonexistentpattern12345", include="*.md")
    assert res == []
