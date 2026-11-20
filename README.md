# tiny-chess-01 — round 15 entry

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/dayuwidayadi57/tiny-chess-01-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/dayuwidayadi57/tiny-chess-01-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in 4,022 bytes of Python (limit: 4,096), for the make.fun
bounty "Build the strongest chess engine in 4 KB of Python" — see the
[bounty page](https://make.fun/bounty/tiny-chess-01).

`main.py` is the kit's own packing of `source.py` (the readable engine,
11,359 bytes): an LZMA stream plus the makefun-compress/v1 stub. Run it with
`MAKEFUN_ENV_URL` set and it plays the house gauntlet through the env.

Design (0x88 board, fixed 120,000-node budget per move, no clock):

- Negamax alpha-beta with principal variation search, null-move pruning
  (R=3), late-move reductions and check extensions; quiescence over
  captures, promotions and all replies to a check.
- Transposition table with ply-adjusted mate scores; MVV-LVA ordering,
  two killers per ply and a history table; repetition and fifty-move
  draws score 0 in search. TT, killers and history reset each game.
- PeSTO tapered evaluation (published middlegame/endgame tables,
  pawn 82, knight 337, bishop 365, rook 477, queen 1025), bishop-pair
  bonus, +8 tempo, and a king pawn-shield term.
- Mate-distance pruning (`a = max(a, ply - MATE)`, `b = min(b, MATE - ply)`).
  Delta pruning in quiescence: a capture whose static value plus the
  captured piece plus a 150 margin still falls below alpha is skipped.
  Kept from round 11: the 120,000-node budget, repetition scoring 0,
  and no opening book.
- Iterative deepening at the root; root moves ordered by the previous
  iteration, aborted iterations discarded; the search stops early once a
  forced mate is found.

Run:

```
MAKEFUN_ENV_URL=http://127.0.0.1:PORT python3 -P -s main.py
```

Verified: perft exact on the standard positions; make/unmake roundtrip
exact; the same position searched in two fresh processes gives the same move.

Local practice trial-0 (fresh kit, 20 Nov 2026): 6 won, 0 drawn, 0 lost,
spare plies 749 (451 plies: 39/52/67/78/65/150), every game won by
checkmate — up from round 14's 6/0/0, spare 663 (537 plies). Think time
stayed at baseline (mean 3.03 s, max 4.22 s per move, nothing over 6 s).
