"""Console script for emoji."""
import sys
import click

from emoji.emoji import search_emoji_limited, search_emoji_by_index


@click.command()
@click.option('-a', '--all', 'all_emoji', is_flag=True, help='All emoji from results.')
@click.option('-i', '--index', default=0, help='The index th (1 is the 1st) emoji of results.')
@click.option('-l', '--limit', default=0, help='Emoji from limited number of results.')
@click.argument('keywords', nargs=-1)
def main(keywords, all_emoji, index, limit):
    """Search emoji by keywords."""
    try:
        if all_emoji or limit:
            if all_emoji:
                emoji = search_emoji_limited(keywords=keywords)
            else:
                emoji = search_emoji_limited(keywords=keywords, limit=limit)
            for i, e in enumerate(emoji):
                print(f'{e.emoji}\t{("#" + str(i + 1)).rjust(3)} - {e.desc}')
        else:
            if index:
                emoji = search_emoji_by_index(keywords=keywords, index=index)
            else:
                emoji = search_emoji_by_index(keywords=keywords, index=1)
            print(emoji.emoji, end='\n')
    except Exception as err:
        print(err)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
