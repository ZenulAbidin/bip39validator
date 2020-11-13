class InvalidRemoteContent(Exception):
    """URL has an unexpected content type

  Exception raised by the ``BIP39WordList`` constructor.
  This class is not meant to be created directly.
  """

    """The offending URL"""
    url = None

    """The content type of ``url``"""
    content_type = None

    """The expected content type of ``url``"""
    expected_content_type = None

    def __init__(self, url, content_type, expected_content_type):
        self.url = url
        self.content_type = content_type
        self.expected_content_type = expected_content_type