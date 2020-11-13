class ValidationFailed(Exception):
    """One of the validation test_vectors has failed.

  Exception raised by methods in ``BIP39WordList``. This
  class is not meant to be created directly.
  """

    def __init__(self, status_obj=None):
        self.status_obj = status_obj