""" Module contains all core functions for utility """
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
import logging
from datetime import datetime
from sys import exit as sys_exit
from os.path import isdir, join

from .source import build_source, parse_summary
from .mdfile import MDFile

# Globals
name = "GBLint"
slogan = "A Linter for GitBook Markdown"
version = "0.1"
author = "Kenneth P. J. Dyer"
email = "kenneth@avoceteditors.com"
company = "Avocet Editorial Consultants"

# Logger
logger = None
timer_start = 0


# Exit
def exit(exit_code=0, msg="Closing GBLint"):
    """ Function to exit GBLint"""

    # Log Exit
    if exit_code > 0:
        logger.critical(msg)
    else:
        logger.info(msg)

    # Calculate Runtime
    timer_diff = datetime.now() - timer_start
    sec = round(timer_diff.total_seconds(), 2)
    op_msg = "\nOperation completed in %s seconds" % sec
    print(op_msg)

    # Exit
    sys_exit(exit_code)


# Run Main Process
def run(args):
    """ This function runs the main process for GBLint"""
    global timer_start
    global logger

    # Initialize Timer
    timer_start = datetime.now()

    if args.verbose:
        content = [
                "%s: %s" % (name, slogan),
                "%s <%s>" % (author, email),
                company,
                "Version %s\n" % version]
        masthead = '\n  '.join(content)

        loglevel = logging.INFO
    else:
        masthead = "%s: %s - version %s" % (name, slogan, version)

        loglevel = logging.CRITICAL

    print(masthead)

    # Configure Logging
    logging.basicConfig(level=loglevel,
                        format="%(levelname)s: %(message)s")

    logger = logging.getLogger()

    # Check Source
    if not isdir(args.source):
        exit(2, "The source argument must be a directory")

    # Fetch Source Files
    (hasSum, summary, source) = build_source(args.source)

    if not hasSum:
        exit(1, "Unable to locate %s file" % summary)

    contents = parse_summary(join(args.source, summary), source)

    # Generate Data
    data = {}
    for href, info in contents.items():
        title = info[1]

        data[href] = MDFile(href, join(args.source, href), title)

    # Check Links
    for key, entry in data.items():

        if entry.has_links:
            for link in entry.links_internal:
                if link['target'] not in data:
                    logger.warning("Bad Internal Link: %s"
                                   % link['target'])
                    entry.add_error(link)

    # Report Bad Links
    for key, entry in data.items():
        if entry.bad_links != []:
            entry.report()
    # Exit
    exit()
