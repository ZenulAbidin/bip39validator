# BIP39 Wordlist Validator - A tool to validate BIP39 wordlists in Latin
# languages.
# bip39validator/validation_tests.py: Validation test_vectors
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

# Functions in this file are simultaneously the backbone of the command line
# program and the API.

import jellyfish
from .data_structs import LevDistArray
from .util import is_all_lower


# Callback functions called from progressbar()

def compute_lev_dist_interal(i, distance_array=[], wordlist=[], line_numbers=[],
                             n=0):
    for j in range(0, i):  # j between 0 and i-1 inclusive
        dist = jellyfish.levenshtein_distance(wordlist[j], wordlist[i])
        lev_array = {'dist': dist, 'indices': (j, i),
                     'lines': (line_numbers[j], line_numbers[i]),
                     'words': (wordlist[j], wordlist[i])
                     }
        distance_array.append(lev_array)
    return {'distance_array': distance_array, 'wordlist': wordlist,
            'line_numbers': line_numbers, 'n': n}


def sanitize_internal(i, err_lines=[], l=[], line_nums=[]):
    s = l[i]
    if not is_all_lower(s) or len(s) < 1:
        # In this test, the indices exactly correlate to the line numbers in the
        # file. (Add 1 to output index since line numbers are one-based)
        err_lines.append((s, i + 1))
        l[i] = None
        line_nums[i] = None
    return {'err_lines': err_lines, 'l': l, 'line_nums': line_nums}


# Generates a dictionary of prefixes organizing each group of words with the
# same prefix into the same key. A key with a string length of X means the
# words in it can be identified by the first X+1 characters.
# This means that keys with a string length of N have words that are identifiable
# by the first N+1 characters, which causes the test to fail.
# Note: N is the longest prefix length to group words by. Even if there are words
# that are so similar they must be identified by more than N+1 characters, this
# function will group them with key lengths of N.
# Words are uniquely identified by the prefix key and the first character in the word.
# In particular, words in the empty string key '' can be identified by the first
# character.
def uniq_chars_internal_2(i_dummy, words=[], lines=[], n=0, prefix_list={}):
    def prefix(wl, i, m):
        return wl[i][0][0:m]

    def matches(wl, i, j, m):
        word, line = wl[i]
        word2, line2 = wl[j]
        return word[0:m] == word2[0:m]

    # Supposed to be uncommented, but we're forced to use a legacy implementation
    # formerly used to accommodate rich.Progress progressbar.
    #    prefix_list = {}
    delete_indices = []
    words_lines = [*zip(words, lines)]
    for m in range(n, 0, -1):
        i = 0
        while i < len(words_lines) - 1:
            i_start = i
            i_end = i + 1
            if matches(words_lines, i, i + 1, m):
                for j in range(i + 1, len(words_lines)):
                    if not matches(words_lines, i_start, j, m):
                        break
                    i_end = j
                prefix_list[prefix(words_lines, i_start, m)] = words_lines[i_start:i_end + 1]
                delete_indices += [*range(i_start, i_end + 1)]
            i = i_end
        for d in reversed(delete_indices):
            words_lines.pop(d)
        if not words_lines:
            break
        delete_indices = []
    #prefix_list[''] = words_lines
    kwargs = {'words': words, 'lines': lines, 'n': n, 'prefix_list': prefix_list}
    return kwargs


def regroup_prefix(words, lines, threshold):
    ret = uniq_chars_internal_2(0, words=words, lines=lines, n=threshold, prefix_list={})
    return ret['prefix_list']


def length_internal(i, n=0, wordlist=[], line_numbers=[], long_words_indices=[]):
    if len(wordlist[i]) > n:
        long_words_indices.append({'index': i, 'word': wordlist[i], 'line':
            line_numbers[i]})
    return {'n': n, 'wordlist': wordlist, 'line_numbers': line_numbers,
            'long_words_indices': long_words_indices}


def validate_sanitized_preamble(l):
    line_nums = list(range(1, len(l) + 1))
    err_lines = []
    kwargs = {'err_lines': err_lines, 'l': l, 'line_nums': line_nums}
    return 0, len(l), sanitize_internal, kwargs


def validate_levenshtein_distance_preamble(word_line_arr, n):
    wordlist = word_line_arr.word_list
    line_numbers = word_line_arr.line_numbers

    kwargs = {'distance_array': [], 'wordlist': wordlist,
              'line_numbers': line_numbers, 'n': n}
    return 1, len(wordlist), compute_lev_dist_interal, kwargs


def validate_uniq_chars_preamble(word_line_arr, n):
    wordlist = word_line_arr.word_list
    line_numbers = word_line_arr.line_numbers
    kwargs = {'words': wordlist, 'lines': line_numbers, 'n': n, 'prefix_list': {}}
    return 0, 1, uniq_chars_internal_2, kwargs  # Only run this loop once


def validate_length_preamble(word_line_arr, n):
    wordlist = word_line_arr.word_list
    line_numbers = word_line_arr.line_numbers

    kwargs = {'n': n, 'wordlist': wordlist, 'line_numbers': line_numbers,
              'long_words_indices': []}
    return 0, len(word_line_arr.word_list), length_internal, kwargs


# The actual validation functions

# Given a list of lines in the wordlist read directly into list `l`, with no
# postprocessing except for splitting newlines, validate that all lines only
# contain lowercase characters.
# Returns True if validation succeeded, else returns False.
# It is mandatory for this test to succeed to ensure integrity of further test_vectors.
# Failure of this test aborts the validator.
def validate_sanitized(kwargs):
    err_lines = kwargs['err_lines']
    l = kwargs['l']
    line_nums = kwargs['line_nums']

    stats = {'is_sorted': None, 'length_exact': None, 'err_lines': err_lines,
             'length': None}

    # Count number of invalid words
    n_invalid_words = sum([1 if e is None else 0 for e in l])

    if len(l) != 2048:
        stats['length_exact'] = False
        stats['length'] = len(l)
    else:
        stats['length_exact'] = True
        stats['length'] = 2048

    ll = l
    ll.sort()
    if ll != l:
        stats['is_sorted'] = False
    else:
        stats['is_sorted'] = True

    if n_invalid_words > 0:
        return False, stats
    else:
        return True, stats



# Given a WordAndLineArray data structure `word_line_arr`, validate that all
# word pairs have a Levenshtein distance of at least `n`. Assume that the
# WordAndLineArray is sorted.
# Returns True if validation succeeded, else returns False.
def validate_levenshtein_distance(**kwargs):
    distance_array = kwargs['distance_array']
    n = kwargs['n']
    lev_dist_arr = LevDistArray(distance_array)

    # If lev_dist_arr is empty (has no elements), then this test succeeded.
    # Else it failed.
    n_small_levdists = len([a for a in distance_array if a['dist'] < n])

    if n_small_levdists > 0:
        return False, lev_dist_arr
    else:
        return True, lev_dist_arr


# Given a WordAndLineArray data structure `word_line_arr`, validate that all
# word pairs are unique in the first `n` characters. Assume that the
# WordAndLineArray is sorted.
# Returns True if validation succeeded, else returns False.
def validate_uniq_chars(**kwargs):
    # Get the keys, find the number of keys with length greater than or equal to
    # N, and return true or false if number's non-zero.
    prefix_list = kwargs['prefix_list']
    n = kwargs['n']
    n_notuniq = len([a for a in prefix_list if len(a) >= n])
    ret = kwargs
    #    n_notuniq = kwargs['n_notuniq']
    #    notuniq_words_range_arr = kwargs['notuniq_words_range_arr']
    #
    #    ret = {'n': kwargs['n'], 'n_notuniq': n_notuniq, 'notuniq_words_range_arr':
    #           notuniq_words_range_arr}
    if n_notuniq > 0:
        return False, ret
    else:
        return True, ret


# Given a WordAndLineArray data structure, validate that all words are no
# longer than `n` characters.
# Returns True if validation succeeded, else returns False.
def validate_length(**kwargs):
    long_words_indices = kwargs['long_words_indices']

    n_longwords = len(long_words_indices)

    if n_longwords > 0:
        return False, long_words_indices
    else:
        return True, long_words_indices
