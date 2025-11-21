#!/usr/bin/env python3
"""
VERSIÓN CON ERRORES — Debug & Fix (versión pandas, solo 3 errores)

Objetivo del programa (lo que DEBERÍA hacer):
1. Leer un archivo TSV con columnas: gene, expression
2. Leer un threshold desde la línea de comandos
3. Filtrar los genes cuya expresión sea >= threshold
4. Imprimir la lista de genes filtrados

El alumno debe corregirlos sin cambiar el diseño general.
No todos los errores estan identificados en los comentarios.
"""

import pandas as pd


def load_expression_table(path):
    """
    Carga un archivo TSV con columnas 'gene' y 'expression'.

    Args:
        path (str): Ruta al archivo TSV.

    Returns:
        DataFrame: DataFrame con las columnas 'gene' y 'expression'.
    """
    # ERROR: el separador es incorrecto para un TSV (pista: debería ser tab)
    df = pd.read_csv(path, sep=",") 

    # Validación básica de columnas
    if "gene" not in df.columns or "expression" not in df.columns:
        raise ValueError("El archivo debe tener columnas 'gene' y 'expression'.")

    # Convertir expresión a numérico, valores inválidos se convierten en NaN
    df["expression"] = pd.to_numeric(df["expression"], errors="coerce")

    # Eliminar filas con NaN en expression
    df = df.dropna(subset=["expression"])

    return df


def filter_gene(df, threshold):
    """
    Filtra genes con expresión mayor o igual al threshold.

    Args:
        df: DataFrame con columnas 'gene' y 'expression'.
        threshold (float): Umbral mínimo de expresión.

    Returns:
        DataFrame: Subconjunto con genes filtrados.
    """
    # ERROR: condición lógica equivocada (pista: revisar el operador de comparación)
    filtered = df[df["expression"] <= threshold] 

    # Ordenar alfabéticamente por gene
    filtered = filtered.sort_values("gene")

    return filtered


def build_parser():
    """
    Construye el parser de argumentos.

    Returns:
        ArgumentParser: Parser configurado con archivo y threshold.
    """
    parser = argparse.ArgumentParser(
        description="Filtra genes por expresión usando un archivo TSV y pandas."
    )

    parser.add_argument(
        "file",
        help="Archivo TSV con columnas 'gene' y 'expression'."
    )

    # ERROR 3: el tipo de dato no es el adecuado (pista: threshold debe ser numérico)
    parser.add_argument(
        "-t",
        "--threshold",
        type=str,
        default="0",
        help="Umbral mínimo de expresión (ej. 10.5)."
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    df = load_expression_table(args.file)

    # Aquí threshold llega con el tipo definido en build_parser()
    threshold = args.threshold

    filtered = filter_genes(df, threshold)

    if filtered.empty:
        print("No se encontraron genes por encima del threshold.")
        return

    print("Genes filtrados:")
    for gene in filtered["gene"].tolist():
        print(gene)


if __name__ == "__main__":
    main
