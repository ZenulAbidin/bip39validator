# BIP39 Wordlist Validator - A tool to validate BIP39 wordlists in Latin
# languages.
# __main__.py: Main program
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

import argparse
import pdb
from os.path import abspath
from bip39validator.InvalidWordList import InvalidWordList
from bip39validator.ValidationFailed import ValidationFailed
from bip39validator.BIP39WordList import BIP39WordList
from bip39validator.internal.logging import setargs, progressbar, logerror, loginfo, \
    logdefault, separator, logwarning
from bip39validator.__version__ import __version__

default_lev = 2
default_init_uniq = 4
default_max_length = 8


def version_str():
    return """BIP39 Validator {}
Copyright (C) 2020 Ali Sherief
License: MIT License <https://opensource.org/licenses/MIT>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Ali Sherief.""".format(__version__)


def abort(debug):
    if debug:
        logerror("Debug mode on, entering pdb")
        pdb.set_trace()
        exit(1)
    else:
        logerror("Aborting")
        exit(1)


log_file = None
args = None


def main():
    try:
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                         description='BIP39 wordlist validator')
        parser.add_argument('input', type=str, help='path to the input file')
        parser.add_argument('-d', '--min-levenshtein-distance', dest='lev_dist',
                            default=default_lev, type=int, help='set the minimum required \
  Levenshtein distance between words (default: {})'.format(default_lev))
        parser.add_argument('-u', '--max-initial-unique', dest='init_uniq',
                            default=default_init_uniq, type=int, help='set the maximum \
  required unique initial characters between words (default: {})'.format(
                default_init_uniq))
        parser.add_argument('-l', '--max-length', dest='max_length',
                            default=default_max_length, type=int, help='set the maximum length of \
  each word (default: {})'.format(default_max_length))
        parser.add_argument('-D', '--no-levenshtein-distance', dest='no_lev_dist',
                            help='do not run the Levenshtein distance test', action='store_true')
        parser.add_argument('-U', '--no-initial-unique', dest='no_init_uniq',
                            help='do not run the unique initial characters test',
                            action='store_true')
        parser.add_argument('-L', '--no-max-length', dest='no_max_length',
                            help='do not run the maximum length test', action='store_true')
        parser.add_argument('-o', '--output-file', type=str, dest='output',
                            help='logs all console output to an additional file')
        parser.add_argument('-a', '--ascii', dest='ascii',
                            help='turn off rich text formatting and progress bars for console \
  output', action='store_true')
        parser.add_argument('-q', '--quiet', dest='quiet',
                            help='do not display details of test failures, only whether they \
  succeeded or failed', action='store_true')
        parser.add_argument('--debug', dest='debug', action='store_true',
                            help='turn on debugging mode (intended for developers)')
        parser.add_argument('--pycharm-debug', dest='pycharm_debug', action='store_true',
                            help='re-raise exceptions out of main() to Pycharm (intended for developers)')
        parser.add_argument('-v', '--version', action='version',
                            version=version_str())

        args = parser.parse_args()

        # If there is an output file, then attempt to open it.
        if args.output:
            try:
                absout = abspath(args.output)
                if not args.quiet:
                    logdefault("Attempting to open log file {} for writing".format(absout))
                log_file = open(absout, 'w')
                setargs(log_file, args)
            except OSError as e:
                logerror("open {} for writing failed: {}".format(e.filename,
                                                                 e.strerror))
                abort(args.debug)
        else:
            setargs(None, args)

        # Now validate the parameters
        if args.lev_dist <= 0:
            logerror("Invalid value for --min-levenshtein-distance {}".format(
                args.lev_dist))
            abort(args.debug)
        if args.init_uniq <= 0:
            logerror("Invalid value for --min-initial-unique {}".format(
                args.init_uniq))
            abort(args.debug)
        if args.max_length <= 0:
            logerror("Invalid value for --max-length {}".format(
                args.max_length))
            abort(args.debug)

        try:
            if not args.quiet:
                logdefault("Reading wordlist file {}".format(args.input))
            with open(args.input) as f:
                bip39 = BIP39WordList(desc=f"{args.input}", handle=f)
                # word_line_arr = to_wordline_array(contents2list(s))
                # loginfo("{} words read".format(len(word_line_arr.word_list))
                loginfo("{} words read".format(len(bip39)))
        except OSError as e:
            logerror("Cannot read {}: {}".format(e.filename,
                                                 e.strerror))
            abort(args.debug)

        tally = 0
        total = 4

        def check_validity_warnings(validity):
            if not validity.is_sorted and not args.quiet:
                logwarning('Wordlist is not sorted. It is recommended to sort the wordlist \
  before publishing it.')
            if not validity.has_2048_words and not args.quiet:
                logwarning('Wordlist has {} words. Exactly 2048 words are needed to map \
  each word to an 11-bit value 1-to-1.'.format(validity.num_words))

        logdefault("Checking wordlist for invalid characters")
        try:
            tup = bip39._test_lowercase_1()
            kwargs = tup[3]
            kwargs = progressbar('Looking for invalid characters', tup[0],
                                 tup[1], tup[2], **kwargs)
            validity = bip39._test_lowercase_2(kwargs)
            check_validity_warnings(validity)
            tally += 1
            loginfo("Valid characters test succeeded")
        except InvalidWordList as e:
            check_validity_warnings(e)
            for l in e.err_lines:
                logerror("Word \"{}\" (line{}) has a non-lowercase character\
or is blank (Did you remove whitespace and empty lines?)".format(l.word, l.line))
            logerror("Valid characters test failed")
            logerror("Cannot perform additional test_vectors")
            abort(args.debug)

        logdefault("Finished checking wordlist for invalid characters")
        separator()

        if not args.no_lev_dist:
            logdefault("Performing Levenshtein distance test")
            try:
                tup = bip39._test_lev_distance_1(n=args.lev_dist)
                kwargs = tup[3]
                kwargs = progressbar('Computing Levenshtein distance', tup[0],
                                     tup[1], tup[2], **kwargs)
                bip39._test_lev_distance_2(kwargs)
                if not args.quiet:
                    loginfo("No word pairs with Levenshtein distance less than {}" \
                            .format(args.lev_dist))
                tally += 1
                loginfo("Levenshtein distance test succeeded")
            except ValidationFailed as e:
                if not args.quiet:
                    lev_dist = e.status_obj
                    word_pairs = lev_dist.getwordpairs_lt()
                    logerror("{} word pairs with Levenshtein distance less than {}\n" \
                             .format(len(word_pairs), args.lev_dist))
                    for i in range(1, args.lev_dist):
                        words_list = [*zip(lev_dist.getwordpairs_eq(i), lev_dist.getlinepairs_eq(i))]
                        logerror("{} word pairs with Levenshtein distance *equal* to {}:" \
                                 .format(len(words_list), i))
                        for words, lines in words_list:
                            logerror("    \"{}\" (line {}) <--> \"{}\" (line {})" \
                                    .format(words[0], lines[0], words[1], lines[1]))
                        logerror("")
                    logerror("{} total words below minimum Levenshtein distance".format(len(
                        word_pairs)))
                logerror("Levenshtein distance test failed")

            logdefault("Finished performing Levenshtein distance test")
            separator()

        if not args.no_init_uniq:
            logdefault("Performing unique initial characters test")
            try:
                tup = bip39._test_initial_chars_1(n=args.init_uniq)
                kwargs = tup[3]
                kwargs = progressbar('Checking initial characters', tup[0],
                                     tup[1], tup[2], **kwargs)
                bip39._test_initial_chars_2(kwargs)
                loginfo("All words are unique to {} initial characters".format(args.init_uniq))
                tally += 1
                loginfo("Unique initial characters test succeeded")
            except ValidationFailed as e:
                if not args.quiet:
                    similar = e.status_obj
                    # Filter out groups with just one word in them as those are unique
                    groups = {k: v for (k, v) in similar.similargroup_all().items() if
                              len(v) > 1}
                    logerror("{} groups of similar words (by {} initial characters)\n" \
                             .format(len(groups.items()), args.init_uniq))
                    for pre, group in groups:
                        logerror("Similar words with prefix \"{}\":").format(pre)
                        for wordline in group:
                            logerror("    \"{}\" (line {})".format(wordline[0], wordline[1]))
                        logerror("")
                    logerror("{} total similar words".format(len(groups.keys())))
                logerror("Unique initial characters test failed")
            logdefault("Finished unique initial characters test")
            separator()

        if not args.no_max_length:
            logdefault("Performing maximum word length test")
            try:
                tup = bip39._test_max_length_1(n=args.max_length)
                kwargs = tup[3]
                kwargs = progressbar('Checking length', tup[0],
                                     tup[1], tup[2], **kwargs)
                bip39._test_max_length_2(kwargs)
                loginfo("Length of all words are {} chracters or less".format(args.max_length))
                tally += 1
                loginfo("Maximum word length test succeeded")
            except ValidationFailed as e:
                if not args.quiet:
                    lengths = e.status_obj
                    words = lengths.getwords_gt()
                    lines = lengths.getlines_gt()
                    logerror("Words longer than {} characters:".format(args.max_length))
                    for word, line in [*zip(words, lines)]:
                        logerror("    \"{}\" (line {})", word, line)
                    logerror("{} words longer than {} characters".format(len(lengths),
                                                                         args.max_length))
                logerror("Maximum word length test failed")
            logdefault("Finished maximum word length test")
            separator()

        logdefault("{} of {} test_vectors passed".format(tally, total))
        exit(0)
    except Exception as e:
        print("Got unknown exception {}: {}".format(type(e), str(e)))
        if args.pycharm_debug:
            raise e
        else:
            abort(args.debug)


if __name__ == "__main__":
    main()
