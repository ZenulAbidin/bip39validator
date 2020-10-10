Running
========================================================================================

.. include:: ../README.rst
   :start-after: begin_running
   :end-before:  end_running

Description of validation tests
-----------------------------------------------------------------------------------------

Currently, four validation tests are implemented. Each of these will be explained in
detail below.

Lowercase words test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This test ensures that all words in the wordlist are composed of lowercase latin words,
with no diacritics, and that there is strictly one word on each line, with no intermediate
whitespace except for any of the representations of newline ("\r\n" on Windows, "\n" on
macOS and Linux).

This test also searches for problems in the wordlist that are severe but not fatal. The
presence of these problems will not hamper the other validation tests but the code reviewers
will not merge wordlists that have these warnings. Currently the warnings are 1) wordlist
is not sorted, and 2) wordlist doesn't have exactly 2048 words. Please ensure these
requirements are met before submitting a pull request.

This test is mandatory, because all the other tests depend on the wordlist being well-formed.
Validation cannot continue if this test fails and signals that the medium the wordlist was
loaded from has syntax errors that need to be fixed.

A side-effect of requiring only lowercase latin words is that it cannot validate non-Latin
languages' wordlists. Support for non-Latin languages might be added in the future, but
currently it is not a priority.

Levenshtein distance test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This validation checks that every pair of words in the wordlist has a Levenshtein distance
above a threshold. [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance)
is the number of insertions, removals, and substitutions (replacing one letter with another)
you need to make in a word to transform it into another word. It's used to determine how
easily mistakable two words are.

A rule of thumb is, the higher the Levenshtein distance, the less likely users will confuse
two words with each other. BIP39 wordlist mergers recommend a Levenshtein distance between
all words of at least **2**.

For example, to transform "cat" into "catch", you need to add two characters at the end,
"c" and "h", so that the word transforms to "cat" --> "catc" --> "catch" so the Levenshtein
distance between these two words is 2. But the distance between "cat" and "oatmeal" is 5:

- Replace "c" with "o"
- Add "m" "e" "a" "l" at the end

Here's a slightly more complex example. To transform "research" into "searching", you need
to:

- Remove the letters "r" and "e" at the beginning
- Add the letters "i" "n" "g" at the end

So, the Levenshtein distance between these words is 5.


Initial unique characters test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This validation checks that the prefixes of all words in the wordlist are unique up to a
threshold number of characters. In other words, it checks that the word can be uniquely
identified by it's first N characters. BIP39 wordlist mergers recommend a value of N
(unique initial characters length) of at most **4**.

The bigger the threshold, the longer the prefixes become which may allow groups of words
to be completely identical prefixes, making it harder for them to distinguish each other.
Also, certain wallet software like Electrum try to autocomplete words, the more similar
initial characters two words have, the less effective the autocomplete becomes.

For example, the wordlist

::
   tree
   inkling
   train
   quail
   tasty

has an initial unique character length of 3, as the first three characters in each word
can uniquely identify it in each wordlist.


Maximum length test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This validation checks that the string length all words are no longer than a threshold
number of characters. As some hardware wallets only display the first eight characters
of a word, BIP39 wordlist mergers recommend all words be no longer than **8** characters.


