import pytest
from pathlib import Path
import sys

# Ensure src is importable
root = Path(__file__).resolve().parents[1]
src_path = root / "src"
sys.path.insert(0, str(src_path))

from k_mers import validate_sequence, count_kmers


def test_validate_sequence_normalizes_and_accepts_lowercase_spaces():
    s = " a t c g "
    assert validate_sequence(s) == "ATCG"


def test_validate_sequence_rejects_invalid_chars():
    with pytest.raises(ValueError):
        validate_sequence("ATXG")


def test_validate_sequence_empty_and_none():
    with pytest.raises(ValueError):
        validate_sequence("")
    with pytest.raises(ValueError):
        validate_sequence(None)


def test_count_kmers_basic_and_overlapping():
    seq = validate_sequence("ATCGATCGA")
    counts = count_kmers(seq, 3)
    assert counts["ATC"] == 2
    assert counts["TCG"] == 2
    assert counts["CGA"] == 2
    assert counts["GAT"] == 1


def test_count_kmers_k_equals_len_sequence():
    seq = validate_sequence("ATCG")
    counts = count_kmers(seq, 4)
    assert counts == {"ATCG": 1}


def test_count_kmers_k_one_counts():
    seq = validate_sequence("ATCGAT")
    counts = count_kmers(seq, 1)
    assert counts == {"A": 2, "T": 2, "C": 1, "G": 1}


def test_count_kmers_all_identical_bases():
    seq = validate_sequence("AAAA")
    counts = count_kmers(seq, 2)
    assert counts == {"AA": 3}


def test_count_kmers_k_invalid_values():
    seq = validate_sequence("ATCG")
    with pytest.raises(ValueError):
        count_kmers(seq, 0)
    with pytest.raises(ValueError):
        count_kmers(seq, -1)
    with pytest.raises(ValueError):
        count_kmers(seq, 5)
