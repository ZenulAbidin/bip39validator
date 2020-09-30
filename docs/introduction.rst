Introduction
========================================================================================

Why the need for a utility that validates BIP39 wordlists? To see why an automated
verification system is needed, it's necessary to understand how wordlists are presently
merged into the BIP39 spec.

As easly as 2014, people have submitted several word lists as pull requests. More often
than not, the merging process stalled, because none of the [Bitcoin organization members
on Github](https://github.com/orgs/bitcoin/people) (authors) approved it for merging.
Sometimes it is because a handful of words are too similar to each other, and no progress
was made since then. 

Wordlists have 2048 words in them. Going through each of those words to check them is
a very tedious process, and automated verification for some of the tests helps to avoid
trivial errors in the word request that could cause authors to request you to fix first.

BIP39 Validator has one goal: to become *the* standard way to check wordlists for quality
before merging into the official BIP tree. For wordlist submitters to use it before submitting
a pull request, and for authors to use it to ensure that submitters have done basic checks
on their wordlist first.

The current version, (1.0.0) is a pilot to test whether this tool will gain traction in the
Bitcoin community. It includes checks for three different tests: Levenshtein distances,
initial unique characters and maximum length. If it succeeds, additional tests might be
implemented in the future, such as checking for similarity to words in other languages'
word lists (this can be done using ``googletrans`` and ``NLTK``), and checking for offensive
or bad words.
