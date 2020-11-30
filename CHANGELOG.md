# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.6] - 2020-11-30
### Fixed
- `bip39validator` crashing at startup with error `ModuleNotFoundError: No module named 'validators'`

## [1.0.5] - 2020-11-29
### Added
New method `InitUniqResult.groups_length(n)`

### Changed
- NFC normalization is now done on all words in wordlists after reading them

### Fixed
- `bip39validator` no longer printing erroneous test failures
- GIF in README.rst shows the expected output for the `bip39validator` command
- Plain text URLs as the first positional argument of `bip39validator` are now recognized, in addition to filenames
- Diacritics removal being silently ignored, causing non-english wordlists to fail lowercase characters test

## [1.0.4] - 2020-11-27
### Fixed
- Fixed some exceptions thrown when running the bip39validator main program.

## [1.0.3] - 2020-11-26
Purely metadata-related version bump to add a description to the bip39validator package on PyPI.

## [1.0.2] - 2020-11-26
### Fixed
- Fix MaxLengthResult bug where shorter words are not included in the result

## [1.0.1] - 2020-11-26
First stable version of BIP39 Validator.
### Fixed
- Significantly lower memory usage for Levenshtein distance test (about 200MB). However you still may experience up to 650MB memory usage if ran in a Jupyter Notebook.

## [1.0.0rc2] - 2020-11-06
Pre-release version of BIP39 Validator 1.0.0. Much more stable than 1.0.0rc1 and should run without errors.
### Added
- Unit tests created
- New documentation theme
### Fixed
- Setup.py now works and can be used to install bip39validator locally

## [1.0.0rc1] - 2020-10-01
Pre-release version of BIP39 Validator 1.0.0. Be warned that this is alpha-quality software and may not even run.
### Added
- Driver program created
- API and docstrings created
- reStructuredText documentation created
- Well-formed test implemented
- Levenshtein distance test implemented
- Initial unique characters test implemented
- Maximum length test implemented

[Unreleased]: https://github.com/ZenulAbidin/bip39validator/compare/v1.0.6...HEAD
[1.0.6]: https://github.com/ZenulAbidin/bip39validator/releases/tag/v1.0.6
[1.0.5]: https://github.com/ZenulAbidin/bip39validator/releases/tag/v1.0.5pypi4
[1.0.4]: https://github.com/ZenulAbidin/bip39validator/releases/tag/1.0.4
[1.0.3]: https://github.com/ZenulAbidin/bip39validator/releases/tag/1.0.3
[1.0.2]: https://github.com/ZenulAbidin/bip39validator/releases/tag/1.0.2
[1.0.1]: https://github.com/ZenulAbidin/bip39validator/releases/tag/1.0.1
[1.0.0rc2]: https://github.com/ZenulAbidin/bip39validator/releases/tag/v1.0.0rc2
[1.0.0rc1]: https://github.com/ZenulAbidin/bip39validator/releases/tag/v1.0.0rc1

