"""Tests for model.lattice."""

import pytest

from model import (
    WIDTH,
    PoleString,
    all_strings,
    atoms,
    bottom,
    canonical,
    coatoms,
    complement,
    from_bits,
    from_poles,
    join,
    leq,
    meet,
    orbit_count,
    same_orbit,
    top,
)
from model.duality import DUAL_PAIRS

LEFT_POLES = (
    "UV",
    "exterior",
    "compression",
    "photon",
    "entropy",
    "becoming",
    "discrete",
    "reprocessed",
)
RIGHT_POLES = tuple(pair.right for pair in DUAL_PAIRS)


def test_width_and_size():
    assert WIDTH == len(DUAL_PAIRS) == 8
    assert len(all_strings()) == 2**WIDTH == 256
    assert orbit_count() == 2 ** (WIDTH - 1) == 128


@pytest.mark.parametrize("bits", ["00000000", "10101010", "11111111", "01010101"])
def test_bits_round_trip(bits):
    assert from_bits(bits).to_bits() == bits
    assert str(from_bits(bits)) == bits


def test_poles_round_trip():
    assert from_poles(LEFT_POLES).to_bits() == "00000000"
    assert from_poles(RIGHT_POLES).to_bits() == "11111111"
    for value in all_strings()[::37]:
        assert from_poles(value.poles) == value


def test_bits_reject_bad_input():
    with pytest.raises(ValueError):
        from_bits("0101")
    with pytest.raises(ValueError):
        from_bits("0101010x")


def test_poles_reject_bad_input():
    with pytest.raises(ValueError):
        from_poles(("UV",))
    with pytest.raises(ValueError):
        from_poles(("visible",) + RIGHT_POLES[1:])
    with pytest.raises(ValueError):
        from_poles(("interior",) + RIGHT_POLES[1:])


def test_pole_string_validates_bits():
    with pytest.raises(ValueError):
        PoleString((True, False))
    with pytest.raises(ValueError):
        PoleString(tuple(1 for _ in range(WIDTH)))  # type: ignore[arg-type]


def test_dual_is_an_involution_without_fixed_points():
    for value in all_strings():
        assert value.dual.dual == value
        assert value.dual != value
        assert value.rank + value.dual.rank == WIDTH
        assert complement(value) == value.dual


def test_join_meet_and_rank():
    a = from_bits("11000000")
    b = from_bits("10101010")
    assert join(a, b).to_bits() == "11101010"
    assert meet(a, b).to_bits() == "10000000"
    assert join(a, b).rank + meet(a, b).rank == a.rank + b.rank


def test_order_is_a_partial_order():
    a = from_bits("10000000")
    b = from_bits("11000000")
    c = from_bits("11100000")
    assert leq(a, a)
    assert leq(a, b) and leq(b, c)
    assert leq(a, c)
    assert not leq(b, a)
    assert leq(a, join(a, b))
    assert leq(meet(a, b), a)


@pytest.mark.parametrize(
    ("left", "right"),
    [("00000000", "11111111"), ("10101010", "01010101"), ("11000000", "00110000")],
)
def test_complement_laws(left, right):
    a, b = from_bits(left), from_bits(right)
    assert join(a, complement(a)) == top()
    assert meet(a, complement(a)) == bottom()
    assert complement(join(a, b)) == meet(complement(a), complement(b))
    assert complement(meet(a, b)) == join(complement(a), complement(b))


@pytest.mark.parametrize(
    ("left", "middle", "right"),
    [
        ("00000000", "11111111", "10101010"),
        ("11000000", "10101010", "00110011"),
        ("10000001", "01000010", "00100100"),
    ],
)
def test_boolean_lattice_laws(left, middle, right):
    a, b, c = from_bits(left), from_bits(middle), from_bits(right)
    assert join(a, b) == join(b, a)
    assert meet(a, b) == meet(b, a)
    assert join(join(a, b), c) == join(a, join(b, c))
    assert meet(meet(a, b), c) == meet(a, meet(b, c))
    assert join(a, a) == a
    assert meet(a, a) == a
    assert join(a, meet(a, b)) == a
    assert meet(a, join(a, b)) == a
    assert join(a, meet(b, c)) == meet(join(a, b), join(a, c))
    assert meet(a, join(b, c)) == join(meet(a, b), meet(a, c))


def test_top_bottom_and_atoms():
    assert bottom().to_bits() == "0" * WIDTH
    assert top().to_bits() == "1" * WIDTH
    for value in all_strings():
        assert leq(bottom(), value)
        assert leq(value, top())

    atom_list = atoms()
    assert len(atom_list) == WIDTH
    assert all(atom.rank == 1 for atom in atom_list)
    assert len(set(atom_list)) == WIDTH
    assert join_all(atom_list) == top()

    coatom_list = coatoms()
    assert all(coatom.rank == WIDTH - 1 for coatom in coatom_list)
    assert meet_all(coatom_list) == bottom()


def join_all(values):
    result = bottom()
    for value in values:
        result = join(result, value)
    return result


def meet_all(values):
    result = top()
    for value in values:
        result = meet(result, value)
    return result


def test_canonical_folds_complement_orbits():
    representatives = set()
    for value in all_strings():
        chosen = canonical(value)
        assert chosen in (value, value.dual)
        assert canonical(value.dual) == chosen
        assert same_orbit(value, value.dual)
        assert same_orbit(value, chosen)
        representatives.add(chosen)
    assert len(representatives) == orbit_count()


def test_all_strings_are_unique_and_ordered():
    values = all_strings()
    assert len(set(values)) == 256
    assert values[0] == bottom()
    assert values[-1] == top()
