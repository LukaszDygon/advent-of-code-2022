# Uses A* search

from functools import cache
from heapq import heappush, heappop


DIRS = {'<':(-1, 0), '>':(1, 0), '^':(0, -1) ,'v':(0, 1), '.':(0, 0)}
grid_height, grid_width = 0, 0

@cache  # memoization
def step(grid, blizz):
    blizz = frozenset((((x+dx)%grid_height, (y+dy)%grid_width), (dx, dy)) for (x, y), (dx, dy) in blizz)
    free = grid - {b[0] for b in blizz}
    return blizz, free

def manhatan_distance(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)

def walk(start, goal, grid, blizzards):
    stack, seen, ti = [], set(), 0
    heappush(stack, (0, start, blizzards, ti))
    while stack:
        _, (x, y), blizzard, t = heappop(stack)
        blizzard, free = step(grid, blizzard)
        for (dx, dy) in DIRS.values():
            p = (x+dx, y+dy)
            if p == goal:
                return t+1, blizzard
            elif p in free:
                if (p, blizzard) not in seen:
                    seen.add((p, blizzard))
                    heappush(stack, (manhatan_distance(*p, *goal)+t, p, blizzard, t+1))
    return -1

grid, blizzards = set(), set()
with open('day24/input.txt') as f:
    for y, row in enumerate(f.readlines()[1:-1]):
        grid_width = max(y + 1, grid_width)
        for x, val in enumerate(row.strip()[1:-1]):
            grid_height = max(x + 1, grid_height)
            grid.add((x, y))
            if val != '.': blizzards.add(((x, y), DIRS[val]))

start, goal = (0, -1), (grid_height-1, grid_width)
grid.add(start)
grid.add(goal)
tt = []
grid, blizz = frozenset(grid), frozenset(blizzards)
for p1, p2 in (start, goal), (goal, start), (start, goal):
    t, blizz = walk(p1, p2, grid, blizz)
    tt.append(t)
print('1:', tt[0])
print('2:', sum(tt))