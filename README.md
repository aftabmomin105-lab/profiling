# profiling
Algorithmic profiling
# BFS vs A* Search — Profiling Report (SLE-2)

**Student:** Aftab Momin
**PRN:** 25UAM028
**Course:** 02AML204 — Introduction to Artificial Intelligence
**Assignment:** SLE-2, Profiling Report (Empirical Performance Analysis)

This repository empirically compares an **uninformed search algorithm (BFS)** against
an **informed search algorithm (A\*)** on the same 60×60 grid maze, measuring real
execution time, nodes expanded, and path length instead of relying on theory alone.

## Problem

Find the shortest path from the top-left corner `(0, 0)` to the bottom-right corner
`(59, 59)` of a 60×60 grid maze that contains randomly placed obstacles
(`~22%` of cells, fixed random seed `42` for reproducibility). Movement is allowed
in 4 directions (up/down/left/right), and every move costs `1`.

- **Algorithm A — BFS (Breadth-First Search):** Uninformed search. Explores the
  grid level by level using a FIFO queue, with no knowledge of where the goal is.
- **Algorithm B — A\* Search:** Informed search. Uses the evaluation function
  `f(n) = g(n) + h(n)`, where `h(n)` is the Manhattan distance to the goal, to
  prioritise nodes that are likely closer to the destination.

## Files

| File | Description |
|---|---|
| `bfs_astar_compare.py` | Main script — implements BFS and A\*, builds the maze, and profiles both algorithms (3 runs each) using `time.perf_counter()` and a manual node-expansion counter. Run it directly: `python3 bfs_astar_compare.py` |
| `profile_bfs_run.py` | Wrapper that loops BFS repeatedly for ~3 seconds so `py-spy` has enough time to sample it |
| `profile_astar_run.py` | Wrapper that loops A\* repeatedly for ~3 seconds so `py-spy` has enough time to sample it |
| `profile_bfs.svg` | Flame graph of BFS, captured with `py-spy` |
| `profile_astar.svg` | Flame graph of A\*, captured with `py-spy` |
| `SLE2_25UAM028_AftabMomin.docx` | Final SLE-2 report (Word document) submitted on Moodle |
| `AI_CONTRIBUTION_LOG.md` | Log of what AI helped with vs. what I did myself |

## How to reproduce

```bash
# 1. Install dependencies
pip install py-spy --break-system-packages

# 2. Run the core comparison (prints the numbers used in the report)
python3 bfs_astar_compare.py

# 3. Generate the flame graphs
py-spy record -o profile_bfs.svg   -- python3 profile_bfs_run.py
py-spy record -o profile_astar.svg -- python3 profile_astar_run.py
```

Open the `.svg` files in a browser to view the interactive flame graphs (hover
over a block to see the function, file, line number, and % of samples).

## Results

| Metric | BFS | A\* Search | Better? |
|---|---|---|---|
| Avg. Time (ms) | 3.158 ms | 3.755 ms | BFS |
| Nodes Expanded | 2,817 nodes | 1,923 nodes | A\* Search |
| Path Length (steps) | 118 steps | 118 steps | Equal |

A\* expanded **~32% fewer nodes** than BFS because the Manhattan-distance
heuristic steers the search toward the goal instead of exploring every
direction equally. BFS was slightly *faster in wall-clock time* because it
only maintains a plain FIFO queue, while A\* pays extra overhead for
heap push/pop operations (`O(log n)`) and a heuristic calculation on every
candidate node. Both algorithms return the same optimal path length, which
confirms the Manhattan heuristic is admissible for this grid.

Full justification and analysis are in `SLE2_25UAM028_AftabMomin.docx`.

## What is a flame graph?

See [`FLAME_GRAPH_EXPLAINED.md`](FLAME_GRAPH_EXPLAINED.md) for a full walkthrough
of how to read `profile_bfs.svg` and `profile_astar.svg`.

## License

This repository is submitted coursework for SLE-2 (02AML204). Feel free to
reference the profiling approach, but please don't submit this exact code as
your own assignment.
