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