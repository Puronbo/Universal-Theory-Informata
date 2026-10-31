"""The meta-audit itself is part of the contract; keep it green."""

from validate_claims import check_cross_refs, check_engine_refs, check_overclaims


def test_docs_have_no_forbidden_overclaims():
    assert check_overclaims() == []


def test_all_model_references_resolve():
    assert check_engine_refs() == []


def test_every_axiom_is_linked_in_connections():
    assert check_cross_refs() == []
