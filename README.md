# tiny-chess-01 — round 11 entry

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/dayuwidayadi57/tiny-chess-01-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/dayuwidayadi57/tiny-chess-01-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in 3,833 bytes of Python (limit: 4,096), for the make.fun
bounty "Build the strongest chess engine in 4 KB of Python" — see the
[bounty page](https://make.fun/bounty/tiny-chess-01).

`main.py` is the kit's own packing of `source.py` (the readable engine,
10,967 bytes): an LZMA stream plus the makefun-compress/v1 stub. Run it with
`MAKEFUN_ENV_URL` set and it plays the house gauntlet through the env.

Design (0x88 board, fixed 120,000-node budget per move, no clock):

- Negamax alpha-beta with principal variation search, null-move pruning
  (R=3), late-move reductions and check extensions; quiescence over
  captures, promotions and all replies to a check.
- Transposition table with ply-adjusted mate scores; MVV-LVA move
  ordering, two killer moves per ply and a history table; repetition
  (game history + search path) and fifty-move draws score 0 inside the
  search. The transposition table, killers and history are reset at the
  start of every game, so each game is a pure function of its moves.
- PeSTO tapered evaluation: the published middlegame/endgame
  piece-square tables and material values (pawn 82, knight 337, bishop
  365, rook 477, queen 1025), blended by game phase, plus a bishop-pair
  bonus.
- Iterative deepening at the root; root moves ordered by the previous
  iteration, aborted iterations discarded; the search stops early once a
  forced mate is found, so won games finish fast.

Run:

```
MAKEFUN_ENV_URL=http://127.0.0.1:PORT python3 -P -s main.py
```

Verified: perft exact on the standard positions (start, position 3, 4, 5
through depth 3–4; Kiwipete agrees exactly with the independent round 8
implementation at 37/1657/62832); make/unmake roundtrip exact; the same
position searched in two fresh processes gives the same move.

Local practice trial-0 (fresh kit, 19 Nov 2026): 5 won, 1 drawn, 0 lost,
Elo 1809, spare plies 364 — up from round 8's 3 won, 1 drawn, 2 lost,
Elo 1364, spare plies 294.
