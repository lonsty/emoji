"""Main module."""
import random
import threading
import time
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, wait
from functools import wraps
from typing import Iterable, List
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

SEARCH_API = 'https://emojipedia.org/search/?q={keywords}'
EMOJI_DETAIL_API = 'https://emojipedia.org/emoji/{emoji}'
TIMEOUT = 10
Emoji = namedtuple('Emoji', 'emoji shortcodes desc')
NOT_FOUND = Emoji('😞', ':disappointed:', 'No results found')
thread_local = threading.local()


def get_session():
    """
    Get the same requests Session in the same thread.

    :return: Session, session object.
    """
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


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


@retry(ConnectionError)
def request_to_beautifulsoup(url: str) -> BeautifulSoup:
    """
    Request a url, then load it's html text to BeautifulSoup.

    :param url: str, url to request.
    :return: BeautifulSoup object.
    """

    session = get_session()
    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except Exception as e:
        raise ConnectionError(e)

    try:
        return BeautifulSoup(response.text, 'html.parser')
    except:
        raise ValueError('Response html text can not be converted to a <BeautifulSoup>.')


def search_emoji(keywords: Iterable) -> List[Emoji]:
    """
    Search emoji by keywords.

    :param keywords: Iterable, keywords to search.
    :return: list, list of Emoji.
    """
    assert keywords, "ValueError: keyword must be provided for search."
    keywords = quote(' '.join(keywords))
    soup = request_to_beautifulsoup(SEARCH_API.format(keywords=keywords))
    emoji = [Emoji(emoji=a.text.split(' ')[0],
                   desc=' '.join(a.text.split(' ')[1:]),
                   shortcodes=None)
             for a in soup.find(class_='search-results').find_all('a')]
    if len(emoji) == 1 and emoji[0].emoji == 'random':
        return [NOT_FOUND]
    return emoji


def search_emoji_limited(keywords: Iterable, limit: int = 0) -> List[Emoji]:
    """
    Get limited emoji from search result.

    :param keywords: Iterable, search keywords.
    :param limit: int, result limit numbers.
    :return: list, list of Emoji.
    """
    emoji = search_emoji(keywords)
    if emoji:
        if limit:
            selected_emoji = emoji[:limit]
        else:
            selected_emoji = emoji
        return get_multi_emoji_shortcodes(selected_emoji)
    return [NOT_FOUND]


def search_emoji_by_index(keywords: Iterable, index: int = 1, shortcodes: bool = False) -> Emoji:
    """
    Get the first emoji from result.

    :param keywords: Iterable, search keywords.
    :return: a Emoji.
    """
    emoji = search_emoji(keywords)
    if emoji and len(emoji) >= index:
        if shortcodes:
            return get_emoji_shortcodes(emoji[index - 1])
        return emoji[index - 1]
    return NOT_FOUND


def get_emoji_shortcodes(emoji: Emoji) -> Emoji:
    """
    Get the shortcodes of a emoji if it has, by call a API.

    :param emoji: Emoji, emoji object.
    :return: A new or original emoji object.
    """
    soup = request_to_beautifulsoup(url=EMOJI_DETAIL_API.format(emoji=quote(emoji.emoji)))
    row = soup.find('table', class_='emoji-detail').find('td', text='Shortcodes')
    if row:
        return Emoji(emoji=emoji.emoji, desc=emoji.desc,
                     shortcodes=row.find_next_sibling().text)
    return emoji


def get_multi_emoji_shortcodes(emoji: List[Emoji]) -> List[Emoji]:
    """
    Use thread pool to get all shortcodes in once.

    :param emoji: List, list of emoji object.
    :return: List, list of processed emoji object.
    """
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(get_emoji_shortcodes, e): e for e in emoji}
        wait(futures)

    emojis = []
    for future in futures:
        try:
            emj = future.result()
        except Exception as e:
            print(e)
        else:
            emojis.append(emj)

    return emojis


def maxlen(emoji: List[Emoji], attr: str) -> int:
    """
    Max value length of a emoji attribute.

    :param emoji: list, list of Emoji.
    :param attr: a Emoji attribute.
    :return: max length of this attribute value.
    """
    return max([len(eval(f'e.{attr}') or '') for e in emoji])


def pretty_print(emoji: List[Emoji]):
    """
    Print all emoji information as table.

    :param emoji: List, list of emoji object.
    :return: None
    """
    title = ['Index', 'Emoji', 'Shortcodes', 'Description']
    maxlens = [len(title[0]), max(maxlen(emoji, "emoji"), len(title[1])),
               max(maxlen(emoji, "shortcodes"), len(title[2]))]

    print(f'{title[0]}  {title[1].ljust(maxlens[1])}\t{title[2].ljust(maxlens[2])}  {title[3]}')
    for i, e in enumerate(emoji):
        print(f'{(str(i + 1)).center(maxlens[0])}  '
              f'{e.emoji}\t'
              f'{(e.shortcodes or "").ljust(maxlens[2])}  '
              f'{e.desc}')
