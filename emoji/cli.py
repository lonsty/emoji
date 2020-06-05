"""Console script for emoji."""
import sys
import click

from emoji.emoji import search_emoji_limited, search_emoji_first


@click.command()
@click.option('-f', '--first', is_flag=True, help='Print the first emoji without wrap in the results.')
@click.option('-l', '--limit', default=0, help='Limit the number of results.')
@click.argument('keywords', nargs=-1)
def main(keywords, limit, first):
    """Search emoji by keywords."""
    try:
        if first:
            emoji = search_emoji_first(keywords)
            print(emoji.emoji, end='')
        else:
            emoji = search_emoji_limited(keywords, limit)
            for e in emoji:
                print(e.emoji, '\t', e.desc)
    except Exception as err:
        print(err)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
