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


from typing import List, Dict
from _io import TextIOWrapper

import requests
from bip39validator.validation_tests import validate_sanitized_preamble, \
    validate_levenshtein_distance_preamble, validate_uniq_chars_preamble, \
    validate_length_preamble, validate_sanitized, \
    validate_levenshtein_distance, validate_uniq_chars, validate_length, regroup_prefix
from bip39validator.util import contents2list, to_wordline_array, is_all_lower

"""Validation of BIP39 wordlists.

This module provides methods that check BIP39 wordlists
against a set of requirements, such
as a minimum Levenshtein distance between words, a
minimum number of unique initial characters, and a
maximum word length.

These test_vectors are not officially mandated by BIP39 but
have been generally accepted by the community.
"""


class InvalidRemoteContent(Exception):
    """URL has an unexpected content type

  Exception raised by the ``BIP39WordList`` constructor.
  This class is not meant to be created directly.
  """

    """The offending URL"""
    url = None

    """The content type of ``url``"""
    content_type = None

    """The expected content type of ``url``"""
    expected_content_type = None

    def __init__(self, url, content_type, expected_content_type):
        self.url = url
        self.content_type = content_type
        self.expected_content_type = expected_content_type


class InvalidWordList(Exception):
    """One or more wordlist words have invalid characters.

  Exception raised by methods in ``BIP39WordList``. This
  class is not meant to be created directly.
  """

    """Indicates if the wordlist file has invalid characters in it.
  Any character that isn't lowercase ASCII is an invalid character.
  This member is always True.
  """
    has_invalid_chars = True

    """Tuple of line contents and line numbers of invalid words."""
    err_lines = None

    """Indicates if the wordlist file is in sorted order."""
    is_sorted = None

    """Indicates if the wordlist has exactly 2048 words."""
    has_2048_words = None

    """The number of words in the wordlist."""
    num_words = None

    def __init__(self, **kwargs):
        self.is_sorted = kwargs['is_sorted']
        self.err_lines = kwargs['err_lines']
        self.has_2048_words = kwargs['length_exact'] == 2048
        self.num_words = kwargs['length']
        super(Exception, self).__init__()


class ValidWordList:
    """The wordlist is well-formed and has no invalid characters.

  Data structure returned by ``BIP39WordList.test_lowercase()``.
  This class is not meant to be created directly.
  """

    """Indicates if the wordlist file has invalid chracters in it.
  Any character that isn't lowercase ASCII is an invalid character.
  This member is always False.
  """
    has_invalid_chars = False

    """Tuple of line contents and line numbers of invalid words."""
    err_lines = None

    """Indicates if the wordlist file is in sorted order."""
    is_sorted = None

    """Indicates if the wordlist has exactly 2048 words."""
    has_2048_words = None

    """The number of words in the wordlist."""
    num_words = None

    def __init__(self, **kwargs):
        self.is_sorted = kwargs['is_sorted']
        self.err_lines = kwargs['err_lines']
        self.has_2048_words = kwargs['length_exact']
        self.num_words = kwargs['length']


class ValidationFailed(Exception):
    """One of the validation test_vectors has failed.

  Exception raised by methods in ``BIP39WordList``. This
  class is not meant to be created directly.
  """

    def __init__(self, status_obj=None):
        self.status_obj = status_obj


class LevDistResult:
    """Levenshtein distances between each word pair.

  Data structure returned or raised by ``BIP39WordList.test_lev_distance()``.
  This class is not meant to be created directly.
  """

    """Test conducted with a minimum Levenshtien distance of ``threshold``."""
    threshold = None

    """Array of tuples containing exactly two words the
  Levenshtein distance was computed bewteen
  """
    word_pairs = []

    """Array of tuples containing exactly two line numbers
  corresponding to each word of ``word_pairs``
  """
    line_pairs = []

    """Array of tuples containing exactly two indices
  that reference the corresponding ``word_pairs`` and
  ``line_pairs``
  """
    index_pairs = []

    """Array of Levenshtien distance integers for each
  index, word and line pair
  """
    dists = []

    def __init__(self, res, threshold):
        self.word_pairs = [(a['words'][0], a['words'][1]) for a in res.lev_dist_arr]
        self.line_pairs = [(a['lines'][0], a['lines'][1]) for a in res.lev_dist_arr]
        self.index_pairs = [(a['indices'][0], a['indices'][1]) for a in res.lev_dist_arr]
        self.dists = [a['dist'] for a in res.lev_dist_arr]
        self.threshold = threshold

    """Gets the word pairs which have a Levenshtein distance of ``dist``

  :param dist: Levenshtein distance
  :type dist: int
  :returns: a list of word pairs
  """

    def getwordpairs_eq(self, dist=None):
        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for i in range(0, len(self.dists)):
            if self.dists[i] == dist:
                pairs.append(self.word_pairs[i])
        return pairs

    """Gets the line numbers of pairs which have a Levenshtein distance of ``dist``

  :param dist: Levenshtein distance
  :type dist: int
  :returns: a list of line pairs
  """

    def getlinepairs_eq(self, dist=None):
        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for i in range(0, len(self.dists)):
            if self.dists[i] == dist:
                pairs.append(self.line_pairs[i])
        return pairs

    """Gets the word pairs which have a Levenshtein distance less than ``dist``

  :param dist: Levenshtein distance
  :type dist: int
  :returns: a list of word pairs
  """

    def getwordpairs_lt(self, dist=None):
        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for i in range(0, len(self.dists)):
            if self.dists[i] < dist:
                pairs.append(self.word_pairs[i])
        return pairs

    """Gets the line numbers of pairs which have a Levenshtein distance less than ``dist``

  :param dist: Levenshtein distance
  :type dist: int
  :returns: a list of line number pairs
  """

    def getlinepairs_lt(self, dist=None):
        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for i in range(0, len(self.dists)):
            if self.dists[i] < dist:
                pairs.append(self.line_pairs[i])
        return pairs

    """Gets the word pairs which have a Levenshtein distance greater than ``dist``

  :param dist: Levenshtein distance
  :type dist: int
  :returns: a list of word pairs"""

    def getwordpairs_gt(self, dist=None):
        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for i in range(0, len(self.dists)):
            if self.dists[i] > dist:
                pairs.append(self.word_pairs[i])
        return pairs

    """Gets the line numbers of pairs which have a Levenshtein distance greater than ``dist``

  :param dist: Levenshtein distance
  :type dist: int
  :returns: a list of line number pairs"""

    def getlinepairs_gt(self, dist=None):
        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for i in range(0, len(self.dists)):
            if self.dists[i] > dist:
                pairs.append(self.line_pairs[i])
        return pairs

    """Gets the word pairs which have a Levenshtein distance inside the list ``dists``

  :param dists: list of Levenshtein distances
  :type dists: list
  :returns: a list of word pairs"""

    def getwordpairs_list(self, dists):
        assert type(dists) == list, 'Invalid type "{}" for argument `dists` (expected "list")' \
            .format(type(dists).__name__)
        assert len(dists) > 0, "Cannot use empty list as list of dists"

        pairs = []
        for i in range(0, len(dists)):
            assert type(dists[i]) == int, 'Invalid type "{}" for list element of `dists` (expected "int")' \
                .format(type(dists[i]).__name__)
            assert dists[i] > 0, "Distance must be greater than 0"

            if self.dists[i] in dists:
                pairs.append(self.word_pairs[i])
        return pairs

    """Gets the line numbers of pairs which have a Levenshtein distance inside the list ``dists``

  :param dists: list of Levenshtein distances
  :type dists: list
  :returns: a list of line number pairs"""

    def getlinepairs_list(self, dists):
        assert type(dists) == list, 'Invalid type "{}" for argument `dists` (expected "list")' \
            .format(type(dists).__name__)
        assert len(dists) > 0, "Cannot use empty list as list of dists"

        pairs = []
        for i in range(0, len(dists)):
            assert type(dists[i]) == int, 'Invalid type "{}" for list element of `dists` (expected "int")' \
                .format(type(dists[i]).__name__)
            assert dists[i] > 0, "Distance must be greater than 0"

            if self.dists[i] in dists:
                pairs.append(self.line_pairs[i])
        return pairs

    """Gets Levenshtein distance between ``word1`` and ``word2``

  :param word1: first word
  :type word1: str
  :param word2: second word
  :type word2: str
  :returns: Levenshtein distance between ``word1`` and ``word2``"""

    def getdist(self, word1, word2):
        assert type(word1) == str, 'Invalid type "{}" for argument `word1` (expected "str")' \
            .format(type(word1).__name__)
        assert len(word1) > 0, "Cannot use empty string as word"
        assert is_all_lower(word1), 'Word "{}" is not all ASCII lowercase'.format(word1)

        assert type(word2) == str, 'Invalid type "{}" for argument `word2` (expected "str")' \
            .format(type(word2).__name__)
        assert len(word2) > 0, "Cannot use empty string as word"
        assert is_all_lower(word2), 'Word "{}" is not all ASCII lowercase'.format(word2)

        if not is_all_lower(word1):
            raise ValueError("{} is not all lowercase".format(word1))
        if not is_all_lower(word2):
            raise ValueError("{} is not all lowercase".format(word2))
        if word1 > word2:
            word1, word2 = (word2, word1)
        arr = [self.dists[i] for i in range(0, len(self.word_pairs)) if
               self.word_pairs[i][0] == word1 and self.word_pairs[i][1] == word2]
        try:
            dist = arr[0]
            return dist
        except IndexError as e:
            raise KeyError("word pair \"{}\" and \"{}\" not found".format(word1,
                                                                          word2))

    """Gets Levenshtein distance between `word` and all other words

  :param word: the word
  :type word: str
  :returns: list of Levenshtein distances between ``word`` and each word"""

    def getdist_all(self, word):
        assert type(word) == str, 'Invalid type "{}" for argument `word` (expected "str")' \
            .format(type(word).__name__)
        assert len(word) > 0, "Cannot use empty string as word"
        assert is_all_lower(word), 'Word "{}" is not all ASCII lowercase'.format(word)

        dist_arr = [self.dists[i] for i in range(0, len(self.word_pairs)) if
                    self.word_pairs[i][0] == word or self.word_pairs[i][1] == word]
        word_arr = [self.word_pairs[i] for i in range(0, len(self.word_pairs)) if
                    self.word_pairs[i][0] == word or self.word_pairs[i][1] == word]
        line_arr = [self.line_pairs[i] for i in range(0, len(self.word_pairs)) if
                    self.word_pairs[i][0] == word or self.word_pairs[i][1] == word]
        dist_all = [*zip(word_arr, line_arr, dist_arr)]
        if dist_all == []:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all

    """Gets Levenshtein distance between ``word`` and all other words, equal to ``dist``

  :param word: the word
  :type word: str
  :param dist: Levenshtein distance
  :type dist: int
  :returns: list of Levenshtein distances between ``word`` and each word"""

    def getdist_all_eq(self, word, dist=None):
        if not dist:
            dist = self.threshold
        assert type(word) == str, 'Invalid type "{}" for argument `word` (expected "str")' \
            .format(type(word).__name__)
        assert len(word) > 0, "Cannot use empty string as word"
        assert is_all_lower(word), 'Word "{}" is not all ASCII lowercase'.format(word)

        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        dist_arr = [self.dists[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] == dist]
        word_arr = [self.word_pairs[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] == dist]
        line_arr = [self.line_pairs[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] == dist]
        dist_all = [*zip(word_arr, line_arr, dist_arr)]
        if dist_all == []:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all

    """Gets Levenshtein distance between ``word`` and all other words, less than ``dist``

  :param word: the word
  :type word: str
  :param dist: Levenshtein distance
  :type dist: int
  :returns: list of Levenshtein distances between ``word`` and each word"""

    def getdist_all_lt(self, word, dist=None):
        if not dist:
            dist = self.threshold
        assert type(word) == str, 'Invalid type "{}" for argument `word` (expected "str")' \
            .format(type(word).__name__)
        assert len(word) > 0, "Cannot use empty string as word"
        assert is_all_lower(word), 'Word "{}" is not all ASCII lowercase'.format(word)

        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        dist_arr = [self.dists[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] < dist]
        word_arr = [self.word_pairs[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] < dist]
        line_arr = [self.line_pairs[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] < dist]
        dist_all = [*zip(word_arr, line_arr, dist_arr)]
        if dist_all == []:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all

    """Gets Levenshtein distance between ``word`` and all other words, greater than ``dist``

  :param word: the word
  :type word: str
  :param dist: Levenshtein distance
  :type dist: int
  :returns: list of Levenshtein distances between ``word`` and each word"""

    def getdist_all_gt(self, word, dist=None):
        if not dist:
            dist = self.threshold
        assert type(word) == str, 'Invalid type "{}" for argument `word` (expected "str")' \
            .format(type(word).__name__)
        assert len(word) > 0, "Cannot use empty string as word"
        assert is_all_lower(word), 'Word "{}" is not all ASCII lowercase'.format(word)

        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        dist_arr = [self.dists[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] > dist]
        word_arr = [self.word_pairs[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] > dist]
        line_arr = [self.line_pairs[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] > dist]
        dist_all = [*zip(word_arr, line_arr, dist_arr)]
        if dist_all == []:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all

    """Gets Levenshtein distance between ``word`` and all other words, inside the list ``dists``

  :param word: the word
  :type word: str
  :param dists: list of Levenshtein distances
  :type dists: list
  :returns: list of Levenshtein distances between ``word`` and each word"""

    def getdist_all_list(self, word, dists):
        assert type(word) == str, 'Invalid type "{}" for argument `word` (expected "str")' \
            .format(type(word).__name__)
        assert len(word) > 0, "Cannot use empty string as word"
        assert is_all_lower(word), 'Word "{}" is not all ASCII lowercase'.format(word)

        assert type(dists) == list, 'Invalid type "{}" for argument `dists` (expected "list")' \
            .format(type(dists).__name__)
        assert len(dists) > 0, "Cannot use empty list as list of dists"

        for i in range(0, len(dists)):
            assert type(dists[i]) == int, 'Invalid type "{}" for list element of `dists` (expected "int")' \
                .format(type(dists[i]).__name__)
            assert dists[i] > 0, "Distance must be greater than 0"

        dist_arr = [self.dists[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] in dists]
        word_arr = [self.word_pairs[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] in dists]
        line_arr = [self.line_pairs[i] for i in range(0, len(self.word_pairs)) if
                    (self.word_pairs[i][0] == word or self.word_pairs[i][1] == word)
                    and self.dists[i] in dists]
        dist_all = [*zip(word_arr, line_arr, dist_arr)]
        if dist_all == []:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all


class InitUniqResult:
    """Initial unique characters (prefix) shared by each word pair.

  Data structure returned or raised by ``BIP39WordList.test_initial_chars()``.
  This class is not meant to be created directly.
  """

    """All word pairs in this class are unique up to ``threshold`` characters."""
    threshold = None

    regrouped_n = None

    """Array of 2-tuples containing start and end indices
  of a block of non-unique words.
  """
    word_pairs = []

    """Array of tuples containing exactly two line numbers
  corresponding to each word of ``word_pairs``
  """
    line_pairs = []

    """Array of tuples containing exactly two indices
  that reference the corresponding ``word_pairs`` and
  ``line_pairs``
  """
    index_pairs = []

    def __init__(self, res, threshold):
        self.prefix_list = res['prefix_list']
        self.n = res['n']
        self.words = res['words']
        self.lines = res['lines']
        self.threshold = threshold



    """Gets the list of words and lines beginning with ``prefix``
        
  As ``BIP39WordList`` sorts its internal copy of the wordlist, the words and
  lines in the returned tuple array are sorted in alphabetic order.

  :param prefix: the prefix
  :type prefix: str
  :returns: list of (word, line) tuples beginning with ``prefix``"""

    def similargroup(self, prefix):
        assert type(prefix) == str, 'Invalid type "{}" for argument `prefix` (expected "str")' \
            .format(type(prefix).__name__)
        assert len(prefix) > 0, "Cannot use empty string as prefix"

        n = len(prefix)
        prefix_list = regroup_prefix(self.words, self.lines, n)
        try:
            return prefix_list[prefix]
        except KeyError as e:
            return []

    """Gets the list of words beginning with ``prefix``

  As ``BIP39WordList`` sorts its internal copy of the wordlist, the words in the
  returned list are sorted in alphabetic order.
  
  :param prefix: the prefix
  :type prefix: str
  :returns: list of words beginning with ``prefix``"""

    def similar_wordgroup(self, prefix):
        assert type(prefix) == str, 'Invalid type "{}" for argument `prefix` (expected "str")' \
            .format(type(prefix).__name__)
        assert len(prefix) > 0, "Cannot use empty string as prefix"

        n = len(prefix)
        prefix_list = regroup_prefix(self.words, self.lines, n)
        try:
            return [a[0] for a in prefix_list[prefix]]
        except KeyError as e:
            return []

    """Gets the list of lines of words beginning with ``prefix``

  As ``BIP39WordList`` sorts its internal copy of the wordlist, the lines in the
  returned list are sorted in alphabetic order.
  
  :param prefix: the prefix
  :type prefix: str
  :returns: list of line numbers of words beginning with ``prefix``"""

    def similar_linegroup(self, prefix):
        assert type(prefix) == str, 'Invalid type "{}" for argument `prefix` (expected "str")' \
            .format(type(prefix).__name__)
        assert len(prefix) > 0, "Cannot use empty string as prefix"

        n = len(prefix)
        prefix_list = regroup_prefix(self.words, self.lines, n)
        try:
            return [a[1] for a in prefix_list[prefix]]
        except KeyError as e:
            return []

    """Gets the list of words and lines beginning with any of the prefixes in ``prefixes``

  As ``BIP39WordList`` sorts its internal copy of the wordlist, the words and
  lines in the returned tuple array are sorted in alphabetic order.

  :param prefixes: list of prefixes
  :type prefixes: str
  :returns: list of (word, line) tuples beginning with any of the ``prefixes``"""

    def similargroup_many(self, prefixes):
        assert type(prefixes) == list, 'Invalid type "{}" for argument `prefixes` (expected "list")' \
            .format(type(prefixes).__name__)
        assert len(prefixes) > 0, "Cannot use empty list as list of prefixes"

        groups = {}
        for prefix in prefixes:
            assert type(prefix) == str, 'Invalid type "{}" for list element of `prefixes` (expected "str")' \
                .format(type(prefix).__name__)
            assert len(prefix) > 0, "Cannot use empty string as prefix"

            n = len(prefix)
            prefix_list = regroup_prefix(self.words, self.lines, n)
            try:
                groups[prefix] = prefix_list[prefix]
            except KeyError as e:
                pass
        return groups

    """Gets the list of words beginning with any of the prefixes in ``prefixes``

  As ``BIP39WordList`` sorts its internal copy of the wordlist, the words in the
  returned list are sorted in alphabetic order.
  
  :param prefixes: list of prefixes
  :type prefixes: str
  :returns: list of words beginning with any of the ``prefixes``"""

    def similar_wordgroup_many(self, prefixes):
        assert type(prefixes) == list, 'Invalid type "{}" for argument `prefixes` (expected "list")' \
            .format(type(prefixes).__name__)
        assert len(prefixes) > 0, "Cannot use empty list as list of prefixes"

        groups = {}
        for prefix in prefixes:
            assert type(prefix) == str, 'Invalid type "{}" for list element of `prefixes` (expected "str")' \
                .format(type(prefix).__name__)
            assert len(prefix) > 0, "Cannot use empty string as prefix"

            n = len(prefix)
            prefix_list = regroup_prefix(self.words, self.lines, n)
            try:
                groups[prefix] = [a[0] for a in prefix_list[prefix]]
            except KeyError as e:
                pass
        return groups


    """Gets the list of lines of words beginning with any of the prefixes in ``prefixes``

  As ``BIP39WordList`` sorts its internal copy of the wordlist, the lines in the
  returned list are sorted in alphabetic order.
  
  :param prefixes: list of prefixes
  :type prefixes: str
  :returns: list of lines of words beginning with any of the ``prefixes``"""

    def similar_linegroup_many(self, prefixes):
        assert type(prefixes) == list, 'Invalid type "{}" for argument `prefixes` (expected "list")' \
            .format(type(prefixes).__name__)
        assert len(prefixes) > 0, "Cannot use empty list as list of prefixes"

        groups = {}
        for prefix in prefixes:
            assert type(prefix) == str, 'Invalid type "{}" for list element of `prefixes` (expected "str")' \
                .format(type(prefix).__name__)
            assert len(prefix) > 0, "Cannot use empty string as prefix"

            n = len(prefix)
            prefix_list = regroup_prefix(self.words, self.lines, n)
            try:
                groups[prefix] = [a[1] for a in prefix_list[prefix]]
            except KeyError as e:
                pass
        return groups

    """Gets the entire hash table of words and lines grouped by all prefixes of length ``n``

  :param n: prefix length to group by
  :type n: int
  :returns: dictionary of (word, line) tuples grouped by length ``n`` prefixes"""

    def similargroup_all(self, n):
        if not n:
            n = self.threshold
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Prefix length must be greater than 0'

        prefix_list = regroup_prefix(self.words, self.lines, n)
        return prefix_list

    """Gets the entire hash table of words grouped by all prefixes of length ``n``

  As ``BIP39WordList`` sorts its internal copy of the wordlist, the words and
  lines in the returned tuple array are sorted in alphabetic order.

  :param n: prefix length to group by
  :type n: int
  :returns: dictionary of words grouped by length ``n`` prefixes"""

    def similar_wordgroup_all(self, n):
        if not n:
            n = self.threshold
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Prefix length must be greater than 0'

        return {k: [a[0] for a in v] for k, v in self.similargroup_all(n).items()}

    """Gets the entire hash table of lines of words grouped by all prefixes of length ``n``

  :param n: prefix length to group by
  :type n: int
  :returns: dictionary of lines of words grouped by length ``n`` prefixes"""

    def similar_linegroup_all(self, n):
        if not n:
            n = self.threshold
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Prefix length must be greater than 0'

        return {k: [a[1] for a in v] for k, v in self.similargroup_all(n).items()}


class MaxLengthResult:
    """Length of each word exceeding a certain threshold.

  Data structure returned or raised by ``BIP39WordList.test_max_length()``.
  This class is not meant to be created directly.
  """

    """Maximum length parameter the test was performed against.

  All words in this class have a length no greater than this amount."""
    threshold = None

    """Array of indices of each word longer than ``threshold``"""
    words = []

    """Array of line numbers corresponding to each word in ``words``"""
    lines = []

    """Array of indicies that reference the corresponding ``words`` and ``lines``"""
    indices = []

    def __init__(self, res, threshold):
        self.threshold = threshold
        self.words = [a['word'] for a in res]
        self.lines = [a['line'] for a in res]
        self.indices = [a['index'] for a in res]

    """Gets the words which have a length of ``n``

  :param n: length
  :type n: int
  :returns: a list of words"""

    def getwords_eq(self, n):
        if not n:
            n = self.threshold
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Length must be greater than 0'

        arr = []
        for word in self.words:
            if len(word) == n:
                arr.append(word)
        return arr

    """Gets the line numbers of words which have a length of ``n``

  :param n: length
  :type n: int
  :returns: a list of line numbers"""

    def getlines_eq(self, n):
        if not n:
            n = self.threshold
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Length must be greater than 0'

        arr = []
        for word, line in zip(self.words, self.lines):
            if len(word) == n:
                arr.append(line)
        return arr

    """Gets the words which have a length less than ``n``

  :param n: length
  :type n: int
  :returns: a list of words"""

    def getwords_lt(self, n):
        if not n:
            n = self.threshold
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Length must be greater than 0'

        arr = []
        for word in self.words:
            if len(word) < n:
                arr.append(word)
        return arr

    """Gets the line numbers which have a length less than ``n``

  :param n: length
  :type n: int
  :returns: a list of line numbers"""

    def getlines_lt(self, n):
        if not n:
            n = self.threshold
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Length must be greater than 0'

        arr = []
        for word, line in zip(self.words, self.lines):
            if len(word) < n:
                arr.append(line)
        return arr

    """Gets the words which have a length greater than ``n``

  :param n: length
  :type n: int
  :returns: a list of words"""

    def getwords_gt(self, n):
        if not n:
            n = self.threshold
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Length must be greater than 0'

        arr = []
        for word in self.words:
            if len(word) > n:
                arr.append(word)
        return arr

    """Gets the line numbers which have a length greater than ``n``

  :param n: length
  :type n: int
  :returns: a list of line numbers"""

    def getlines_gt(self, n=None):
        if not n:
            n = self.threshold
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Length must be greater than 0'

        arr = []
        for word, line in zip(self.words, self.lines):
            if len(word) > n:
                arr.append(line)
        return arr

    """Gets the words which have a length inside the list ``lengths``

  :param lengths: list of lengths to check words with
  :type lengths: list
  :returns: a list of words"""

    def getwords_list(self, lengths):
        assert type(lengths) == list, 'Invalid type "{}" for argument `lengths` \
(expected "list")' \
            .format(type(lengths).__name__)
        assert len(lengths) > 0, 'Length list must not be empty'

        arr = []
        for word in self.words:
            if len(word) in lengths:
                arr.append(word)
        return arr

    """Gets the line numbers which have a length inside the list ``lengths``

  :param n: length
  :type n: int
  :returns: a list of line numbers"""

    def getlines_list(self, lengths):
        assert type(lengths) == list, 'Invalid type "{}" for argument `lengths` \
(expected "list")' \
            .format(type(lengths).__name__)
        assert len(lengths) > 0, 'Length list must not be empty'

        arr = []

        for n in lengths:
            assert type(n) == int, 'Invalid type "{}" for list element of `lengths` (expected "int")' \
                .format(type(n).__name__)
            assert n > 0, 'Length must be greater than 0'

        for word, line in zip(self.words, self.lines):
            if len(word) in lengths:
                arr.append(line)
        return arr


class BIP39WordList:
    """Encapsulates a BIP39 wordlist."""

    """A textual description of the wordlist."""
    desc = None

    """The list of words."""
    words = None

    def __init__(self, desc, string=None, handle=None, url=None):
        """Initializes a BIP39WordList object

    Words can be read from a string buffer, a file
    handle or a URL. The precedence order of the inputs
    is ``string``, then ``handle``, then ``url``. The wordlist
    is expected to contain one word on each line with no
    intermediate whitespaces or blank lines (this includes newline
    at the end of the file), but actual validation of
    these requirements is not performed here.

    :param desc: textual description of the word list
    :type desc: str
    :param string: string buffer to read the words from, defaults to None
    :type string: str, optional
    :param handle: file handle to read the words from, defaults to None
    :type handle: class:``_io.TextIOWrapper``, optional
    :param url: URL to read the words from, defaults to None
    :type url: str, optional

    :raises ValueError: ``string``, ``handle`` or ``url`` must be specified
    :raises InvalidWordList: non-lowercase characters
        in words
    """
        self.desc = desc

        if string:
            assert type(string) == str, 'Invalid type "{}" for argument `string` (expected "str")' \
                .format(type(string).__name__)
            assert len(string) > 0, "Cannot use empty bytes string as prefix"

            self.words = contents2list(string)
        elif handle:
            assert type(handle) == TextIOWrapper, 'Invalid type "{}" for argument `handle` (expected \
          "TextIOWrapper")'.format(type(handle).__name__)

            s = handle.read()
            self.words = contents2list(s)
        elif url:
            assert type(url) == str, 'Invalid type "{}" for argument `url` (expected "str")' \
                .format(type(url).__name__)
            assert len(url) > 0, "Cannot use empty string as url"
            r = requests.get(url)
            content_type = r.headers['content-type'].split('; ')[0]
            if content_type != 'text/plain':
                raise InvalidRemoteContent(url, content_type, 'text/plain')
            s = r.content.decode("utf-8")
            self.words = contents2list(s)
        else:
            raise ValueError('`string`, `handle` or `url` must be specified')
        if not all([is_all_lower(w) for w in self.words]):
            dummy = {'is_sorted': False, 'length': len(self.words),
                     'has_invalid_chars': True, 'length_exact': len(self.words),
                     'err_lines': []}
            raise InvalidWordList(**dummy)
        self._assemble()

    def _assemble(self):
        # Note: self.words is not passed to a sort function
        self.word_line_sorted = to_wordline_array(self.words)
        self.words_sorted = self.word_line_sorted.word_list
        self.lines_sorted = self.word_line_sorted.line_numbers

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return "<bip39validator.BIP39WordList desc=\"{}\", wordlist=[{} words]>" \
            .format(self.desc, len(self.words))

    def __str__(self):
        return repr(self)

    """Gets the line number if ``key`` is a word, or the
       word if ``key`` is a line number

    :param key: a word, or a line number in the wordlist
    :type key: str
    :returns: the corresponding line number or word
    """

    def __getitem__(self, key):
        try:
            if isinstance(key, str):
                idx = self.lines_sorted[self.words.index(key)]
                return idx
            elif isinstance(key, int):
                word = self.words[self.lines_sorted.index(key)]
                return word
        except (IndexError, ValueError) as e:
            raise ValueError(key)

        if any([key == item for item in self.words]):
            return self.word_line_arr.__getattribute__(key)
        # FIXME hanging?

    def test_lowercase(self):
        """Checks for forbidden characters in a wordlist.

      Checks each word in the wordlist to ensure it only
      contains lowercase characters on each line, with
      no *empty lines* or *whitespace* anywhere on each
      line. Trailing newline at the end of the file is
      also forbidden.

      :return: ``None``
      :raises InvalidWordList: non-lowercase characters
          in one or more words
      """
        low, high, callback, kwargs = self._test_lowercase_1()
        for i in range(low, high):
            kwargs = callback(i, **kwargs)
        return self._test_lowercase_2(kwargs)

    def _test_lowercase_1(self):
        return validate_sanitized_preamble(self.words)

    def _test_lowercase_2(self, kwargs):
        (success, obj) = validate_sanitized(kwargs)
        if success:
            return ValidWordList(**obj)
        else:
            raise InvalidWordList(**obj)

    def test_lev_distance(self, n):
        """Runs the minimum Levenshtein distance test.

      The minimum Levenshtein distance test takes each
      combination of two words in the wordlist and
      calculates the Levenshtein distance between them.

      :param n: minimum Levenshtein distance required
      :type n: int
      :returns: an instance of ``LevDistResult``
      :raises ValidationFailed: <LevDistResult object>
      """
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Distance must be greater than 0'

        self.test_lowercase()
        low, high, callback, kwargs = self._test_lev_distance_1(n)
        for i in range(low, high):
            kwargs = callback(i, **kwargs)
        return self._test_lev_distance_2(kwargs)

    def _test_lev_distance_1(self, n):
        return validate_levenshtein_distance_preamble(self.word_line_sorted, n)

    def _test_lev_distance_2(self, kwargs):
        success, res = validate_levenshtein_distance(**kwargs)
        obj = LevDistResult(res, threshold=kwargs['n'])
        if success:
            return obj
        else:
            raise ValidationFailed(obj)

    def test_initial_chars(self, n):
        """Runs the maximum unique initial characters test.

      The maximum unique initial characters test takes each
      combination of two words in the wordlist and compares
      their first ``n`` characters for equality.

      ``n`` is required, since there is no use case
      for analyzing pairs of BIP39 words with arbitrary unique
      prefixes.

      :param n: maximum unique initial characters required.
      :type n: int
      :returns: an instance of ``InitUniqResult``
      :raises ValidationFailed: <InitUniqResult object>
      """
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Maximum unique initial chars must be greater than 0'

        low, high, callback, kwargs = self._test_initial_chars_1(n)
        for i in range(low, high):
            kwargs = callback(i, **kwargs)
        return self._test_initial_chars_2(kwargs)

    def _test_initial_chars_1(self, n):
        return validate_uniq_chars_preamble(self.word_line_sorted, n)

    def _test_initial_chars_2(self, kwargs):
        success, res = validate_uniq_chars(**kwargs)
        obj = InitUniqResult(res, threshold=kwargs['n'])
        if success:
            return obj
        else:
            raise ValidationFailed(obj)

    def test_max_length(self, n):
        """Runs the maximum word length test.

      :param n: maximum word length allowed

      This parameter is required, since there is no use case
      for analyzing BIP39 words with arbitrary lengths.
      :type n: int

      :returns: an instance of ``MaxLengthResult``
      :raises ValidationFailed: <MaxLengthResult object>
      """
        assert type(n) == int, 'Invalid type "{}" for argument `n` (expected "int")' \
            .format(type(n).__name__)
        assert n > 0, 'Length must be greater than 0'

        low, high, callback, kwargs = self._test_max_length_1(n)
        for i in range(low, high):
            kwargs = callback(i, **kwargs)
        return self._test_max_length_2(kwargs)

    def _test_max_length_1(self, n):
        return validate_length_preamble(self.word_line_sorted, n)

    def _test_max_length_2(self, kwargs):
        success, res = validate_length(**kwargs)
        obj = MaxLengthResult(res, threshold=kwargs['n'])
        if success:
            return obj
        else:
            raise ValidationFailed(obj)
