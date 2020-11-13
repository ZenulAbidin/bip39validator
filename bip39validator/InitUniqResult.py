from .internal.validation_tests import regroup_prefix


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