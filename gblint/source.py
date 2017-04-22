# Copyright (c) 2017, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the name of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import re
from os import listdir

# Logger
from logging import getLogger
logger = getLogger()


# Build Souce List
def build_source(sourcedir, contents = "SUMMARY.md"):
    """ Function generates a source list of Markdown files
    found in the given directory.  If it finds the contents
    file, which defaults to SUMMARY.md, it automatically
    excludes it from the output."""

    logger.info("Build file list from source directory")

    base = listdir(sourcedir)

    # Exclude contents and Non-Markdown files
    md = []
    has_contents = False
    for i in base:
        if re.match("^.*?\.md$", i) and i != contents:
            md.append(i)
        elif i == contents:
            has_contents = True
            logger.info("Found %s" % contents)

    return has_contents, contents, md

# Parse Line
def parse_line(line):
    """ Function parses a line from SUMMARY.md, extracting
    relevant data"""

    # Find Indentation Level
    count = 0
    for c in line:
        if re.match('\s', c):
            count += 1
        else:
            break

    base = re.split("^[\s]*\* ", line)[1]
    (title, href) = base.split('](')
    title = re.sub('^\[', '', title)
    href = re.sub('\)[\s\S]*$', '', href)

    return count, title, href

# Generate List
def gen_list(contents):
    """ Function takes the contents of a SUMMARY.md file,
    then converts it into a list of Entry class instances."""

    base_empties = contents.split('\n')
    base = []
    for i in base_empties:
        if re.match('^[\s]*\* ', i):
            base.append(i)

    # Loop over Lines
    skip_level = None
    data = {}
    for i in base:
        (indent, title, href) = parse_line(i)

        if href in data:
            logger.warning("Duplication Error: %s" % "[%s](%s)" % (title, href))
            skip_level = indent
        else:
            if skip_level is None or skip_level == indent:
                skip_level = None
                data[href] = (indent, title, href)
            else:
                logger.warning("- Child of Duplicate: %s" % "[%s](%s)" % (title, href))

    return data



# Find Orphans
def find_orphans(contents, filelist):
    """ Function loops through filelist to identify files that
    exist in the source directory but are not called by the build
    process to generate HTML"""

    orphans = []
    bad_target = []
    newcon = {}
    for i in filelist:
        if i not in contents:
            logger.warning("Orphaned File: %s" % i)
            orphans.append(i)
        else:
            try:
                newcon[i] = contents[i]
            except:
                logger.warning("Nonexistent Entry in SUMMARY.md: %s" % i)

    logger.info("Found %s orphaned files" % len(orphans))

    return newcon


# Parse SUMMARY.md
def parse_summary(path, filelist):
    """ Function parses SUMMARY.md, the contents file for
    GitBook, then returns a list of files that build from
    it.  It logs errors for double entries."""

    # Fetch Contents from SUMMARY.md
    f = open(path, 'r')
    contents = f.read()
    f.close()

    # Generate List
    base = gen_list(contents)

    # Find Orphans
    contents = find_orphans(base, filelist)

    # Return Summary Base
    return contents 


