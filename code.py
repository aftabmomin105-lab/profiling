"""
SLE-2: Profiling Report - BFS vs A* Search Algorithm
Student: Aftab Momin | PRN: 25UAM028
Course: 02AML204 - Introduction to Artificial Intelligence

This script implements BFS (Uninformed Search) and A* (Informed Search)
on the same 20x20 grid maze with obstacles, and profiles both algorithms
using time.perf_counter() and a manual node-expansion counter.
"""

import heapq
import time
import random
from collections import deque

# ----------------------------------------------------------------------
# 1. Build a small, fixed grid maze (20x20) with obstacles
# ----------------------------------------------------------------------
ROWS, COLS = 60, 60
random.seed(42)  # fixed seed so the maze is reproducible

def generate_maze(rows, cols, obstacle_prob=0.22):
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if random.random() < obstacle_prob:
                maze[r][c] = 1  # 1 = wall
    maze[0][0] = 0
    maze[rows - 1][cols - 1] = 0
    return maze

MAZE = generate_maze(ROWS, COLS)
START = (0, 0)
GOAL = (ROWS - 1, COLS - 1)


def neighbors(node):
    r, c = node
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
            yield (nr, nc)


# ----------------------------------------------------------------------
# 2. BFS - Uninformed Search
# ----------------------------------------------------------------------
def bfs(start, goal):
    frontier = deque([start])
    came_from = {start: None}
    nodes_expanded = 0

    while frontier:
        current = frontier.popleft()
        nodes_expanded += 1

        if current == goal:
            break

        for nxt in neighbors(current):
            if nxt not in came_from:
                came_from[nxt] = current
                frontier.append(nxt)

    path = reconstruct_path(came_from, start, goal)
    return path, nodes_expanded


# ----------------------------------------------------------------------
# 3. A* Search - Informed Search (Manhattan distance heuristic)
# ----------------------------------------------------------------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(start, goal):
    frontier = [(0, start)]
    came_from = {start: None}
    g_score = {start: 0}
    nodes_expanded = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        nodes_expanded += 1

        if current == goal:
            break

        for nxt in neighbors(current):
            new_g = g_score[current] + 1
            if nxt not in g_score or new_g < g_score[nxt]:
                g_score[nxt] = new_g
                f_score = new_g + heuristic(nxt, goal)
                heapq.heappush(frontier, (f_score, nxt))
                came_from[nxt] = current

    path = reconstruct_path(came_from, start, goal)
    return path, nodes_expanded


def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return None
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path


# ----------------------------------------------------------------------
# 4. Profiling: run each algorithm 3 times, record time + nodes expanded
# ----------------------------------------------------------------------
def profile_algorithm(func, runs=3):
    times = []
    nodes_list = []
    path_len = None

    for _ in range(runs):
        t0 = time.perf_counter()
        path, nodes_expanded = func(START, GOAL)
        t1 = time.perf_counter()

        times.append((t1 - t0) * 1000)  # ms
        nodes_list.append(nodes_expanded)
        path_len = len(path) - 1 if path else None  # steps

    avg_time = sum(times) / len(times)
    avg_nodes = sum(nodes_list) / len(nodes_list)
    return avg_time, avg_nodes, path_len, times, nodes_list


if __name__ == "__main__":
    print(f"Grid size: {ROWS}x{COLS} | Start: {START} | Goal: {GOAL}")
    print("-" * 60)

    bfs_time, bfs_nodes, bfs_path_len, bfs_times, bfs_nodes_list = profile_algorithm(bfs, runs=3)
    astar_time, astar_nodes, astar_path_len, astar_times, astar_nodes_list = profile_algorithm(a_star, runs=3)

    print("BFS (Uninformed Search)")
    print(f"  Run times (ms): {[round(t, 3) for t in bfs_times]}")
    print(f"  Nodes expanded per run: {bfs_nodes_list}")
    print(f"  Avg time: {bfs_time:.3f} ms | Avg nodes expanded: {bfs_nodes:.0f} | Path length: {bfs_path_len} steps")
    print("-" * 60)

    print("A* Search (Informed Search - Manhattan heuristic)")
    print(f"  Run times (ms): {[round(t, 3) for t in astar_times]}")
    print(f"  Nodes expanded per run: {astar_nodes_list}")
    print(f"  Avg time: {astar_time:.3f} ms | Avg nodes expanded: {astar_nodes:.0f} | Path length: {astar_path_len} steps")
    print("-" * 60)

    faster = "BFS" if bfs_time < astar_time else "A*"
    fewer_nodes = "BFS" if bfs_nodes < astar_nodes else "A*"
    print(f"Faster (avg time): {faster}")
    print(f"Fewer nodes expanded: {fewer_nodes}")