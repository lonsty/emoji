"""Main module."""
import random
import time
from collections import namedtuple
from functools import wraps
from typing import List, Iterable
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

SEARCH_API = 'https://emojipedia.org/search/?q={k}'
TIMEOUT = 10
Emoji = namedtuple('Emoji', 'emoji desc')
NOT_FOUND = Emoji('😞', 'No results found')


def retry(exceptions, tries=3, delay=1, backoff=2, logger=None):
    """
    Retry calling the decorated function using an exponential backoff.
    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay or random.uniform(0.5, 1.5)
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    if logger:
                        logger.warning('{}, Retrying in {} seconds...'.format(e, mdelay))
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry


@retry(Exception)
def search_emoji(keywords: Iterable) -> List[Emoji]:
    """
    Search emoji by keywords.

    :param keywords: Iterable, keywords to search.
    :return: list, list of Emoji.
    """
    assert keywords, "ValueError: keyword must be provided for search."
    keywords = quote(' '.join(keywords))

    try:
        response = requests.get(SEARCH_API.format(k=keywords), timeout=TIMEOUT)
    except Exception:
        raise

    if response.status_code != 200:
        return [NOT_FOUND]

    soup = BeautifulSoup(response.text, 'html.parser')
    # emoji = [s.text for s in soup.find(class_='search-results').find_all('span')]
    emoji = [Emoji(a.text.split(' ')[0], ' '.join(a.text.split(' ')[1:]))
             for a in soup.find(class_='search-results').find_all('a')]
    if len(emoji) == 1 and emoji[0].emoji == 'random':
        return [NOT_FOUND]
    return emoji


def search_emoji_limited(keywords: Iterable, limit: int) -> List[Emoji]:
    """
    Get limited emoji from search result.

    :param keywords: Iterable, search keywords.
    :param limit: int, result limit numbers.
    :return: list, list of Emoji.
    """
    emoji = search_emoji(keywords)
    if emoji:
        if limit == 0:
            return emoji
        return emoji[:limit]
    return [NOT_FOUND]


def search_emoji_first(keywords: Iterable) -> Emoji:
    """
    Get the first emoji from result.

    :param keywords: Iterable, search keywords.
    :return: a Emoji.
    """
    emoji = search_emoji(keywords)
    if emoji:
        return emoji[0]
    return NOT_FOUND
