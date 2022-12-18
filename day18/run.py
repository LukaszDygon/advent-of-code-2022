from typing import List, Tuple, Set
from aoc_helpers import input_helper


def main():
    lines = input_helper.get_lines(18)
    cubes = parse_input(lines)

    print("1:", count_all_faces(cubes))
    print("2:", get_water(cubes))

def parse_input(lines: Set[Tuple[int, int, int]]):
    return {tuple([int(x) for x in line.split(",")]) for line in lines}

def count_all_faces(cubes: Set[Tuple[int, int, int]]) -> int:
    faces = [s for s in get_sides(cubes) if s not in cubes]
    return len(faces)

def get_water(cubes: Set[Tuple[int, int, int]]) -> int:
    seen = set()
    todo = [(-1,-1,-1)]  # start with a cube outside the grid
    max_v = max(max(*c) for c in cubes) + 1

    while todo:
        here = todo.pop()
        sides_set = set(get_sides([here]))
        todo += [s for s in (sides_set - cubes - seen) if all(-1<=c<=max_v for c in s)]
        seen |= {here}
    
    return len([s for s in get_sides(cubes) if s not in cubes and s in seen])

def get_sides(cubes: Set[Tuple[int, int, int]]) -> Set[Tuple[int, int, int]]:
    sides = []
    iter_sides = lambda x, y, z: [(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)]
    for c in cubes:
       sides.extend(iter_sides(*c))
    
    return sides
    

if __name__ == "__main__":
    main()