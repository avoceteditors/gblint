from distutils.core import setup
from os.path import join

setup(name = 'gblint',
    version = "0.1",
    description = "Checks GitBook projects for bad links",
    author = "Kenneth P. J. Dyer",
    author_email = "kenneth@avoceteditors.com",
    url = "https://github.com/avoceteditors/gblint",
    packages = ['gblint'],
    scripts = [
        join('scripts', 'gblint')
        ]
    )
