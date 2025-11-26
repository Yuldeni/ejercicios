#!/usr/bin/env python3
"""Juego Piedra, Papel o Tijera (Rock-Paper-Scissors).

Este módulo implementa un juego interactivo por línea de comandos donde
el usuario juega contra la computadora. La interacción es simple:
- El usuario escribe "rock", "paper" o "scissors".
- El juego se repite hasta que el usuario presiona ENTER sin introducir valor.
- La computadora selecciona aleatoriamente una opción.
- Se imprime el resultado de cada ronda y si el usuario gana se muestran
    emojis de celebración.

El módulo proporciona las funciones:
- determine_result(user, cpu): determina victoria/derrota/empate.
- play(user_choice): ejecuta una ronda y devuelve (cpu_choice, resultado).
- main(): bucle principal del CLI.
"""

import random
from typing import Tuple


# Lista de opciones válidas
VALID_CHOICES = ["rock", "paper", "scissors"]


def determine_result(user: str, cpu: str) -> str:
    """Determina el resultado de una ronda entre usuario y CPU.

    Args:
        user: Elección del usuario -- una de "rock", "paper", "scissors".
        cpu: Elección de la CPU -- una de "rock", "paper", "scissors".

    Returns:
        'win' si el usuario gana, 'lose' si pierde, y 'draw' si empatan.
    """
    # Igualdad
    if user == cpu:
        return "draw"

    # Mapa de victoria: clave gana a valor
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    if wins.get(user) == cpu:
        return "win"
    return "lose"


def play(user_choice: str) -> Tuple[str, str]:
    """Ejecuta una ronda del juego con la elección del usuario.

    Valida la entrada, elige la jugada de la CPU al azar y calcula el resultado.

    Args:
        user_choice: Elección del usuario ('rock'|'paper'|'scissors').

    Returns:
        Tupla (cpu_choice, resultado) donde resultado es 'win'|'lose'|'draw'.
    """
    # Validar entrada
    if user_choice not in VALID_CHOICES:
        raise ValueError(f"Opción inválida: {user_choice}")

    # Elegir para la CPU
    cpu_choice = random.choice(VALID_CHOICES)

    # Determinar resultado
    result = determine_result(user_choice, cpu_choice)
    return cpu_choice, result


def main() -> None:
    """Bucle principal del juego. Lee entradas del usuario y muestra resultados.

    El bucle se repite hasta que el usuario presione ENTER sin escribir nada.
    Para cada ronda se valida la entrada, se imprime la elección de la CPU y
    el resultado. Si el usuario gana, se muestra un mensaje con emojis.
    """
    print("🎮 Rock, Paper, Scissors Game 🎮")
    print("Escribe rock, paper o scissors.")
    print("Presiona ENTER sin escribir nada para salir.")
    print("-" * 40)

    while True:
        # Leer entrada del usuario
        user_input = input("Tu elección (rock/paper/scissors) > ").strip().lower()

        # Salir si presiona ENTER
        if user_input == "":
            print("¡Gracias por jugar! Hasta la próxima 👋")
            break

        if user_input not in VALID_CHOICES:
            print("Entrada inválida. Escribe rock, paper o scissors.")
            continue

        cpu_choice, result = play(user_input)
        print(f"CPU: {cpu_choice}")
        print(f"Resultado: {result}")
        if result == "win":
            print("🎉✨🚀 ¡Ganaste! 🎉✨🚀")


if __name__ == "__main__":
    main()
