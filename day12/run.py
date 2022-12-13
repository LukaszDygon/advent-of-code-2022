from aoc_helpers import input_helper
from typing import List, Tuple

def main():
    lines = input_helper.get_lines(12)
    start, end, grid = parse_map(lines)
    print("1:", get_shortest_bfs(start, end, grid))
    print("2:", get_shortest_reverse(end, ord("a"), grid))

def parse_map(lines: List[str]) -> Tuple[Tuple[int, int], Tuple[int, int], List[List[int]]]:
    grid = []
    start = None
    end = None
    for j, l in enumerate(lines):
        if "S" in l:
            start = (l.index("S"), j)
            l = l.replace("S", "a")
        if "E" in l:
            end = (l.index("E"), j)
            l = l.replace("E", "z")
        grid.append([ord(x) for x in l])
    
    return start, end, grid

def get_shortest_bfs(start: Tuple[int, int], end: Tuple[int, int], grid: List[List[int]]) -> int:
    paths: List[List[Tuple[int, int]]] = [[start]]
    visited = set()
    while paths:
        path = paths.pop(0)
        last_coord = path[-1]
        if last_coord == end:
            return len(path) - 1
        
        next_coords = get_next_coords(last_coord, grid)
        next_coords = [x for x in next_coords if x not in visited and grid[last_coord[1]][last_coord[0]] >= grid[x[1]][x[0]] - 1]
        visited.update(next_coords)
        for coord in next_coords:
            paths.append(path + [coord])

def get_shortest_reverse(start: Tuple[int, int], end_elevation: int, grid: List[List[int]]) -> int:
    paths: List[List[Tuple[int, int]]] = [[start]]
    visited = set()
    while paths:
        path = paths.pop(0)
        last_coord = path[-1]
        if grid[last_coord[1]][last_coord[0]] == end_elevation:
            return len(path) - 1
        next_coords = get_next_coords(last_coord, grid)
        next_coords = [x for x in next_coords if x not in visited and grid[last_coord[1]][last_coord[0]] <= grid[x[1]][x[0]] + 1]
        visited.update(next_coords)
        for coord in next_coords:
            paths.append(path + [coord])

def get_next_coords(coord: Tuple[int, int], grid: List[List[int]]) -> List[Tuple[int, int]]:
    return [
        (max(0, coord[0] - 1), coord[1]),
        (min(len(grid[0])-1, coord[0] + 1), coord[1]),
        (coord[0], max(0, coord[1] - 1)),
        (coord[0], min(len(grid)-1, (coord[1] + 1)))
    ]
if __name__ == "__main__":
    main()