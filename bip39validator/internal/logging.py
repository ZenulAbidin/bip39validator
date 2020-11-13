# BIP39 Wordlist Validator - A tool to validate BIP39 wordlists in Latin languages.
# bip39validator/logging.py: Console and file logging facilities
# Copyright 2020 Ali Sherief
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track


# These functions are not intended for use outside the main program.

# Utility function to print an error message
def logerror(*args):
    if not ascii:
        error_console.print(*["[bold red]ERROR: [/bold red]" + s for s in args])
    else:
        print(*["ERROR: " + s for s in args], sep="\n", file=sys.stderr)

    if log_file:
        print(*["ERROR: " + s for s in args], sep="\n", file=log_file)


# Utility function to print a warning message
def logwarning(*args):
    if not ascii:
        error_console.print(*["[bold yellow]WARNING: [/bold yellow]" + s for s
                              in args], sep="\n")
    else:
        print(*["WARNING: " + s for s in args], sep="\n", file=sys.stderr)

    if log_file:
        print(*["WARNING: " + s for s in args], sep="\n", file=log_file)


# Utility function to print an informational message
def loginfo(*args):
    if not ascii:
        info_console.print(*["[green]INFO: [/green]" + s for s in args], sep="\n")
    else:
        print(*["INFO: " + s for s in args], sep="\n", file=sys.stdout)

    if log_file:
        print(*["INFO: " + s for s in args], sep="\n", file=log_file)


# Utility function to print a normal default message
def logdefault(*args):
    if not ascii:
        info_console.print(*args, sep="\n")
    else:
        print(*args, sep="\n", file=sys.stdout)

    if log_file:
        print(*args, sep="\n", file=log_file)


# Utility function to print a progress bar that repeatedly calls a worker
# function that takes it's own `kwargs` and returns its updated `kwargs` for
# the next iteration.
def progressbar(desc, low, high, func, **kwargs):
    if not ascii:
        for i in track(range(low, high), description=desc):
            kwargs = func(i, **kwargs)
        return kwargs
    else:
        print(desc + ", please wait...")
        for i in range(low, high):
            kwargs = func(i, **kwargs)
        return kwargs


def separator():
    if not ascii:
        info_console.print(Markdown('---'))
    else:
        print("=" * 10, file=sys.stdout)

    if log_file:
        print("=" * 10, file=log_file)

log_file = None
ascii = False

def setargs(log, args):
    log_file = log
    ascii = args.ascii


if not ascii:
    error_console = Console(file=sys.stderr)
    info_console = Console(file=sys.stdout)
