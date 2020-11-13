# BIP39 Wordlist Validator - A tool to validate BIP39 wordlists in Latin
# languages.
# bip39validator/util.py: Supporting utility functions.
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

import unicodedata as ud
from bip39validator.internal.data_structs import WordAndLineArray



def longestCommonPrefix(strs):
    """
    :type strs: List[str]
    :rtype: str
    """
    if len(strs) == 0:
        return ""
    current = strs[0]
    for i in range(1, len(strs)):
        temp = ""
        if len(current) == 0:
            break
        for j in range(len(strs[i])):
            if j < len(current) and current[j] == strs[i][j]:
                temp += current[j]
            else:
                break
        current = temp
    return current


# Credits: https://stackoverflow.com/a/15547803/12452330
def rmdiacritics(word):
    """
    Removes all diacritics from each character in `word`
    like accents or curls and strokes and the like.
    """
    ret_word = ""
    for char in word:
        desc = ud.name(char)
        cutoff = desc.find(' WITH ')
        if cutoff != -1:
            desc = desc[:cutoff]
            try:
                char = ud.lookup(desc)
            except KeyError:
                pass  # removing "WITH ..." produced an invalid name
        ret_word += char
    return ret_word


# Lambda function that test_vectors a character if it's lowercase English.
# Do not use str.islower() because it also returns true for accented lowercase
# letters.
def is_lower(c):
    return True if c in 'abcdefghijklmnopqrstuvwxyz' else False


# Lambda function to test if *all* the characters in a string are lowercase
# English. Again, don't use str.islower() because it returns true even if some
# characters aren't lowercase (e.g. digits and symbols)
def is_all_lower(s):
    return s != '' and all([True if is_lower(c) else False for c in s])


# Given a list of lines in the wordlist read directly into list `l`, with no
# postprocessing except for splitting newlines, return a WordAndLineArray
# data structure.
def to_wordline_array(l):
    # Please do NOT modify the wordlist array in-code. It may be lucrative to
    # sanitize the wordlist array ourselves but this will scramble the line
    # numbers of the remaining words in the array causing that information to be
    # lost. -Ali

    line_nums = list(range(1, len(l) + 1))
    # Creates a list with elements that are tuples ('word', line of word)
    zipped_l_arr = list(zip(l, line_nums))

    # The key is index 0 of each tuple.
    sortkey = lambda e: e[0]
    zipped_l_arr.sort(key=sortkey)

    # Unzip the list, split the tuple elements in their own arrays.
    return WordAndLineArray(list(zip(*zipped_l_arr)))


# Given the entirety of the file read as a string buffer `buf`, split it by
# newlines into a list. Do not clean it up, do not remove whitespace in any way.
def contents2list(buf):
    l = buf.split("\n")

    # Remove extraneous empty element after the last newline if the file ends with
    # newline.
    # This will *not* remove trailing blank line that has whitespace in it.
    if not l[-1]:
        l.pop()
    return l
