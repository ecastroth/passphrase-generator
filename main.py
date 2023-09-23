#!/usr/bin/env python
# -----------------------------------------------------------------------------
#                               Libraries
# -----------------------------------------------------------------------------
import os
import argparse
import inspect
from urllib import request

try: 
    from secrets import choice
except ImportError:
    from random import SystemRandom

# Localname : url
local_wordlists_dirpath = os.path.join(
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
    'wordlists'
)
local_url_dict = {'large' : {'local': os.path.join(local_wordlists_dirpath, 'EFF_Large_wordlist.txt'),
                             'url': 'https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt'},
                  'short1': {'local': os.path.join(local_wordlists_dirpath, 'EFF_Short1_wordlist.txt'),
                             'url': 'https://eff.org/files/2016/09/08/eff_short_wordlist_1.txt'},
                  'short2': {'local': os.path.join(local_wordlists_dirpath, 'EFF_Short2_wordlist.txt'), 
                             'url': 'https://eff.org/files/2016/09/08/eff_short_wordlist_2_0.txt'}}

# -----------------------------------------------------------------------------
#                               Functions
# -----------------------------------------------------------------------------
# Parser creator
# -----------------------------------------------------------------------------
def createParser() -> argparse.ArgumentParser:
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
        const= 'large',
        help= 'Use EFF general large wordlist')
    parser.add_argument(
        '-s1', 
        '--short1', 
        action= 'store_const', 
        const= 'short1',
        help= 'Use EFF general short wordlist')
    parser.add_argument(
        '-s2', 
        '--short2', 
        action= 'store_const', 
        const= 'short2',
        help= 'Use EFF short wordlist with unique prefixes')
    return parser


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
def buildWordList(wordlist_names: list[str]) -> list[str]:
    words = set()
    for name in wordlist_names:
        # File exists
        if os.path.exists(local_url_dict[name]['local']):
            # Read local file
            with open(local_url_dict[name]['local'], 'r') as f:
                filewords = [line.rstrip('\n') for line in f]

        # File does not exists
        else:
            # Read wordlist from EFF webpage
            filewords = downloadWordlist(name)
        words = words.union(filewords)
        print(len(words))
    return list(words)


def downloadWordlist(name: str) -> list[str]:
    # Read txt
    response = request.urlopen(local_url_dict[name]['url'])
    decoded_response = response.read().decode()
    # Get words
    filewords = [x.split('\t')[1] for x in decoded_response.split('\n')[:-1]]
    # Make localdir if not exists
    if not os.path.exists(local_wordlists_dirpath):
        os.makedirs(local_wordlists_dirpath)
    # Save local
    with open(local_url_dict[name]['local'], 'w') as f:
        f.write('\n'.join(filewords))
    return filewords


# -----------------------------------------------------------------------------
#                                 Main
# -----------------------------------------------------------------------------
def main() -> None:
    parser = createParser()
    args = vars(parser.parse_args())

    # Verificate number of passphrases
    assert args['n_passphrases'] > 0, 'Number of passphrases must be greiter than 0'

    # Get usable wordlists filepaths
    usable_wordlists_names = [args[y] for y in local_url_dict.keys() if args[y]]
    # Default. Use EFF Short1 wordlist
    if not usable_wordlists_names:
        usable_wordlists_names.append('short1')
    
    wordlist = buildWordList(usable_wordlists_names)
    [print(generatePassphrase(wordlist= wordlist, 
                             n_words= args['n_words'], 
                             separator= args['separator']))
     for _ in range(args['n_passphrases'])]

if __name__ == '__main__':
    main()