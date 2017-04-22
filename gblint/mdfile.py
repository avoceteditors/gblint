""" Module provides the MDFile class, which provides methods for
extracting data from Markdown files, including link and anchor
extraction."""
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

# Logger
from logging import getLogger
logger = getLogger()

# Markdown FIle Class
class MDFile():
    """ Class to convert Markdown files into Python data, and to
    process the given file data in printing reports to stdout."""

    # Initialize the Class
    def __init__(self, name, path, title):
        """ Initializes the class, loads data"""
        self.name = name
        self.path = path
        self.title = title
        self.bad_links = []
        self.has_errors = False

        logger.info("Reading File: %s" % name)
        self.read()


    # Read in File Data
    def read(self):
        """ Method reads in data from file """

        # Load File Contents
        f = open(self.path, 'r')
        contents = f.read()
        f.close()

        # Remove Code Samples
        contents = re.sub(" `.*?`", "", contents)

        # Separate Content into Paragraphs
        base_lines = contents.split('\n')
        lines = []
        for line in base_lines:
            if re.match("^[\s]*[\S]", line):
                lines.append(line)

        # Identify Headings and Links
        links = []
        headings = []
        for line in lines:
            if re.match("^#", line):
                headings.append(line)
            else:
                base_links = re.findall("\[.*?\]\(.*?\)", line)
                if base_links != []:
                    links += base_links

        # Parse Links
        if links != []:
            self.has_links = True
            self.parse_links(links)
        else:
            self.has_links = False


    # Parse Heading
    def parse_heading(self, heading):
        pass

    # Parse Links
    def parse_links(self, links):
        """ Method parses the given links, adding them to the relevant
        variables for later checks.  """
        logger.info("Parsing %s links" % len(links))
        self.links_internal = []
        self.links_local = []
        internal = ['internal-no-anchor', 'internal-with-anchor']
        for link in links:
            data = self.parse_link(link)
            typ = data['type']

            if typ in internal:
                self.links_internal.append(data)
            elif typ == 'local-with-anchor':
                self.links_local.append(data)

    # Parse Single Link
    def parse_link(self, link):
        """ Method parses the given link, extracting the relevant data
        from the text. """

        (title, href) = link.split("](")
        title = re.sub("^\[", "", title)
        href = re.sub("\)$", "", href)

        data = {
            "raw": link,
            "title": title,
            'anchor': None,
            'target': None,
            'type': None,
            "raw_href": href}

        if re.match("^http", href):
            data['type'] = 'external'
        elif re.match('^[\S]*?\.md$', href):
            data['type'] = 'internal-no-anchor'
            data['target'] = href
        elif re.match('^[\S]*?\.md\#[\S]*?$', href):
            data['type'] = 'internal-with-anchor'
            (href, anchor) = href.split('#')
            data['target'] = href
            data['anchor'] = anchor
        elif re.match("^\#[\S]*?$", href):
            data['type'] = 'local-with-anchor'
            data['target'] = self.name
            data['anchor'] = re.sub('^\#', '', href)
        elif re.match('^[\S]*?\.jpg$|^[\S]*?\.png$', href):
            data['type'] = 'image'
        elif re.match('^[\S]*?@[\S]*?\.[\S]*$', href):
            data['type'] = 'email'
        else:
            logger.debug("Unable to identify link: %s" % link)

        return data


    # Add Error to Records
    def add_error(self, link):
        """ Method appends the givne link to the error list
        of bad links. """
        self.bad_links.append(link)


    # Report Errors
    def report(self):
        """ Method prints errors on file to stdout. """

        print("ERRORS: ", self.name)
       
        # Report Errors
        for err in self.bad_links:
            print(" - ", err['raw'])
