#!/usr/bin/env python3
"""k-mers: contador de k-mers simple en línea de comandos.

Este script lee una secuencia de ADN desde la línea de comandos (argumento
posicional), valida que solo contenga las bases A, T, C y G, y cuenta todos los
k-mers contiguos de longitud `k` proporcionada por el usuario.

Ejemplo de uso:
    python k-mers.py ATCGATCGA -k 3

Formato de salida:
    kmer<TAB>conteo

La salida se ordena por conteo (descendente) y luego por k-mer de forma
lexicográfica.
"""
import argparse
from typing import Dict


def validate_sequence(seq: str) -> str:
    """Validar y normalizar una secuencia de ADN.

    - Convertir a mayúsculas
    - Eliminar caracteres de espacio en blanco
    - Levantar ValueError si hay caracteres distintos de A/T/C/G

    Args:
        seq: secuencia cruda proporcionada por el usuario

    Returns:
        Secuencia normalizada en mayúsculas con solo A/T/C/G.

    Raises:
        ValueError: si la secuencia contiene caracteres inválidos o está vacía.
    """
    # Desecha secuencia si está vacía
    if seq is None:
        raise ValueError("La secuencia no puede ser nula")
    
    # Elimina espacios y convierte a mayúsculas
    normalized = "".join(seq.split()).upper()
    if len(normalized) == 0:
        raise ValueError("La secuencia está vacía después de eliminar espacios")
    
    # Verifica caracteres inválidos
    allowed = set("ATCG")
    invalid = set(normalized) - allowed
    if invalid:
        raise ValueError(
            f"La secuencia contiene caracteres inválidos: {','.join(sorted(invalid))}. "
            "Solo se permiten A, T, C, G."
        )
    return normalized


def count_kmers(seq: str, k: int) -> Dict[str, int]:
    """Contar k-mers de longitud k en la secuencia.

    Args:
        seq: Secuencia de ADN validada que contiene solo A/T/C/G.
        k: Tamaño del k-mer (entero positivo).

    Returns:
        Un diccionario que mapea k-mers a sus conteos.

    Raises:
        ValueError: si k no es un entero positivo o es mayor que len(seq).
    """
    # Si k no es válido, levantar error
    if not isinstance(k, int) or k <= 0:
        raise ValueError("k debe ser un entero positivo")
    if k > len(seq):
        raise ValueError("k no puede ser mayor que la longitud de la secuencia")
    
    # Guarda cuenta de k-mers str para k-mero e int para la cuenta
    counts: Dict[str, int] = {}
    # Para cada posición posible en la secuencia
    for i in range(len(seq) - k + 1):
        # Extrae el k-mer y actualiza su conteo
        kmer = seq[i : i + k]
        counts[kmer] = counts.get(kmer, 0) + 1
    return counts


def build_parser() -> argparse.ArgumentParser:
    """Construir y retornar el parseador de argumentos."""
    parser = argparse.ArgumentParser(
        description="Contar k-mers en una secuencia de ADN (solo A/T/C/G permitidos)."
    )
    parser.add_argument(
        "sequence",
        help="Secuencia de ADN como argumento posicional (p.ej., ATCGTT)",
    )
    parser.add_argument(
        "-k",
        "--kmer_size",
        type=int,
        default=3,
        help="Tamaño del k-mer (entero positivo). Por defecto: 3",
    )
    parser.add_argument(
        "--sort",
        choices=["count", "kmer"],
        default="count",
        help="Ordenar por 'count' (descendente) y luego por kmer o por 'kmer' (lexicográfico).",
    )
    return parser


def main() -> None:
    """Punto de entrada CLI: parsear argumentos, validar secuencia, contar k-mers e imprimir resultados."""
    parser = build_parser()
    args = parser.parse_args()

    # Validar secuencia
    try:
        seq = validate_sequence(args.sequence)
    except ValueError as exc:
        parser.error(str(exc))

    # Contar k-mers
    try:
        counts = count_kmers(seq, args.kmer_size)
    except ValueError as exc:
        parser.error(str(exc))

    # Ordenar resultados: por conteo (desc) y luego por kmer lexicográficamente, o solo por kmer
    if args.sort == "count":
        sorted_items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    else:
        sorted_items = sorted(counts.items(), key=lambda kv: kv[0])

    # Imprimir resultados
    for kmer, cnt in sorted_items:
        print(f"{kmer}\t{cnt}")


if __name__ == "__main__":
    main()
