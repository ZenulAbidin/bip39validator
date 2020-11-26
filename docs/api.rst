API
========================================================================================

.. include:: ../README.rst
   :start-after: begin_using_api
   :end-before:  end_using_api

Classes
-----------------------------------------------------------------------------------------

The most basic class of the BIP39 Validator API is ``BIP39WordList``. This class is
responsible for loading the wordlist from an input sorce, such as the local disk or
network, and running the multiple validation tests on it. It also stores the line numbers
of the words, to enable cross-referencing results with the original file.

Once you instantiate an instance of a ``BIP39WordList`` class, there are two different
types of operations that can be done. The first group collects metadata about the wordlist,
retrieving the words themselves, their line numbers, and also the number of words it has.
The second group is the validation tests themselves.

Each validation test is exposed as a ``BIP39WordList`` method. They are:

- ``test_lowercase()``, to perform the well-formed test
- ``test_lev_distance(n)``, to perform the Levenshtein distance test
- ``test_initial_chars(n)``, to perform the initial unique characters test
- ``test_max_length(n)``, to perform the maximum length test

``test_lowercase()`` returns a ``ValidWordList`` class on success and throws an
``InvalidWordList`` exception on failure. The others return a unique class with the
results (``LevDistResult``, ``InitUniqResult``, and ``MaxLengthResult`` respectively)
and throw the respective class on failure. The reason for this is so that the same
result object can be explored whethe the test succeeded or failed.

Except for ``test_lowercase()`` itself, all tests run ``test_lowercase()`` before
running their own tests to ensure that the wordlist is well-formed.

API Reference
-----------------------------------------------------------------------------------------

.. module:: bip39validator

.. automodule:: bip39validator.BIP39WordList
   :members:

.. automodule:: bip39validator.ValidWordList
   :members:

.. automodule:: bip39validator.LevDistResult
   :members:

.. automodule:: bip39validator.InitUniqResult
   :members:

.. automodule:: bip39validator.MaxLengthResult
   :members:

Exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoexception:: bip39validator.InvalidWordList
   :inherited-members:

.. autoexception:: bip39validator.InvalidRemoteContent
   :inherited-members:

.. autoexception:: bip39validator.ValidationFailed
   :inherited-members:
