from typing import Tuple, List
from aoc_helpers import input_helper


def main():
    lines = input_helper.get_lines(4)
    assignments = parse_assignments(lines)
    ovelapping = get_fully_overlapping(assignments)
    print("1:", len(ovelapping))
    print("2:", len(get_partially_overlapping(assignments)))

def parse_assignments(lines: List[str]) -> List[List[Tuple[str, str]]]:
    assignments = []
    for line in lines:
        if line == "":
            continue
        pair = [el.split("-") for el in line.split(",")]
        assignments.append([(int(v[0]), int(v[1])) for v in pair])
    return assignments

def get_fully_overlapping(assignments: List[List[Tuple[str, str]]]) -> List[int]:
    overlapping = []
    for assignment in assignments:
            if (assignment[0][0] <= assignment[1][0] and assignment[0][1] >= assignment[1][1]) or \
                (assignment[1][0] <= assignment[0][0] and assignment[1][1] >= assignment[0][1]):
                overlapping.append(assignment)
    return overlapping

def get_partially_overlapping(assignments: List[List[Tuple[str, str]]]) -> List[int]:
    overlapping = []
    for assignment in assignments:
            if (assignment[0][0] <= assignment[1][0] and assignment[0][1] >= assignment[1][0]) or \
                (assignment[1][0] <= assignment[0][0] and assignment[1][1] >= assignment[0][0]):
                overlapping.append(assignment)
    return overlapping
    
if __name__ == "__main__":
    get_fully_overlapping([[(7,8),(8,18)]])
    main()