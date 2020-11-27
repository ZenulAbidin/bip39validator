from .internal.util import is_all_lower


class LevDistResult:
    """Levenshtein distances between each word pair.

  Data structure returned or raised by ``BIP39WordList.test_lev_distance()``.
  This class is not meant to be created directly.
  """

    """Test conducted with a minimum Levenshtien distance of ``threshold``."""
    threshold = None

    def __init__(self, res, words_sorted, lines_sorted, threshold):
        lev, split = res
        self.split = split
        self.words_sorted = words_sorted
        self.lines_sorted = lines_sorted
        self.threshold = threshold

    def __len__(self):
        return len(self.split)

    def _index_pair(self, first, second):
        return (first, second)

    def _word_pair(self, first, second):
        return (self.words_sorted[first], self.words_sorted[second])

    def _line_pair(self, first, second):
        return (self.lines_sorted[first], self.lines_sorted[second])

    def getwordpairs_eq(self, dist=None):
        """Gets the word pairs which have a Levenshtein distance of ``dist``

  :param dist: Levenshtein distance
  :type dist: int
  :returns: a list of word pairs
  """
        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split == dist:
                pairs.append(self._word_pair(first, second))
        return pairs

    def getlinepairs_eq(self, dist=None):
        """Gets the line numbers of pairs which have a Levenshtein distance of ``dist``

          :param dist: Levenshtein distance
          :type dist: int
          :returns: a list of line pairs
          """

        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split == dist:
                pairs.append(self._line_pair(first, second))
        return pairs

    def getwordpairs_lt(self, dist=None):
        """Gets the word pairs which have a Levenshtein distance less than ``dist``

          :param dist: Levenshtein distance
          :type dist: int
          :returns: a list of word pairs
          """

        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split < dist:
                pairs.append(self._word_pair(first, second))
        return pairs

    def getlinepairs_lt(self, dist=None):
        """Gets the line numbers of pairs which have a Levenshtein distance less than ``dist``

          :param dist: Levenshtein distance
          :type dist: int
          :returns: a list of line number pairs
          """

        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split < dist:
                pairs.append(self._line_pair(first, second))
        return pairs

    def getwordpairs_gt(self, dist=None):
        """Gets the word pairs which have a Levenshtein distance greater than ``dist``

  :param dist: Levenshtein distance
  :type dist: int
  :returns: a list of word pairs"""

        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split > dist:
                pairs.append(self._word_pair(first, second))
        return pairs

    def getlinepairs_gt(self, dist=None):
        """Gets the line numbers of pairs which have a Levenshtein distance greater than ``dist``

  :param dist: Levenshtein distance
  :type dist: int
  :returns: a list of line number pairs"""

        if not dist:
            dist = self.threshold
        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        pairs = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split > dist:
                pairs.append(self._line_pair(first, second))
        return pairs


    def getwordpairs_list(self, dists):
        """Gets the word pairs which have a Levenshtein distance inside the list ``dists``

      :param dists: list of Levenshtein distances
      :type dists: list
      :returns: a list of word pairs"""
        assert type(dists) == list, 'Invalid type "{}" for argument `dists` (expected "list")' \
            .format(type(dists).__name__)
        assert len(dists) > 0, "Cannot use empty list as list of dists"

        pairs = []
        for i in range(0, len(dists)):
            assert type(dists[i]) == int, 'Invalid type "{}" for list element of `dists` (expected "int")' \
                .format(type(dists[i]).__name__)
            assert dists[i] > 0, "Distance must be greater than 0"

        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split in dists:
                pairs.append(self._word_pair(first, second))
        return pairs

    def getlinepairs_list(self, dists):
        """Gets the line numbers of pairs which have a Levenshtein distance inside the list ``dists``

      :param dists: list of Levenshtein distances
      :type dists: list
      :returns: a list of line number pairs"""
        assert type(dists) == list, 'Invalid type "{}" for argument `dists` (expected "list")' \
            .format(type(dists).__name__)
        assert len(dists) > 0, "Cannot use empty list as list of dists"

        pairs = []
        for i in range(0, len(dists)):
            assert type(dists[i]) == int, 'Invalid type "{}" for list element of `dists` (expected "int")' \
                .format(type(dists[i]).__name__)
            assert dists[i] > 0, "Distance must be greater than 0"

        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split in dists:
                pairs.append(self._line_pair(first, second))
        return pairs

    def getdist(self, word1, word2):
        """Gets Levenshtein distance between ``word1`` and ``word2``

      :param word1: first word
      :type word1: str
      :param word2: second word
      :type word2: str
      :returns: Levenshtein distance between ``word1`` and ``word2``"""
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

        dist = None
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if self.words_sorted[first] == word1 and self.words_sorted[second] == word2:
                dist = dist_split
                break
        if not dist:
            raise KeyError("word pair \"{}\" and \"{}\" not found".format(word1,
                                                                          word2))
        else:
            return dist


    def getdist_all(self, word):
        """Gets Levenshtein distance between `word` and all other words

  :param word: the word
  :type word: str
  :returns: list of Levenshtein distances between ``word`` and each word"""
        assert type(word) == str, 'Invalid type "{}" for argument `word` (expected "str")' \
            .format(type(word).__name__)
        assert len(word) > 0, "Cannot use empty string as word"
        assert is_all_lower(word), 'Word "{}" is not all ASCII lowercase'.format(word)

        dist_all = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            correct_idx = None
            if self.words_sorted[first] == word:
                correct_idx = first
                other_idx = second
            elif self.words_sorted[second] == word:
                correct_idx = second
                other_idx = first
            if correct_idx != None:
                dist_all.append((self._word_pair(other_idx, correct_idx),
                                 self._line_pair(other_idx, correct_idx), dist_split))
        if not dist_all:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all

    def getdist_all_eq(self, word, dist=None):
        """Gets Levenshtein distance between ``word`` and all other words, equal to ``dist``

      :param word: the word
      :type word: str
      :param dist: Levenshtein distance
      :type dist: int
      :returns: list of Levenshtein distances between ``word`` and each word"""
        if not dist:
            dist = self.threshold
        assert type(word) == str, 'Invalid type "{}" for argument `word` (expected "str")' \
            .format(type(word).__name__)
        assert len(word) > 0, "Cannot use empty string as word"
        assert is_all_lower(word), 'Word "{}" is not all ASCII lowercase'.format(word)

        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        dist_all = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split == dist:
                correct_idx = None
                if self.words_sorted[first] == word:
                    correct_idx = first
                    other_idx = second
                elif self.words_sorted[second] == word:
                    correct_idx = second
                    other_idx = first
                if correct_idx != None:
                    dist_all.append((self._word_pair(other_idx, correct_idx),
                                     self._line_pair(other_idx, correct_idx), dist_split))
        if not dist_all:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all

    def getdist_all_lt(self, word, dist=None):
        """Gets Levenshtein distance between ``word`` and all other words, less than ``dist``

          :param word: the word
          :type word: str
          :param dist: Levenshtein distance
          :type dist: int
          :returns: list of Levenshtein distances between ``word`` and each word"""
        if not dist:
            dist = self.threshold
        assert type(word) == str, 'Invalid type "{}" for argument `word` (expected "str")' \
            .format(type(word).__name__)
        assert len(word) > 0, "Cannot use empty string as word"
        assert is_all_lower(word), 'Word "{}" is not all ASCII lowercase'.format(word)

        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        dist_all = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split < dist:
                correct_idx = None
                if self.words_sorted[first] == word:
                    correct_idx = first
                    other_idx = second
                elif self.words_sorted[second] == word:
                    correct_idx = second
                    other_idx = first
                if correct_idx != None:
                    dist_all.append((self._word_pair(other_idx, correct_idx),
                                     self._line_pair(other_idx, correct_idx), dist_split))
        if not dist_all:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all

    def getdist_all_gt(self, word, dist=None):
        """Gets Levenshtein distance between ``word`` and all other words, greater than ``dist``

          :param word: the word
          :type word: str
          :param dist: Levenshtein distance
          :type dist: int
          :returns: list of Levenshtein distances between ``word`` and each word"""
        if not dist:
            dist = self.threshold
        assert type(word) == str, 'Invalid type "{}" for argument `word` (expected "str")' \
            .format(type(word).__name__)
        assert len(word) > 0, "Cannot use empty string as word"
        assert is_all_lower(word), 'Word "{}" is not all ASCII lowercase'.format(word)

        assert type(dist) == int, 'Invalid type "{}" for argument `dist` (expected "int")' \
            .format(type(dist).__name__)
        assert dist > 0, 'Distance must be greater than 0'

        dist_all = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split > dist:
                correct_idx = None
                if self.words_sorted[first] == word:
                    correct_idx = first
                    other_idx = second
                elif self.words_sorted[second] == word:
                    correct_idx = second
                    other_idx = first
                if correct_idx != None:
                    dist_all.append((self._word_pair(other_idx, correct_idx),
                                     self._line_pair(other_idx, correct_idx), dist_split))
        if not dist_all:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all

    def getdist_all_list(self, word, dists):
        """Gets Levenshtein distance between ``word`` and all other words, inside the list ``dists``

          :param word: the word
          :type word: str
          :param dists: list of Levenshtein distances
          :type dists: list
          :returns: list of Levenshtein distances between ``word`` and each word"""
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

        dist_all = []
        for node in self.split:
            data = node.split(',')
            dist_split = int(data[0])
            first = int(data[1])
            second = int(data[2])
            if dist_split in dists:
                correct_idx = None
                if self.words_sorted[first] == word:
                    correct_idx = first
                    other_idx = second
                elif self.words_sorted[second] == word:
                    correct_idx = second
                    other_idx = first
                if correct_idx != None:
                    dist_all.append((self._word_pair(other_idx, correct_idx),
                                     self._line_pair(other_idx, correct_idx), dist_split))
        if not dist_all:
            raise KeyError("word \"{}\" not found".format(word))
        else:
            return dist_all
