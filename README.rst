BIP39 Validator
========================================================================================
|docs| |gh_actions| |pyversions| |bitcointalk|

.. |docs| image:: https://readthedocs.org/projects/bip39validator/badge/?version=latest
    :target: http://bip39validator.readthedocs.org/en/latest/?badge=latest
    :alt: Docs

.. |gh_actions| image:: https://github.com/ZenulAbidin/bip39validator/workflows/tests/badge.svg?
     :target: https://github.com/ZenulAbidin/bip39validator/actions?workflow=tests
   :alt: Github Actions Build Status

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/bip39validator.svg
    :target: https://pypi.org/project/bip39validator/

.. |bitcointalk| image:: https://img.shields.io/badge/bitcointalk-thread-yellow
   :target: https://bitcointalk.org/index.php
   :alt: Bitcointalk thread

.. image:: https://files.notatether.com/bip39validator.gif
  :width: 600
  :alt: bip39validator sample run

|

.. begin_brief_description

BIP39 Validator is a small program for checking BIP39 wordlists for Latin languages.
It supports checking wordlists for semantic errors and implements three different tests:

- A minimum Levenshtein distance test
- A minimum unique prefix length
- A maximum length test

It also has a Python API for running each test programmatically and interactively
exploring the results.

.. end_brief_description

- `View Demo on Google Colab <https://colab.research.google.com/drive/1nJQl25XhjtUNzF3MY_MdH0AotwgdlwOz?usp=sharing>`_
- `Documentation <https://bip39validator.readthedocs.io>`_

.. contents:: Contents
   :local:
   :backlinks: none


Description
----------------------------------------------------------------------------------------

.. begin_long_description

BIP39 Validator checks that wordlists use the `best practices`_ written
in the BIP39 standard. These checks are ones that maintainers frequently ask
submitters for compliance before merging the wordlist. By using this tool, you
avoid having to manually verify the technical rules of the list.

Note that there is no support for validating with rules such as "Words cannot
sound too similar" or "Wordlists cannot contain words from any other languages'
wordslists". There is also no support for wordlists in non-Latin languages such
as Arabic, Hebrew or CJK languages.


.. _best practices: `https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md`

.. end_long_description

Installing
----------------------------------------------------------------------------------------

.. begin_installing

You can install BIP39 Validator either from PyPI or directly from source on Github.

To install from PyPI:

.. code-block:: sh

   pip3 install bip39validator

Alternatively, to install BIP39 Validator from source, head over to the Releases page,
and download the version you want to install. Unzip the package, change into the newly
created directory and then run:

.. code-block:: sh

   python3 setup.py install

.. end_installing

Running
----------------------------------------------------------------------------------------

.. begin_running

You invoke BIP39 Validator like this:

.. code-block:: sh

   bip39validator [OPTIONS] {INPUT_FILE | URL_OF_TEXT_FILE}

One, and only one of INPUT_FILE and URL_OF_TEXT_FILE should be specified, where INPUT_FILE
is a file in your local filesystem, while URL_OF_TEXT_FILE is an HTTP or HTTPS URL pointing
to the wordlist file with a mimetype of text/plain. In both cases, the input must be a plain
text file.

BIP39 Validator displays rich formatted status messages as it progresses with validation,
however it is also possible to run BIP39 Validator with minimum diagnostic messages, or
to log status messages to a file. The complete list of command-line arguments is below:

.. list-table:: Command-line options
   :widths: 15 30
   :header-rows: 1

   * - Option
     - Description
   * - -d, --min-levenshtein-distance
     - set the minimum required Levenshtein distance between words (default: 2)
   * - -u, --min-initial-unique
     - set the minimum required unique initial characters between words (default: 4)
   * - -l, --max-length
     - set the maximum length of each word (default: 8)
   * - -D, --no-levenshtein-distance
     - do not run the Levenshtein distance test
   * - -U, --no-initial-unique
     - do not run the unique initial characters test
   * - -L, --no-max-length
     - do not run the maximum length test
   * - -o <FILE>, --output-file <FILE>
     - log all console output to an additional file
   * - -a, --ascii
     - turn off rich text formatting and progress bars for console output
   * - -q, --quiet
     - do not display details of test failures, only whether they succeeded or failed
   * - -v, --version
     - print the version number and exit

BIP39 Validator displays which validation tests succeeded and the total number of tests
that succeeded.

.. end_running

Using the API
----------------------------------------------------------------------------------------

.. begin_using_api

BIP39 Validator comes with a powerful API for querying the result of validation tests.
The most basic class provided is `BIP39WordList`. It is responsible for creating a word
list object from a file, string buffer or even a URL. `BIP39WordList` objects are *immutable*
and words can't be changed, added or removed from the object one they are loaded. To alter
the wordlist, you'd need to change it on file and then create a `BIP39WordList` from it again.

When a test fails, it throws a `ValidationFailed` exception. This contains a member called
`status_obj` that contains a class with diagnostic information about the test that threw the
exception. This object is also returned by the validation test if it succceeds, but the reason
there are two different ways to capture the test state is because it's most common for users
to look at the state only if a test fails.

.. end_using_api

API Examples
----------------------------------------------------------------------------------------

.. begin_examples

Here are some of the anticipated uses of the BIP39 Validator API.

- Validate that Levenshtein distances >= 2, then find all the word pairs with Levenshtein
  distance less than 2:

.. code-block:: python

   from bip39validator import BIP39WordList, InvalidWordList, ValidationFailed

   f = open('wordlist-en.txt')
   try:
     wordlist = BIP39Wordlist('English wordlist', handle=f)
     wordlist.test_lev_distance(2)
     # At this point, no word pairs have Levenshtein distance < 2.
   except ValidationFailed as e:
     dists = e.status_obj.getwordpairs_lt(2)
     for wordpair in dists:
       word1 = wordpair[0]
       word2 = wordpair[1]
       # Do something with word1 and word2...
   except InvalidWordList as e:
     print("Wordlist file is not well-formed")

- Validate that Levenshtein distances >= 2, then calculate the number and percentage
  of word pairs with Levenshtein distance less than 2 (assume 2048-word list):

.. code-block:: python

   from bip39validator import BIP39WordList, InvalidWordList, ValidationFailed

   f = open('wordlist-en.txt')
   try:
     wordlist = BIP39Wordlist('English wordlist', handle=f)
     wordlist.test_lev_distance(2)
     # At this point, the percentage and number of
     # words fulfilling the condition are 0.
   except ValidationFailed as e:
     dists = e.status_obj.getwordpairs_lt(2)
     n = len(dists)
     prct = n/(2048*2048)
   except InvalidWordList as e:
     print("Wordlist file is not well-formed")

- Validate that words are unique in at least 4 initial characters, then find all
  the words beginning with "str" (prefix-3 group "str"):

.. code-block:: python

   from bip39validator import BIP39WordList, InvalidWordList, ValidationFailed

   f = open('wordlist-en.txt')
   try:
     wordlist = BIP39Wordlist('English wordlist', handle=f)
     wordlist.test_initial_chars(4)
     # At this point, all words are unique in at least 4 initial characters
   except ValidationFailed as e:
     words = e.status_obj.similar_wordgroup("str")
     for word in words:
       # Do something with word...
   except InvalidWordList as e:
     print("Wordlist file is not well-formed")

- Validate that words are unique in at least 4 initial characters, then calculate
  the number and percentage of word prefix-4 groups with at least two words in them:

.. code-block:: python

   from bip39validator import BIP39WordList, InvalidWordList, ValidationFailed

   f = open('wordlist-en.txt')
   try:
     wordlist = BIP39Wordlist('English wordlist', handle=f)
     wordlist.test_initial_chars(4)
     # At this point, the percentage and number of
     # words fulfilling the condition are 0.
   except ValidationFailed as e:
     groups = e.status_obj.similar_wordgroup_all(4)
     n = sum([c for c in groups.values() if len(c) >= 2])
     denom = len(groups.values())
     perc = n/denom
   except InvalidWordList as e:
     print("Wordlist file is not well-formed")

- Validate that words are no longer than 8 characters, then find all of the
  words longer than 8 characters:

.. code-block:: python

   from bip39validator import BIP39WordList, InvalidWordList, ValidationFailed

   f = open('wordlist-en.txt')
   try:
     wordlist = BIP39Wordlist('English wordlist', handle=f)
     wordlist.test_max_length(8)
     # At this point, all words are no longer than 8 characters
   except ValidationFailed as e:
     words = e.status_obj.getwords_gt(8)
     lines = e.status_obj.getlines_gt(8)
     for word, line in [*zip(words, lines)]:
       # Do something with word and line...
   except InvalidWordList as e:
     print("Wordlist file is not well-formed")

- Validate that words are no longer than 8 characters, then calculate
  the number and percentage of words longer than 8 characters:

.. code-block:: python

   from bip39validator import BIP39WordList, InvalidWordList, ValidationFailed

   f = open('wordlist-en.txt')
   try:
     wordlist = BIP39Wordlist('English wordlist', handle=f)
     wordlist.test_max_length(8)
     # At this point, the percentage and number of
     # words fulfilling the condition are 0.
   except ValidationFailed as e:
     words = e.status_obj.getwords_gt(8)
     n = sum([w for w in words if len(w) > 8])
     perc = n/len(words)
   except InvalidWordList as e:
     print("Wordlist file is not well-formed")

.. end_examples

Local Development
----------------------------------------------------------------------------------------

.. begin_local_development

First, clone the `master` branch of this repository, and then make a new virtualenv:

.. code-block:: sh

   python3 -m venv env-bip39validator
   source env-bip39validator/bin/activate

Then install the module dependencies using:

.. code-block:: sh

   pip3 install -r requirements.txt -r dev-requirements.txt

.. end_local_development

Contributing
----------------------------------------------------------------------------------------

See CONTRIBUTING.md for details on how to contribute issues and pull requests to this project.

License
----------------------------------------------------------------------------------------

.. begin_license

BIP39 Validator is provided under the MIT license that can be found in the LICENSE_
file. By using, distributing, or contributing to this project, you agree to the
terms and conditions of this license.

.. _LICENSE: https://github.com/ZenulAbidin/bip39validator/blob/master/LICENSE

.. end_license
