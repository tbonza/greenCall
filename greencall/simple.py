import asyncio
import aiohttp

"""
@asyncio.coroutine
def print_page(url):
    response = yield from aiohttp.request('GET',url)
    body = yield from response.read_and_close(decode=True)
    print(body)

loop = asyncio.get_event_loop()
#loop.run_until_complete(print_page('http://example.com'))

loop.run_until_complete(asyncio.wait([print_page('http://example.com/foo'),
                                      print_page('http://example.com/bar')
                                      ]))
# instead of .wait, use .as_completed, returns coroutines in the order that
# they're completed
"""

""" See Below for Basic Example """

@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    # may not want to decode API responses
    return (yield from response.read_and_close(decode=False))

def first_magnet(page):
    """ Parses output returned from aiohttp.request """
    #soup = bs4.BeautifulSoup(page)
    #a = soup.find('a', title='Download this torrent using magnet')
    #return a['href']
    return page

@asyncio.coroutine
def print_magnet(query):
    url = 'http://thepiratebay.se/search/{}/0/7/0'.format(query)
    with (yield from sem):
        page = yield from get(url, compress = True)
    magnet = first_magnet(page)
    print('{}: {}'.format(query, magnet))

distros = ['archlinux', 'ubuntu', 'debian']
sem = asyncio.Semaphore(5)
loop = asyncio.get_event_loop()
f = asyncio.wait([print_magnet(d) for d in distros])
loop.run_until_complete(f)

# crawler example is recursively adding tasks & using semaphores
# so they don't hit the server too hard. We might be able to add
# tasks to speed up the process but I'm not sure yet.
#
# let's modify this example to hit the yelp client and get some
# basic times. Let's then try to improve those times. After this evening
# you'll have to worry about writing to the database & writing the
# google search client.
#
# let's make little to no assumptions for now about handling the
# csv file since you know it's relatively clean.



