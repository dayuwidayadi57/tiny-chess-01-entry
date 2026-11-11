# tiny-chess-01 — a 4 KB Python chess engine

`main.py` (4,067 of the 4,096 allowed bytes) is the whole engine: an
lzma-packed artifact that unpacks and execs a compact Python source
(the rules explicitly allow a compressed payload plus its unpacker).
No model calls, no clock reads, no randomness — every move is a pure
function of the position, the game history and the trial seed, so a
trial replays move for move.

## Design

- 0x88 board, negamax alpha-beta with quiescence (captures, promotions,
  check replies), transposition table with ply-adjusted mate scores.
- Move ordering: TT move, MVV-LVA captures, killers. Null-move pruning
  and late-move reductions; checking moves are extended.
- Tapered evaluation: material + piece-square terms, bishop pair,
  passed-pawn bonuses by rank, knight/bishop mobility. Pawn-structure
  state is maintained incrementally with bit masks.
- Fixed budget of 60,000 nodes per move. The budget was set from local
  trial evidence, not by feel: at 95,000 nodes the richer evaluation's
  slowest moves on a throttled 1-CPU box ran past 11 s and four games
  were lost on time; at 60,000 the worst move over two full trials was
  7.5 s, with zero time losses and the strength gain intact.

## Local trials (kit gauntlet, same 8 book openings, fitted vs anchors)

| build | W/D/L | score | fitted Elo |
| --- | --- | --- | --- |
| v1, 90k nodes | 7/2/7 | 8.0/16 | ~1,396 |
| v2, 95k nodes | 7/2/7 | 8.0/16 | ~1,396 (4 time losses) |
| v2, 60k nodes | 8/2/6 | 9.0/16 | ~1,464 |

Perft verified exact on the standard five positions; make/unmake and
the incremental eval state round-trip exactly. The house baseline
(sunfish 4k) practices at a 1,360 mean on the kit instances.

## License

MIT — see `LICENSE`.
