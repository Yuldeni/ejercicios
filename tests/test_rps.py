import sys
import builtins
from unittest import mock
import pytest
import random

from rps import determine_result, play, main


def test_determine_result_all_combinations():
    # All combos and expected outcomes
    combos = [
        ("rock", "scissors", "win"),
        ("rock", "paper", "lose"),
        ("rock", "rock", "draw"),
        ("paper", "rock", "win"),
        ("paper", "scissors", "lose"),
        ("paper", "paper", "draw"),
        ("scissors", "paper", "win"),
        ("scissors", "rock", "lose"),
        ("scissors", "scissors", "draw"),
    ]
    for user, cpu, expected in combos:
        assert determine_result(user, cpu) == expected


def test_play_valid_choice_and_random_cpu(monkeypatch):
    # Make random.choice deterministic
    monkeypatch.setattr(random, "choice", lambda x: "paper")
    cpu, result = play("rock")
    assert cpu == "paper"
    assert result == "lose"


def test_play_invalid_choice_raises():
    with pytest.raises(ValueError):
        play("lizard")


def test_main_cli_flow_win(monkeypatch, capsys):
    # Monkeypatch input to simulate a winning round then empty to exit
    inputs = ["rock", ""]
    monkeypatch.setattr(builtins, "input", lambda prompt="": inputs.pop(0))
    # Force CPU to choose scissors so user rock wins
    monkeypatch.setattr(random, "choice", lambda choices: "scissors")
    main()
    out = capsys.readouterr().out
    assert "CPU: scissors" in out
    assert "Resultado: win" in out
    assert "🎉✨🚀 ¡Ganaste! 🎉✨🚀" in out


def test_main_invalid_input_shows_message(monkeypatch, capsys):
    # Simulate invalid input followed by enter to exit
    inputs = ["spock", ""]
    monkeypatch.setattr(builtins, "input", lambda prompt="": inputs.pop(0))
    main()
    out = capsys.readouterr().out
    assert "Entrada inválida" in out
