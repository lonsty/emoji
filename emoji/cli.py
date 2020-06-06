"""Console script for emoji."""
import sys

import click

from emoji.emoji import (pretty_print, search_emoji_by_index,
                         search_emoji_limited)


@click.command()
@click.option('-a', '--all', 'all_emoji', is_flag=True, help='All emojis from the results.')
@click.option('-c', '--shortcodes', is_flag=True, help='Return the emoji shortcodes instead of unicode.')
@click.option('-i', '--index', default=0, help='The index th (1 is the 1st) emoji of the results.')
@click.option('-l', '--limit', default=0, help='Emojis from limited number of the results.')
@click.argument('keywords', nargs=-1)
def main(keywords, all_emoji, shortcodes, index, limit):
    """Search emoji by keywords."""
    try:
        if all_emoji or limit:
            if all_emoji:
                emoji = search_emoji_limited(keywords=keywords)
            else:
                emoji = search_emoji_limited(keywords=keywords,
                                             limit=limit)
            pretty_print(emoji)
        else:
            if index:
                emoji = search_emoji_by_index(keywords=keywords,
                                              index=index,
                                              shortcodes=shortcodes)
            else:
                emoji = search_emoji_by_index(keywords=keywords,
                                              index=1,
                                              shortcodes=shortcodes)
            print(emoji.shortcodes or emoji.emoji if shortcodes else emoji.emoji)
    except Exception as err:
        print(err)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
