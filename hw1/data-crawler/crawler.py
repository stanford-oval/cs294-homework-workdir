# Copyright 2020 The Board of Trustees of the Leland Stanford Junior University
#
# Author: Silei Xu <silei@cs.stanford.edu>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import extruct
import requests
import json
import sys
import urllib.parse
import time
from bs4 import BeautifulSoup

base_url = 'https://www.yelp.com/'
target_size = 1000


def crawl(initial, url_pattern, schema_pattern, output, interval=0):
    """
    navigate through pages

    :param initial: the initial url to start crawling
    :param url_pattern: the pattern of the urls you are looking for
    :param schema_pattern: the pattern of the json-ld containing the schema.org data
    :param output: the list of schema.org extracted from each page
    :param interval: seconds to time between visiting each page (to avoid being banned)
    :return: None
    """
    queue = [initial]
    visited = set()

    while len(queue) > 0 and len(output) < target_size:
        # get one url from the queue
        current = queue.pop()

        # if the url has been visited, skip
        if current in visited:
            continue

        # otherwise, start getting information from the url
        print(f'Extract schema.org data from page: {current}')
        response = requests.get(current)

        # extract the schema.org data
        extracted = extract(response.text, response.url, schema_pattern)
        if extracted is not None:
            output.append(extracted)

        # mark the current page to be visited
        visited.add(current)

        # find unvisited links in the current page and add to the queue
        add_urls(queue, response.text, url_pattern, visited)

        # wait to avoid being banned by the website
        time.sleep(interval)


def extract(html, url, schema_pattern):
    """
    extract schema.org information of a given page

    :param html: html text of the page
    :param url: the url to the page
    :param schema_pattern: the pattern of the json-ld containing the schema.org data
    :return: an object containing the desired schema.org markup from the page
    """
    data = extruct.extract(html, base_url=url, syntaxes=['json-ld'])
    for schema in data['json-ld']:
        if schema_pattern(schema):
            return schema
    return None


def add_urls(queue, html, url_pattern, visited):
    """
    Add unvisited urls that match the pattern to queue

    :param queue: the url queue to be added
    :param html: the html text of the page
    :param url_pattern: the pattern of the urls you are looking for
    :param visited: a set of visited urls
    :return: None
    """
    # parse the current page
    soup = BeautifulSoup(html, 'html5lib')

    # find all links that matches the patterns
    for link in soup.find_all('a'):
        if 'href' not in link.attrs:
            continue
        url = urllib.parse.urljoin(base_url, link['href'])
        if url in visited:
            continue

        # if the url found matches the given pattern, add it to the queue
        if url_pattern(url):
            queue.insert(0, url.split('?')[0])


def main():
    output = []
    try:
        init_url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=stanford'
        crawl(
            init_url,
            lambda url: url.startswith('https://www.yelp.com/biz/'),
            lambda obj: obj['@type'] == 'Restaurant',
            output
        )
    finally:
        with open('./yelp.json', 'w') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
