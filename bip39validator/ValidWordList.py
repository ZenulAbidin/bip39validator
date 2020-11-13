class ValidWordList:
    """The wordlist is well-formed and has no invalid characters.

  Data structure returned by ``BIP39WordList.test_lowercase()``.
  This class is not meant to be created directly.
  """

    """Indicates if the wordlist file has invalid chracters in it.
  Any character that isn't lowercase ASCII is an invalid character.
  This member is always False.
  """
    has_invalid_chars = False

    """Tuple of line contents and line numbers of invalid words."""
    err_lines = None

    """Indicates if the wordlist file is in sorted order."""
    is_sorted = None

    """Indicates if the wordlist has exactly 2048 words."""
    has_2048_words = None

    """The number of words in the wordlist."""
    num_words = None

    def __init__(self, **kwargs):
        self.is_sorted = kwargs['is_sorted']
        self.err_lines = kwargs['err_lines']
        self.has_2048_words = kwargs['length_exact']
        self.num_words = kwargs['length']