#!/usr/bin/env python
# -----------------------------------------------------------------------------
#                               Libraries
# -----------------------------------------------------------------------------
import os
import argparse
import inspect

try: 
    from secrets import choice
except ImportError:
    from random import SystemRandom


# -----------------------------------------------------------------------------
#                               Functions
# -----------------------------------------------------------------------------
# Phasphrase generator
# -----------------------------------------------------------------------------
def generatePassphrase(wordlist: set, n_words: int= 7, separator: str= ' ') -> str:
    assert n_words > 0, 'Number of words in the passphrase must be greiter than 0'
    try:
        return separator.join(choice(wordlist) for _ in range(n_words))
    except NameError:
        return separator.join(SystemRandom().sample(wordlist, n_words))


# -----------------------------------------------------------------------------
# Wordlist
# -----------------------------------------------------------------------------
def buildWordList(filepaths: list[str]) -> list[str]:
    words = set()
    for filepath in filepaths:
        with open(filepath, 'r') as f:
            words = words.union([line.rstrip('\n') for line in f])
    return list(words)


# -----------------------------------------------------------------------------
#                                 Main
# -----------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(prog= 'Passphrase generator', 
                                     description= 'Generate np passphrases of lenght nw using EFF dice wordlists',
                                     epilog= 'Eduardo Castro, 2023')
    # Passphrase parameters
    parser.add_argument(
        '-nw', 
        '--n_words', 
        nargs= '?', 
        default= 7, 
        type= int,
        help= 'Number of words in the passphrases'
    )
    parser.add_argument(
        '-np', 
        '--n_passphrases', 
        nargs= '?', 
        default= 1, 
        type= int,
        help= 'Number of passphrases to generate'
    )
    parser.add_argument(
        '-sep', 
        '--separator', 
        nargs= '?', 
        default= ' ', 
        type= str,
        help= 'Passphrase word separator of passphrases to generate'
    )

    # Wordlist selection
    parser.add_argument(
        '-l', 
        '--large', 
        action= 'store_const', 
        const= 'eff_large_wordlist.txt',
        help= 'Use EFF general large wordlist')
    parser.add_argument(
        '-s1', 
        '--short1', 
        action= 'store_const', 
        const= 'eff_short_wordlist_1.txt',
        help= 'Use EFF general short wordlist')
    parser.add_argument(
        '-s2', 
        '--short2', 
        action= 'store_const', 
        const= 'eff_short_wordlist_2.txt',
        help= 'Use EFF short wordlist with unique prefixes')
    args = vars(parser.parse_args())

    # Verificate number of passphrases
    assert args['n_passphrases'] > 0, 'Number of passphrases must be greiter than 0'
    # Get usable wordlists filepaths
    usable_wordlists = [args[y] for y in ['large', 'short1', 'short2'] if args[y]]
    # Default. Use EFF Short 1
    if not usable_wordlists:
        usable_wordlists.append('eff_short_wordlist_1.txt')
    
    # Build paths
    wordlists_dirpath = os.path.join(
        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
        'wordlists'
    )
    wordlists_filepaths = [os.path.join(wordlists_dirpath, x) for x in usable_wordlists]

    wordlist = buildWordList(wordlists_filepaths)
    [print(generatePassphrase(wordlist= wordlist, 
                             n_words= args['n_words'], 
                             separator= args['separator']))
     for _ in range(args['n_passphrases'])]

if __name__ == '__main__':
    main()