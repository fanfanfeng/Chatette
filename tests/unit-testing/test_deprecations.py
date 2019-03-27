"""
Test module.
Tests the functions in module 'chatette_qiu.utils'.
"""

import chatette_qiu.deprecations
from chatette_qiu.deprecations import warn_semicolon_comments


def test_several_calls():
    assert not chatette_qiu.deprecations._SEMICOLON_COMMENTS_DEPRECATION_WARNED
    warn_semicolon_comments()
    assert chatette_qiu.deprecations._SEMICOLON_COMMENTS_DEPRECATION_WARNED
