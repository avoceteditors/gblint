# GBLint

GBLint provides basic linting and link testing support for Markdown files used with the GitBook static site generator.


## Installation

To install, run the following command:

```
$ python setup.py install --user
```

GBLint development targets Python versions 3.5 and later.  It *should* work with earlier versions of 3.x and with 2.7, but we make no guarantees.  Additionally, while we do attempt to provide cross-platform support, we are only using it on Linux, FreeBSD and Mac OS X.  We are currently unable to test it on Windows systems.

## Usage

GBLint iterates over Markdown files in a given directory.  It logs various errors and then prints a report of these errors to standard output.  For instance, say in your current working directory your GitBook project resides in the `source/` directory.  To lint the project, you would run the following command:

```
$ gblint source/
GBLint: A Linter for GitBook Markdown - version 0.1

ERRORS: example.md
 - [Example](nonexistent-file.md)

Operation completed in 0.0 seconds
```

To view logging information, you can also pass the `-v` option.  That is,

```
$ gblint -v source/
```



