from io import TextIOWrapper

import requests

from .internal.util import contents2list, is_all_lower, to_wordline_array
from .internal.validation_tests import validate_sanitized_preamble, validate_sanitized, \
    validate_levenshtein_distance_preamble, validate_levenshtein_distance, \
    validate_uniq_chars_preamble, validate_uniq_chars, validate_length_preamble, \
    validate_length
from .InvalidRemoteContent import InvalidRemoteContent
from .InvalidWordList import InvalidWordList
from .ValidWordList import ValidWordList
from .ValidationFailed import ValidationFailed
from .LevDistResult import LevDistResult
from .InitUniqResult import InitUniqResult
from .MaxLengthResult import MaxLengthResult

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