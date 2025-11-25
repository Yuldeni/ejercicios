import sys
from pathlib import Path
import tempfile
import os
import io
import pytest

# Ensure src is importable
root = Path(__file__).resolve().parents[1]
src_path = root / "src"
sys.path.insert(0, str(src_path))

import base_freq as bf


def test_parse_args_simple():
    ns = bf.parse_args(["mi_fasta.fasta"])
    assert ns.fasta == "mi_fasta.fasta"


def test_read_file_success_and_not_found(tmp_path):
    p = tmp_path / "test.fasta"
    p.write_text(">header\nATGC\n")
    content = bf.read_file(str(p))
    assert ">header" in content

    with pytest.raises(FileNotFoundError):
        bf.read_file(str(p.parent / "nofile.fasta"))


def test_validate_is_fasta_and_invalid():
    valid = ">h\nATGC\n"
    # Should not raise
    bf.validate_is_fasta(valid)
    # Missing '>'
    with pytest.raises(ValueError) as e:
        bf.validate_is_fasta("ATGC")
    assert "Error: El archivo no parece estar en formato FASTA." in str(e.value)


def test_parse_single_fasta_and_empty_sequence():
    content = ">h\nATG\n"
    header, seq = bf.parse_single_fasta(content)
    assert header == "h"
    assert seq == "ATG"

    # Empty sequence should raise ValueError
    with pytest.raises(ValueError) as e:
        bf.parse_single_fasta(">h\n\n")
    assert "Error: la secuencia está vacía." in str(e.value)


def test_clean_sequence_and_invalids():
    seq = "aTgNxyz \n"
    cleaned, invalids = bf.clean_sequence(seq)
    assert cleaned == "ATG"
    # invalids should be uppercased and preserve order
    assert invalids == ["N", "X", "Y", "Z", " ", "\n"]


def test_compute_base_counts_and_print_results(capsys):
    seq = "AATG"
    counts = bf.compute_base_counts(seq)
    assert counts["A"] == 2
    assert counts["total"] == 4

    # Test print_results output formatting
    bf.print_results("h", counts)
    captured = capsys.readouterr()
    assert "Encabezado:" in captured.out
    assert "Longitud secuencia válida: 4" in captured.out
    assert "A: 2 (50.0%)" in captured.out


def test_main_success_and_invalid_chars(tmp_path, capsys):
    p = tmp_path / "good.fasta"
    p.write_text(">seq1\nATGCatgNxyz\n")
    rc = bf.main([str(p)])
    assert rc == 0
    out = capsys.readouterr().out
    # Should print advices for invalid characters in the order given
    assert "Aviso: caracter inválido 'N' ignorado" in out
    assert "Encabezado: seq1" in out
    assert "Longitud secuencia válida:" in out


def test_main_file_not_found(tmp_path, capsys):
    p = tmp_path / "nofile.fasta"
    rc = bf.main([str(p)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "Error: el archivo no existe:" in out


def test_main_invalid_fasta(tmp_path, capsys):
    p = tmp_path / "bad.fasta"
    p.write_text("NO FASTA HERE\n")
    rc = bf.main([str(p)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "Error: El archivo no parece estar en formato FASTA." in out


def test_main_no_valid_bases(tmp_path, capsys):
    p = tmp_path / "novalids.fasta"
    p.write_text(">s\nNNNNxxx\n")
    rc = bf.main([str(p)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "Error: la secuencia no contiene bases válidas (A,T,G,C)." in out


def test_large_sequence_counts():
    # Boundary: handle large sequences efficiently
    big = "A" * 100000 + "T" * 100000
    counts = bf.compute_base_counts(big)
    assert counts["A"] == 100000
    assert counts["T"] == 100000
    assert counts["total"] == 200000


def test_multiple_fasta_entries_parse_single():
    content = ">h1\nATG\n>h2\nCCCC\n"
    header, seq = bf.parse_single_fasta(content)
    # Should only parse first header and seq
    assert header == "h1"
    assert seq == "ATG"
