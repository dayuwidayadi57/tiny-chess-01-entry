# tiny-chess-01 — a 4 KB Python chess engine

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/dayuwidayadi57/tiny-chess-01-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/dayuwidayadi57/tiny-chess-01-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

`main.py` (4,088 of the 4,096 allowed bytes) is the whole engine: an
lzma-packed artifact that unpacks and execs a compact Python source
(the rules explicitly allow a compressed payload plus its unpacker).
No model calls, no clock reads, no randomness — every move is a pure
function of the position, the game history and the trial seed, so a
trial replays move for move.

## Design

- 0x88 board, negamax alpha-beta with quiescence (captures, promotions,
  check replies), transposition table with ply-adjusted mate scores.
- Move ordering: TT move, MVV-LVA captures, killers, PVS. Null-move
  pruning, late-move reductions, checking moves extended.
- Tapered evaluation: material + piece-square terms, bishop pair,
  passed-pawn bonuses by rank, knight/bishop mobility. Pawn-structure
  state is maintained incrementally with bit masks.
- Fixed budget of 100,000 nodes per move. The budget was set from local
  trial evidence, not by feel: the v3 engine at 150,000 nodes scored 0
  on the server practice grade. At 100,000 nodes the same engine (plus
  principal variation search) uses 70.6% of the wall locally, with the
  slowest move 4.3 s and zero time losses.
- Hardened agent loop (v4e): the env calls retry — `/game` is retried
  with a 3 s pause until the env answers, every request carries a 30 s
  timeout, and the process waits up to 30 s for `MAKEFUN_ENV_URL` to
  appear instead of exiting silently. The search engine is unchanged
  from v4d (same 100,000-node budget, same fitted Elo ~1,396). v4d was
  rejected with practice grade 0 at the day's peak-load hour; a short
  local regression trial confirms the loop survives that startup case.

## Local trials (kit gauntlet, same 8 book openings, fitted vs anchors)

| build | W/D/L | score | fitted Elo |
| --- | --- | --- | --- |
| v4d, 100k nodes | 8/0/8 | 8.0/16 | ~1,396 |
| v4e, 100k nodes | 8/0/8 | 8.0/16 | ~1,396 |

Trials 11–12 (v4e): prestart 2-game gauntlet 2/0/0, think max 3,342 ms; full
16-game gauntlet 8/0/8, Elo ~1,396 (identical to v4d in every rung), think
max 3,423 ms, 0 non-200 calls, zero time losses.

Perft verified exact on the standard five positions; make/unmake and
the incremental eval state round-trip exactly.
