countdown_game
==============

A program to create and solve the countdown numbers game.

    usage: countdown_numbers.py [-h] (--choose N N | --numbers N [N ...])
                                [--target TARGET] [--relaxed]

    Plays the Countdown numbers game

    optional arguments:
      -h, --help            show this help message and exit
      --choose N N, -c N N  Number of cards to choose. First the number of low
                            cards. Second is the number of high cards. Total cards
                            chosen must be equal to 6 unless --relaxed is
                            specified. There are a maximum of 4 high cards and 20
                            low cards to choose from.
      --numbers N [N ...], -n N [N ...]
                            Specify cards to use. Number of cards must be 6,
                            unless --relaxed is specified.
      --target TARGET, -t TARGET
                            Must be a number between 100 and 999 unless --relaxed
                            is specified.
      --relaxed, -r         Relaxes the problem constraints so the problem doesn't
                            have to exactly match the Countdown numbers game. That
                            is, have exactly 6 cards and a target between 100 and
                            999.

Compatible with both Python 2 and Python 3, though it runs slightly faster in Python 2.
