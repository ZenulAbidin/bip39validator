# BIP39 Wordlist Validator - A tool to validate BIP39 wordlists in Latin
# languages.
# bip39validator/data_structs.py: Program data structures.
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

# A data structure consisting of
# - An array of strings `word_list`
# - An array of line numbers `line_numbers`
# Each entry in `word_list` is associated with the corresponding entry in
# `line_number`. They are expected to have the same length.
# It is returned by the following functions:
# - sanitize()
# And is passed to the following functions:
# - compute_levenshtein_distance()
class WordAndLineArray:
    def __init__(self, args):
        self.word_list = args[0]
        self.line_numbers = args[1]


# A data structure consisting of
# - An integer distance `dist`
# - A pair of line numbers `line_numbers`
# - A pair of words `words`
class LevDist:
    def __init__(self, **kwargs):
        self.dist = kwargs['dist']
        self.line_numbers = kwargs['line_numbers']
        self.words = kwargs['words']


# A data structure consisting of an array of LevDist values.
# It is returned by the following functions:
# - compute_levenshtein_distance()
# And is passed to the following functions:
# 
class LevDistArray:
    def __init__(self, lev_dist_arr):
        self.lev_dist_arr = lev_dist_arr
