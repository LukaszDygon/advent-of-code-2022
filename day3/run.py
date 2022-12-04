from collections import Counter
from typing import List, Tuple
from aoc_helpers import input_helper


def main():
    lines = input_helper.get_lines(3)
    compartments = parse_compartments(lines)
    duplicates = get_duplicates(compartments)
    badges = find_badges(lines)
    print("1:", sum([get_value(item) for item in duplicates]))
    print("2:", sum([get_value(item) for item in badges]))

def parse_compartments(lines: List[str]) -> List[Tuple[str, str]]:
    compartments = []
    for line in lines:
        if line == "":
            continue
        mid = len(line)//2
        compartments.append((line[:mid], line[mid:]))
    return compartments

def get_duplicates(compartments: List[Tuple[str, str]]) -> str:
    return ''.join([''.join(set(a).intersection(set(b))) for a, b in compartments])

def find_badges(lines: List[str]) -> str:
    items = ""
    for i in range(0, len(lines), 3):
        c = Counter()
        for j in range(3):
            c.update(set(lines[i+j]))
        item = c.most_common(1)[0][0]
        items += item
    return items

def get_value(item: str) -> int:
    if item.islower():
        return ord(item) - 96
    return ord(item) - 64 + 26

if __name__ == "__main__":
    main()