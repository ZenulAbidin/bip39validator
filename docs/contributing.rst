.. include:: ../CONTRIBUTING.rst
   :start-after: begin_contributing_md
   :end-before:  contributing_md

Debugging Tips
----------------------------------------------------------------------------------------

The ``--debug`` option enables a global exception catcher which invokes pdb when an
exception is about to break out of `main()` for post-mortem debugging. This is an
advanced feature intended for developers only, and you need to be familiar with pdb
commands in order to use this feature effectively. This blog post "`Pdb debugging tips <https://dev.to/zenulabidin/pdb-debugging-tips-2ki7>`_"
lists the most essential pdb commands.

``bip39validator`` includes an option ``--pycharm-debug``. This turns off the global
exception catcher and lets runaway exceptions get caught by Pycharm's debug mode. Despite
its name, it works with other IDEs as well. Use this option if your IDE offers a better
debugging experience than command-line pdb.