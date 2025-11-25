#!/usr/bin/env python3
# archivo: src/base_freq.py

# Importar módulos necesarios
import argparse
import os
import sys
from typing import List, Tuple, Dict, Optional


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parsea los argumentos de la línea de comandos.

    Args:
        argv: Lista de argumentos (útil para tests). Si es None, argparse
            leerá de sys.argv.

    Returns:
        argparse.Namespace con el atributo `fasta`.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Calcula la frecuencia de A, T, G y C de un archivo FASTA con UNA sola secuencia."
        )
    )
    parser.add_argument("fasta", help="Archivo FASTA que contiene una sola secuencia.")
    return parser.parse_args(argv)


def read_file(path: str) -> str:
    """Lee y devuelve el contenido del archivo indicado.

    Lanza FileNotFoundError si no existe, y IOError en caso de otros errores de I/O.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as e:
        raise IOError(e)


def validate_is_fasta(content: str) -> None:
    """Valida que el contenido parece un FASTA con al menos una entrada.

    Lanza ValueError con el mensaje exacto usado en el programa original si la
    validación falla.
    """
    if ">" not in content:
        raise ValueError("Error: El archivo no parece estar en formato FASTA.")
    partes = content.split(">")
    # Si no hay partes después del split, o la primera parte está vacía
    if len(partes) < 2:
        raise ValueError("Error: FASTA vacío o sin secuencia válida.")


def parse_single_fasta(content: str) -> Tuple[str, str]:
    """Extrae el encabezado y la secuencia (raw) de la primera entrada FASTA.

    Devuelve (header, sequence_raw). Lanza ValueError si la secuencia está vacía
    (mensaje idéntico al original).
    """
    partes = content.split(">") #Dividir por '>'
    bloque = partes[1].strip().split("\n") #Elimina espacios y separa líneas
    header = bloque[0] #Primera línea es el encabezado
    seq_raw = "".join(bloque[1:]).strip() #Unir el resto como secuencia
    # Si la secuencia está vacía, lanzar error
    if len(seq_raw) == 0: 
        raise ValueError("Error: la secuencia está vacía.")
    return header, seq_raw


def clean_sequence(seq: str, valid_bases: Tuple[str, ...] = ("A", "T", "G", "C")) -> Tuple[str, List[str]]:
    """Normaliza la secuencia a mayúsculas, filtra bases válidas y recoge inválidos.

    Args:
        seq: Secuencia cruda (puede contener espacios, saltos de línea, caracteres N, etc.).
        valid_bases: tupla de bases consideradas válidas.

    Returns:
        (secuencia_limpia, lista_de_caracteres_invalidos_en_orden)
    """
    seq_upper = seq.upper() # Convertir a mayúsculas
    seq_clean = [] # Guardar bases válidas
    invalid_chars: List[str] = []
    for base in seq_upper:
        # Si base es válida, agregar a secuencia limpia; si no, a inválidos
        if base in valid_bases:
            seq_clean.append(base)
        else:
            invalid_chars.append(base)

    # Devolver secuencia limpia como string y lista de inválidos
    return "".join(seq_clean), invalid_chars


def compute_base_counts(seq: str) -> Dict[str, int]:
    """Cuenta A, T, G, C y total en la secuencia ya limpia (solo ATGC).

    Devuelve diccionario con claves 'A', 'T', 'G', 'C', 'total'.
    """
    return {
        "A": seq.count("A"),
        "T": seq.count("T"),
        "G": seq.count("G"),
        "C": seq.count("C"),
        "total": len(seq),
    }


def print_results(header: str, counts: Dict[str, int]) -> None:
    """Imprime los resultados en el mismo formato que el script original.

    Args:
        header: encabezado de la secuencia FASTA.
        counts: diccionario devuelto por compute_base_counts.
    """
    total = counts["total"]
    a = counts["A"]
    t = counts["T"]
    g = counts["G"]
    c = counts["C"]

    print("Encabezado:", header)
    print("Longitud secuencia válida:", total)
    print("Frecuencias:")
    # Mantener el mismo formato de redondeo
    print("A:", a, f"({round((a/total)*100,2)}%)")
    print("T:", t, f"({round((t/total)*100,2)}%)")
    print("G:", g, f"({round((g/total)*100,2)}%)")
    print("C:", c, f"({round((c/total)*100,2)}%)")


def main(argv: Optional[List[str]] = None) -> int:
    """Función principal que orquesta la ejecución.

    Devuelve 0 en éxito, 1 en errores (imprimiendo mensajes idénticos a los
    del script original).
    """
    # Parsear argumentos
    args = parse_args(argv)
    ruta = args.fasta

    # Intenta leer el archivo
    try:
        contenido = read_file(ruta)
    except FileNotFoundError:
        print("Error: el archivo no existe:", ruta)
        return 1
    except IOError as e:
        print("Error al leer el archivo:", e)
        return 1

    # Intenta obtener datos del FASTA
    try:
        validate_is_fasta(contenido)
        header, seq_raw = parse_single_fasta(contenido)
        seq_clean, invalid_chars = clean_sequence(seq_raw)

        # Imprimir avisos por caracteres inválidos en el mismo orden
        for ch in invalid_chars:
            print(f"Aviso: caracter inválido '{ch}' ignorado en la secuencia '{header}'")

        if len(seq_clean) == 0:
            print("Error: la secuencia no contiene bases válidas (A,T,G,C).")
            return 1

        # Imprimir resultados
        counts = compute_base_counts(seq_clean)
        print_results(header, counts)
        return 0
    except ValueError as e:
        # Los mensajes de ValueError ya contienen el texto exacto esperado
        print(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
