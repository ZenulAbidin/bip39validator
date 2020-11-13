# BIP39 Wordlist Validator - A tool to validate BIP39 wordlists in Latin languages.
# Copyright 2020 Ali Sherief
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.


from bip39validator import InvalidWordList, ValidationFailed
from bip39validator.InitUniqResult import InitUniqResult
from bip39validator.InvalidRemoteContent import InvalidRemoteContent
from bip39validator.InvalidWordList import InvalidWordList
from bip39validator.LevDistResult import LevDistResult
from bip39validator.MaxLengthResult import MaxLengthResult
from bip39validator.ValidWordList import ValidWordList
from bip39validator.ValidationFailed import ValidationFailed
from bip39validator.internal.validation_tests import validate_sanitized_preamble, \
    validate_levenshtein_distance_preamble, validate_uniq_chars_preamble, \
    validate_length_preamble, validate_sanitized, \
    validate_levenshtein_distance, validate_uniq_chars, validate_length, regroup_prefix
from bip39validator.internal.util import contents2list, to_wordline_array, is_all_lower

"""Validation of BIP39 wordlists.

This module provides methods that check BIP39 wordlists
against a set of requirements, such
as a minimum Levenshtein distance between words, a
minimum number of unique initial characters, and a
maximum word length.

These test_vectors are not officially mandated by BIP39 but
have been generally accepted by the community.
"""


from .InvalidRemoteContent import InvalidRemoteContent
from .InvalidWordList import InvalidWordList
from .ValidWordList import ValidWordList
from .ValidationFailed import ValidationFailed
from .LevDistResult import LevDistResult
from .InitUniqResult import InitUniqResult
from .MaxLengthResult import MaxLengthResult
from .BIP39WordList import BIP39WordList
from .__main__ import main

__all__ = ['main', 'InvalidRemoteContent', 'InvalidWordList', 'ValidWordList',
           'ValidationFailed', 'LevDistResult', 'InitUniqResult', 'MaxLengthResult',
           'BIP39WordList']
