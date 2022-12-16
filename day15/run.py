from typing import Tuple, List
from aoc_helpers import input_helper
import re


def main():
    lines = input_helper.get_lines(15)
    positions = [parse_line(line) for line in lines]
    sections = get_y_sections(positions, 2_000_000)
    merged_sections = merge_overlapping(sections)
    print("1:", sum([s[1] - s[0] for s in merged_sections]))
    print("2:", search_tuning_frequency(positions))

def parse_line(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    match = pattern.match(line)
    return (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))

def get_y_sections(positions: Tuple[Tuple[int, int], Tuple[int, int]], y: int) -> List[Tuple[int, int]]:
    line_sections = []
    for sensor, beacon in positions:
        x_radius = abs(sensor[0] - beacon[0])
        y_radius = abs(sensor[1] - beacon[1])
        total_radius = x_radius + y_radius

        section_size = total_radius - abs(y - sensor[1])
        if section_size > 0:
            line_sections.append((sensor[0] - section_size, sensor[0] + section_size))
    
    return line_sections

def merge_overlapping(sections: List[Tuple[int, int]], max_x=None) -> List[Tuple[int, int]]:
    merged_sections = []
    for section in sorted(sections):
        if max_x and section[0] > max_x:
            break
        if not merged_sections:
            merged_sections.append(section)
        else:
            last_section = merged_sections[-1]
            if section[0] <= last_section[1]:
                merged_sections[-1] = (last_section[0], max(section[1], last_section[1]))
            else:
                merged_sections.append(section)
    return merged_sections

def search_tuning_frequency(positions: Tuple[Tuple[int, int], Tuple[int, int]], search_size = 4_000_000) -> int:
    y=0
    while y <= search_size:
        if y % 10_000 == 0:
            print(y)
        sections = get_y_sections(positions, y)
        overlapping_sections = merge_overlapping(sections, search_size)
        if len(overlapping_sections) > 1:
            return get_tuning_frequency(overlapping_sections[0][1]+1, y)
        y += 1
    

def get_tuning_frequency(x: int, y: int) -> int:
    return x * 4_000_000 + y


if __name__ == "__main__":
    main()