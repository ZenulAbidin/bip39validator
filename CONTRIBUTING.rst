.. begin_contributing_md

Contributing
========================================================================================

Thank you for your interest in this project! Please refer to the following sections on
how to contribute code and bug reports.

Reporting bugs
----------------------------------------------------------------------------------------

At the moment, this project is run in the spare time of a single person
(`Ali Sherief <https://zenulabidin.github.io>`_) with very limited resources for
issue tracker tickets. Thus, before submitting a question or bug report, please take a
moment of your time and ensure that your issue isn't already discussed in the project
documentation elsewhere on this site.

Assuming that you have identified a previously unknown problem or an important question,
it's essential that you submit a self-contained and minimal piece of code that
reproduces the problem. In other words: no external dependencies, isolate the
function(s) that cause breakage, submit matched and complete Python snippets that can be
easily run on my end.

Pull requests
----------------------------------------------------------------------------------------
Contributions are submitted, reviewed, and accepted using Github pull requests. Please
refer to `this article <https://help.github.com/articles/using-pull-requests>`_ for
details and adhere to the following rules to make the process as smooth as possible:

- Make a new branch for every feature you're working on.
- Make small and clean pull requests that are easy to review but make sure they do add
  value by themselves.
- Make sure you have tested any new functionality (e.g. if you made a new test).

  - Unit tests can be run using ``python -m unittest discover src/tests/`` to ensure that
    your patch doesn't break existing functionality.
- This project has a strong focus on providing general solutions using a minimal amount
  of code, thus small pull requests are greatly preferred.
- Read the remainder of this document, adhering to the documentation requirements.
- If making a purely documentation PR, please prefix the commit with ``[docs]``
- Ensure that you make a pull request to the **develop** branch, not to master.

  - E.g. ``[docs] Adding documentation for class X.``

.. end_contributing_md
