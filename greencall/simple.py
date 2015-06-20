import asyncio
import aiohttp

import time

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
    #url = 'http://thepiratebay.se/search/{}/0/7/0'.format(query)
    url = query
    with (yield from sem):
        page = yield from get(url, compress = True)#, connector=connector)
    magnet = first_magnet(page)
    #magnet = page

    #with open('simple.txt', 'w') as outfile:
    #    outfile.write(magnet)
    #outfile.close()
    #print('{}: {}'.format(query, magnet))


distros = ["https://www.google.com/", "https://www.yahoo.com/",
        "http://www.cnn.com/", "http://www.msnbc.com/"]

#start = time.time()
#distros = ['archlinux', 'ubuntu', 'debian']
#distros = ['debian']
sem = asyncio.Semaphore(5)
loop = asyncio.get_event_loop()
#connector = aiohttp.TCPConnector(share_cookies=True, loop=loop)
f = asyncio.wait([print_magnet(d) for d in distros])
loop.run_until_complete(f)

#loop = asyncio.get_event_loop()

#tasks = [asyncio.async(print_magnet(d)) for d in distros]
    
#tasks = [
#    asyncio.async([print_magnet(d) for d in distros]),
#    asyncio.async(print_magnet(distros[1])),
#    asyncio.async(print_magnet(distros[2]))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

#loop = asyncio.get_event_loop()

#resp = yield from aiohttp.request('get', url, connector=connector)
#asyncio.Task([print_magnet(d) for d in distros])
#loop.close()

#print("\n\ntime completed: {}".format(time.time() - start))

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
