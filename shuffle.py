"""
Turns a list of 256-bit hashes into a randomly shuffled (yet
deterministic and verifiable) deck of cards.

A game server can get random nonces from players and send a hash
commitment of its own nonce along with the players' cards, and then
after the game ends, the server can reveal its nonce and the prior
game can be verified as having used the correct deck.  (Note that
this reveals all cards to all players, which may be useful even after
the game ends in games like poker.)

Doctest examples:

>>> hashes = ["86b827732d3812061fa1e9baaba82b232fa741a04557fa07225dc2b889bb694a"]
>>> get_shuffled_deck(hashes)
['4c', 'Qd', '4h', '2s', '3s', 'Ks', '5d', 'Js', 'Jh', '4s', '7d', '2c', 'Tc', '9c', 'Jd', 'Ts', 'Kh', '2h', '8c', '7s', '6c', '6s', '6d', 'Jc', 'Th', '8d', '5c', '7c', '6h', '8h', 'Ah', 'Ad', 'Ac', '7h', 'As', 'Td', 'Qs', '9h', '3c', '3h', '3d', 'Kc', 'Qc', 'Qh', '5s', '4d', '9d', '2d', 'Kd', '9s', '8s', '5h']
>>> hashes.append("b6e6985a7c03adf19aa9636b3c748000edd5f9f7363906b8211722acfc44026e")
>>> get_shuffled_deck(hashes)
['2s', 'Ah', '5h', 'Td', '5d', 'Qd', '3c', '3h', '4h', 'Jd', '8s', '6s', 'Jh', '7d', '7s', 'Kh', '3d', '2c', 'Ad', '9c', 'Ts', 'Js', 'Kd', '2d', 'Tc', '3s', '9h', '8d', '4d', 'Qs', 'Ks', '6d', '7c', 'Kc', '5c', 'Jc', '7h', 'Ac', '5s', '2h', '9s', '4s', '6c', 'As', '6h', '4c', '9d', 'Qc', 'Qh', 'Th', '8c', '8h']
"""

from __future__ import print_function
import sys
from math import floor
from hashlib import sha256, sha512
from binascii import hexlify, unhexlify

unopened_deck = [ \
"As","2s","3s","4s","5s","6s","7s","8s","9s","Ts","Js","Qs","Ks",
"Ah","2h","3h","4h","5h","6h","7h","8h","9h","Th","Jh","Qh","Kh",
"Kd","Qd","Jd","Td","9d","8d","7d","6d","5d","4d","3d","2d","Ad",
"Kc","Qc","Jc","Tc","9c","8c","7c","6c","5c","4c","3c","2c","Ac"]

def hashint(d,h):
    while True:
        if int(h,16) > (int(floor(float(((2**256)/1.0)/d))) * d):
            h = hexlify(sha256(unhexlify(h) + 
                        sha512(unhexlify(h)).digest()).digest())
        else:
            break
    o = int(h,16) % d
    h = hexlify(sha256(sha256(unhexlify(h) + unhexlify(h)).digest() + 
                              sha512(unhexlify(h)).digest()).digest())
    return o, h # Output new hash to use next time,
                # just in case there is some link between hash and modulus

def shuffle(ary_, h): # Fisher-Yates shuffle
    ary = []
    for i in range(len(ary_)): # Depending on how functions are imported,
                               # ary can carry over, so this makes sure to
                               # reset it, so the output is always correct.
        ary.append(ary_[i])
    a = len(ary)
    b = a - 1
    for d in range(b,0,-1):
        e, h = hashint(d, h)   # Get new hash each round, just in case
                               # there is some link between hash and modulus
        if e == d:
            continue
        ary[d], ary[e] = ary[e], ary[d]
    return ary

def xorhashes(hash_list):
    """
    XOR hashes to create a single unique 256-bit number

    XOR has the appealing property that the output has the entropy of
    whatever the highest entropy input was; therefore, as long as one
    item in the list is sufficiently random, the output will be
    sufficiently random.
    """

    o = 0
    for i in range(len(hash_list)):
        o = o ^ int(hash_list[i],16)
    o = hex(o).lstrip("0x").replace("L","").zfill(64)
    return o

def get_shuffled_deck(hash_list,element_array=unopened_deck):
    return shuffle(element_array,xorhashes(hash_list))


if __name__ == "__main__":
    """
    Run script with hex hashes as command line args.

    Example:
    $ python shuffle.py 86b827732d3812061fa1e9baaba82b232fa741a04557fa07225dc2b889bb694a b6e6985a7c03adf19aa9636b3c748000edd5f9f7363906b8211722acfc44026e

    Output will be each card followed by a new line.
    """

    hashlist = sys.argv
    hashlist.pop(0)
    deck = get_shuffled_deck(hashlist)
    for card in deck:
        print(card)
    exit()

