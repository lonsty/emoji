=====
Usage
=====

* Search all emoji about `sparkle` in a terminal:

.. code-block:: console

    $ emoji sparkle -a

    Index  Emoji	Shortcodes         Description
      1    ❇️	:sparkle:          Sparkle
      2    ✨	:sparkles:         Sparkles
      3    💖	:sparkling_heart:  Sparkling Heart
      4    🍾	                   Bottle with Popping Cork
      5    🌟	:star2:            Glowing Star
      6    🎇	:sparkler:         Sparkler
      7    🗡️	                   Dagger
      8    💫	:dizzy:            Dizzy
      9    🥂	                   Clinking Glasses
      10   🔮	:crystal_ball:     Crystal Ball
      11   💎	:gem:              Gem Stone
      12   ⭐	:star:             Star
      13   🌠	:stars:            Shooting Star


* Get the first emoji of the searching results:

.. code-block:: console

    $ emoji sparkle

    ❇️


* Get the nth emoji by index of the searching results:

.. code-block:: console

    $ emoji sparkle -i 2

    ✨


* Splice emoji to a git commit message:

.. code-block:: console

    $ git commit -m "`emoji rocket` initial commit"
    $ git commit -m "`emoji memo` update documnets ..."
    $ git commit -m "`emoji bug` bug fix ..."
    $ git commit -m "`emoji sparkles -i 2` new feature ..."
    $ git commit -m "`emoji racehorse` performance ..."
    $ git commit -m "`emoji bookmark` version tag ..."
    $ git commit -m "`emoji hammer` refactor code ..."
    $ git commit -m "`emoji beacon` tests ..."
    $ git commit -m "`emoji shirt` style ..."
    $ git commit -m "`emoji fire` removing code/files ..."
    $ git commit -m "`emoji gear` configuration ..."
    $ git commit -m "`emoji wrench` build ..."
    $ git commit -m "`emoji whale` docker ..."

    🚀 initial commit
    📝 update documnets ...
    🐛 bug fix ...
    ✨ new feature ...
    🐎 performance ...
    🔖 version tag ...
    🔨 refactor code ...
    🚨 tests ...
    👕 style ...
    🔥 removing code/files ...
    👷 ci ...
    🔧 build ...
    🐋 docker ...


* Get more usage by typing `emoji --help` in your terminal:


.. code-block:: console

    $ emoji --help


.. code-block:: none

    Usage: emoji [OPTIONS] [KEYWORDS]...

      Search emoji by keywords.

    Options:
      -a, --all            All emoji from the results.
      -c, --shortcodes     Return the emoji shortcodes instead of unicode.
      -i, --index INTEGER  The index th (1 is the 1st) emoji of the results.
      -l, --limit INTEGER  Emoji from limited number of the results.
      --help               Show this message and exit.
