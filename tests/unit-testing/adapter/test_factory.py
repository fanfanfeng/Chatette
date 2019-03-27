"""
Test module.
Tests the functionalities that are present in module
`chatette_qiu.adapters.factory`.
"""

import pytest

from chatette_qiu.adapters.factory import create_adapter
from chatette_qiu.adapters.jsonl import JsonListAdapter
from chatette_qiu.adapters.rasa import RasaAdapter


def test_valid():
    assert isinstance(create_adapter("jsonl"), JsonListAdapter)
    assert isinstance(create_adapter("rasa"), RasaAdapter)

def test_invalid():
    assert create_adapter(None) is None
    with pytest.raises(ValueError):
        create_adapter("no adapter")
