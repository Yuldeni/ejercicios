import os
import pandas as pd
import io
import sys
import pytest
from pathlib import Path

# Ensure src is importable
root = Path(__file__).resolve().parents[1]
src_path = root / "src"
sys.path.insert(0, str(src_path))

from gene_expression import load_expression_table, filter_gene, main


def write_tsv(tmp_path, content: str):
    p = tmp_path / "test.tsv"
    p.write_text(content)
    return str(p)


def test_load_expression_table_parses_and_drops_nan(tmp_path):
    content = "gene\texpression\nG1\t10\nG2\t5\nBAD\tnotnum\n"
    path = write_tsv(tmp_path, content)
    df = load_expression_table(path)
    assert "gene" in df.columns
    assert "expression" in df.columns
    assert df.shape[0] == 2  # G1 and G2 only
    assert set(df["gene"]) == {"G1", "G2"}


def test_filter_gene_inclusive_threshold():
    df = pd.DataFrame({"gene": ["A", "B", "C"], "expression": [1.0, 2.0, 3.0]})
    res = filter_gene(df, 2.0)
    assert set(res["gene"]) == {"B", "C"}


def test_main_cli_prints_genes(tmp_path, monkeypatch, capsys):
    # Create a temp file and run main() by adjusting sys.argv
    content = "gene\texpression\nZ\t1\nA\t10\nB\t5\n"
    path = write_tsv(tmp_path, content)
    monkeypatch.setattr(sys, "argv", ["prog", path, "-t", "5"])  # threshold 5
    main()
    captured = capsys.readouterr()
    # Should print header and genes A and B sorted alphabetically
    assert "Genes filtrados:" in captured.out
    # Lines with gene names
    lines = [ln.strip() for ln in captured.out.splitlines() if ln.strip() and not ln.startswith("Genes filtrados")]
    assert lines == ["A", "B"]


def test_cli_threshold_type_error(tmp_path, monkeypatch):
    content = "gene\texpression\nG1\t1\n"
    path = write_tsv(tmp_path, content)
    monkeypatch.setattr(sys, "argv", ["prog", path, "-t", "not_a_number"])  # invalid threshold
    with pytest.raises(SystemExit):
        main()
