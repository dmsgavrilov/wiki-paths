import time
from collections import deque

import requests

from bs4 import BeautifulSoup

import storage


def find_shortest_path(start, end):
    '''
    Breadth-first search approach for shortest path between two Wikipedia pages.
    path is a dict of page (key): list of links from start to page (value).
    Q is a double-ended queue of pages to visit.
    '''
    path = {}
    path[start] = [start]
    Q = deque([start])

    while len(Q) != 0:
        page = Q.popleft()
        links = get_links(page)
        for link in links:
            if link in end:
                return path[page] + [link]
            if (link not in path) and (link != page):
                path[link] = path[page] + [link]
                Q.append(link)
    return None


def get_links(page):
    '''
    Retrieves distinct links in a Wikipedia page.
    '''
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    base_url = page[:page.find('/wiki/')]
    links = list({base_url + a['href'] for a in soup.select('p a[href]') if a['href'].startswith('/wiki/')})
    return links


def check_pages(start, end):
    '''
    Checks that "start" and "end "are valid Wikipedia pages of the same language.
    Valid also means that "start" is not a dead-end page (the script would return no path anyways) and that "end" is not an orphan page.
    '''
    languages = []
    for page in [start, end]:
        try:
            ind = page.find('.wikipedia.org/wiki/')
            languages.append(page[(ind-2):ind])
            requests.get(page)
        except:
            err = '{} does not appear to be a valid Wikipedia page.'.format(page)
            return False, err

    if len(set(languages)) > 1:
        err = 'Pages are in different languages.'
        return False, err

    if len(get_links(start)) == 0:
        err = 'Start page is a dead-end page with no Wikipedia links.'
        return False, err

    end_soup = BeautifulSoup(requests.get(end).content, 'html.parser')
    if end_soup.find('table', {'class': 'metadata plainlinks ambox ambox-style ambox-Orphan'}):
        err = 'End page is an orphan page with no Wikipedia pages linking to it.'
        return False, err
    return True, None


def redirected(end):
    '''
    Returns the url that end page points to (helpful for end pages with redirected url)
    '''
    end_soup = BeautifulSoup(requests.get(end).content, 'html.parser')
    title = end_soup.find('h1').text
    title = title.replace(' ', '_', len(title))
    base_url = end[:end.find('/wiki/') + len('/wiki/')]
    return set([end, base_url + title])


def result(start, end, path):
    '''
    Returns json object of shortest path result.
    '''
    if path:
        result = path
    else:
        result = "No path"
    d = {"start": start, "end": end, "steps": len(result) if result != "No path" else 0, "path": result}
    return d


def find_path(start, end):
    start_time = time.time()
    status, err = check_pages(start, end)
    if status:
        path = find_shortest_path(start, redirected(end))
        dict_result = result(start, end, path)
        end_time = time.time()
        dict_result["time"] = round((end_time - start_time), 2)
        dict_result["error"] = None
        res = dict_result
    else:
        res = {
            "start": start,
            "end": end,
            "steps": None,
            "path": None,
            "error": err
        }
    storage.write([res])

# print(find_path("https://en.wikipedia.org/wiki/Borat", "https://en.wikipedia.org/wiki/Larry Charles"))
