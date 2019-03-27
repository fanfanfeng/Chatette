"""
Test module
Tests the functionalities present in module
`chatette_qiu.cli.interactive_commands.exist_command`.
"""

import pytest

from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy
from chatette_qiu.cli.interactive_commands.exist_command import ExistCommand

from test_command_strategy import get_facade


def test_obj():
    cmd = ExistCommand("")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == []

    cmd = ExistCommand("exist ~ /a/")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == ["exist", "~", "/a/"]


def test_err(capsys):
    cmd = ExistCommand("nothing")
    assert cmd.command_tokens == ["nothing"]
    cmd.execute(get_facade())
    captured = capsys.readouterr()
    assert "[ERROR]\tMissing some arguments\n\tUsage: " + \
           'exist <unit-type> "<unit-name>"' in captured.out


def test_execute(capsys):
    cmd = ExistCommand('exist alias "sorry"')
    assert cmd.command_tokens == ["exist", "alias", '"sorry"']
    facade = get_facade()
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "alias: 'sorry'\nmodifiers:\n\tNone\n0 variations" in captured.out

    cmd = ExistCommand('exist ~ /o/g')
    assert cmd.command_tokens ==  ["exist", "~", "/o/g"]
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "alias: 'can you'\nmodifiers:\n\tNone\n0 variations" in captured.out
    assert "alias: 'sorry'\nmodifiers:\n\tNone\n0 variations" in captured.out

    cmd = ExistCommand('exist slot "INEXISTANT"')
    assert cmd.command_tokens == ["exist", "slot", '"INEXISTANT"']
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "Slot 'INEXISTANT' is not defined." in captured.out

def test_variations(capsys):
    cmd = ExistCommand('exist alias "var#one"')
    assert cmd.command_tokens == ["exist", "alias", '"var#one"']
    facade = get_facade()
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "alias: 'var'\nmodifiers:\n\tNone\n2 variations:\n" in captured.out
    assert "\t- one\n" in captured.out
    assert "\t- two with space\n" in captured.out
    assert "Variation 'one' is defined for this alias." in captured.out

    cmd = ExistCommand('exist ~ "var#two with space"')
    assert cmd.command_tokens == ["exist", "~", '"var#two with space"']
    facade = get_facade()
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "alias: 'var'\nmodifiers:\n\tNone\n2 variations:\n" in captured.out
    assert "\t- two with space\n" in captured.out
    assert "\t- one\n" in captured.out
    assert "Variation 'two with space' is defined for this alias." in captured.out
    
    cmd = ExistCommand('exist alias "var#no var"')
    assert cmd.command_tokens == ["exist", "alias", '"var#no var"']
    facade = get_facade()
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "alias: 'var'\nmodifiers:\n\tNone\n2 variations:\n" in captured.out
    assert "Variation 'no var' is not defined for this alias." in captured.out
