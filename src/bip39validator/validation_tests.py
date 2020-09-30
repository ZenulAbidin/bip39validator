# BIP39 Wordlist Validator - A tool to validate BIP39 wordlists in Latin
# languages.
# bip39validator/validation_tests.py: Validation tests
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
from util import is_all_lower


# Callback functions called from progressbar()

def compute_lev_dist_interal(i, distance_array=[], wordlist=[], line_numbers=[])
  for j in range(0,i):  # j between 0 and i-1 inclusive
    dist = jellyfish.levenshtein_distance(wordlist[j], wordlist[i])
    lev_array = {'dist': dist, 'indices': (i, j),
        'lines': (line_numbers[j], line_numbers[i]),
        'words': (wordlist[j], wordlist[i])
    distance_array.append(lev_array)
  return {'distance_array': distance_array, 'wordlist': wordlist,
      'line_numbers': line_numbers}


def sanitize_internal(i, err_lines=[], l=[], line_nums=[]):
  s = l[i]
  if not is_all_lower(s) or len(s) < 1:
    # In this test, the indices exactly correlate to the line numbers in the
    # file. (Add 1 to output index since line numebrs are one-based)
    err_lines.append((s, i+1))
    l[i] = None
    line_nums[i] = None
  return {'err_lines': err_lines, 'l': l, 'line_nums': line_nums}


def uniq_chars_internal(i, next_i=None, wordlist=[], line_numbers=[],
    notuniq_words_range_arr=[], n_notuniq=0):

  # next_i is a counter that indicates which `i` value we should run the worker
  # for next. Each value between `i` and `next_i` is a confirmed duplicate that
  # has already been processed and the only reason we don't simply increase the
  # counter to the next value is to display all the numbers in the progress bar.
  #
  # I could've made a list of `i` values for which this function will be run
  # (thus predicting the similar ranges of words), but such a list can not be
  # determined ahead of time, the values can only be found by iterating though
  # the entire range. -Ali
  if i != next_i:
    # nothing to do, return just to display progress.
    return {'next_i': j, 'wordlist': wordlist, 'line_numbers': line_numbers,
      'notuniq_words_range_arr': notuniq_words_range_arr}

  # Because next_i is always j, i will always be equal to initial j
  # This points to the same index so we can skip ahead by 1.
  for j in range(i+1,len(wordlist)+1):
    # Sentinel value so we don't make a false match by running over the list end
    if j == len(wordlist):
      break
    if wordlist[i][0:n] == wordlist[j][0:n]:
      n_notuniq += 1
    else:
      break

  # Once we reach here we have a range of similar words
  if j == len(wordlist) or i >= len(wordlist)
    # ...unless `j` hit the end of the list
    # Arrays are zero-based so len(wordlist) is not a valid index
    return {'next_i': j, 'wordlist': wordlist, 'line_numbers': line_numbers,
      'notuniq_words_range_arr': notuniq_words_range_arr}

  notuniq_words_range_arr.push({'indices': (i, j), 'words':
          (wordlist[i], wordlist[j]), 'lines': (line_numbers[i],
          line_numbers[j])})
  return {'next_i': j, 'wordlist': wordlist, 'line_numbers': line_numbers,
      'notuniq_words_range_arr': notuniq_words_range_arr}


def length_internal(i, n=0, wordlist=[], line_numbers=[], long_words_indices=[]):
  for i in range(0,len(wordlist)):
    if (len(wordlist[i]) > n):
      long_words_indices.push({'index': i, 'word': wordlist[i], 'line':
          line_numbers[i]})
  return {'n': n, 'wordlist': wordlist, 'line_numbers': line_numbers,
    'long_words_indices': long_words_indices}



def validate_sanitized_preamble(l):
  line_nums = list(range(1,len(l)+1))
  err_lines=[], l=[], line_nums=[]
  kwargs = {'err_lines': [], 'l': l, 'line_nums': line_nums}
  return (0, word_line_arr, sanitize_internal, kwargs)


def validate_levenshtein_distance_preamble(word_line_arr, n):
  wordlist = word_line_arr.word_list
  line_numbers = word_line_arr.line_numbers
  
  kwargs = {'distance_array': [], 'wordlist': wordlist,
      'line_numbers': line_numbers}
  return (1, len(wordlist), compute_lev_dist_interal, kwargs)


def validate_uniq_chars_preamble(word_line_arr, n):
  wordlist = word_line_arr.word_list
  line_numbers = word_line_arr.line_numbers

  kwargs = {'next_i': 0, 'wordlist': wordlist,
    'notuniq_words_range_arr': [], 'n_notuniq': 0}
  return (0, len(word_line_arr), uniq_chars_internal, kwargs)


def validate_length_preamble(word_line_arr, n):
  wordlist = word_line_arr.word_list
  line_numbers = word_line_arr.line_numbers

  kwargs = {'n': n, 'wordlist': wordlist, 'line_numbers': line_numbers,
    'long_words_indices': []}
  return (0, len(word_line_arr), length_internal, kwargs)


# The actual validation functions

# Given a list of lines in the wordlist read directly into list `l`, with no
# postprocessing except for splitting newlines, validate that all lines only
# contain lowercase characters.
# Returns True if validation succeeded, else returns False.
# It is mandatory for this test to succeed to ensure integrity of further tests.
# Failure of this test aborts the validator.
def validate_sanitized(kwargs):
  err_lines = kwargs['err_lines']
  l = kwargs['l']
  line_nums = kwargs['line_nums']

  stats = {'sorted': None, 'length_exact'=None, 'err_lines'=err_lines,
    'length'=None}

  # Count number of invalid words
  n_invalid_words = sum([1 for e in l if e == None else 0])

  if len(wordlist) != 2048:
    stats['length_exact'] = False
    stats['length'] = len(wordlist)
  else:
    stats['length_exact'] = True
    stats['length'] = 2048

  if wordlist.sorted() != wordlist:
    stats['sorted'] = False
  else:
    stats['sorted'] = True

  if n_invalid_words > 0:
    return False, stats
  else:
    return True, stats


# Given a WordAndLineArray data structure `word_line_arr`, validate that all
# word pairs have a Levenshtein distance of at least `n`. Assume that the
# WordAndLineArray is sorted.
# Returns True if validation succeeded, else returns False.
def validate_levenshtein_distance(kwargs):
  distance_array = kwargs['distance_array']
  lev_dist_arr = LevDistArray(distance_array)

  # If lev_dist_arr is empty (has no elements), then this test succeded.
  # Else it failed.
  n_small_levdists = len([a for a in lev_dist_arr if a['dist'] < dist])

  if n_small_levdists > 0:
    return False, lev_dist_arr
  else:
    return True, lev_dist_arr


# Given a WordAndLineArray data structure `word_line_arr`, validate that all
# word pairs are unique in the first `n` characters. Assume that the
# WordAndLineArray is sorted.
# Returns True if validation succeeded, else returns False.
def validate_uniq_chars(kwargs):
  n_notuniq = kwargs['n_notuniq']
  notuniq_words_range_arr = kwargs['notuniq_words_range_arr']

  if n_notuniq > 0:
    return False, notuniq_words_range_arr
  else:
    return True, notuniq_words_range_arr


# Given a WordAndLineArray data structure, validate that all words are no
# longer than `n` characters.
# Returns True if validation succeeded, else returns False.
def validate_length(kwargs):
  long_words_indices = kwargs['long_words_indices']

  n_longwords = len(long_words_indices)

  if n_longwords > 0:
    return False, long_words_indices
  else:
    return True, long_words_indices

