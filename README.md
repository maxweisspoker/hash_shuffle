Turns a list of 256-bit hashes into a randomly shuffled (yet deterministic and verifiable) deck of cards.

A game server can get random nonces from players and send a hash commitment of its own nonce along with the players' cards, and then after the game ends, the server can reveal its nonce and the prior game can be verified as having used the correct deck.  (Note that
this reveals all cards to all players, which may be useful even after the game ends in games like poker.)

Import get_shuffled_deck() and have a single argument that is a list of 256-bit ascii hex hashes.  For example:

    get_shuffled_deck(['86b827732d3812061fa1e9baaba82b232fa741a04557fa07225dc2b889bb694a ', 'b6e6985a7c03adf19aa9636b3c748000edd5f9f7363906b8211722acfc44026e'])
    
will return a list of cards:

    ['2s', 'Ah', '5h', 'Td', '5d', 'Qd', '3c', '3h', '4h', 'Jd', '8s', '6s', 'Jh', '7d', '7s', 'Kh', '3d', '2c', 'Ad', '9c', 'Ts', 'Js', 'Kd', '2d', 'Tc', '3s', '9h', '8d', '4d', 'Qs', 'Ks', '6d', '7c', 'Kc', '5c', 'Jc', '7h', 'Ac', '5s', '2h', '9s', '4s', '6c', 'As', '6h', '4c', '9d', 'Qc', 'Qh', 'Th', '8c', '8h']
    
