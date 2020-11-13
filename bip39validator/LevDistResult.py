from .internal.util import is_all_lower


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