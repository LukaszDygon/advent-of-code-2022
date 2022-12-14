from aoc_helpers import input_helper
from typing import List, Any, Tuple
from itertools import zip_longest
from collections.abc import Iterable
from functools import cmp_to_key

def main():
    lines = input_helper.get_lines(13)
    pairs = parse_line_pairs(lines)
    valid = check_valid(pairs)
    flat = [p1 for p1, _ in pairs] + [p2 for _, p2 in pairs] + [[[2]], [[6]]]
    flat_sorted = sorted(flat, key=cmp_to_key(is_signal_valid), reverse=True)
    print("1:", sum([i+1 for i, v in enumerate(valid) if v == 1]))
    print("2:", (flat_sorted.index([[2]]) + 1) * (flat_sorted.index([[6]]) + 1))

def parse_line_pairs(lines: List[str]) -> List[Tuple[List[Any], List[Any]]]:
    pairs = []
    for l in range(0,len(lines), 3):
        pairs.append((eval(lines[l]), eval(lines[l+1])))
    
    return pairs

def check_valid(pairs: List[Tuple[List[Any], List[Any]]]) -> List[int]:
    return [is_signal_valid(a, b) for a, b in pairs]

def is_signal_valid(a: List[Any], b: List[Any]) -> int:
    for l, r in zip_longest(a, b):
        if r is None:
            return -1
        elif l is None:
            return 1
        elif isinstance(l, int) and isinstance(r, int):
            if l < r:
                return 1
            if l > r:
                return -1
        elif isinstance(l, list) and isinstance(r, list):
            s = is_signal_valid(l, r)
            if s != 0:
                return s
        elif isinstance(l, int) and isinstance(r, list):
            s = is_signal_valid([l], r)
            if s != 0:
                return s
        elif isinstance(l, list) and isinstance(r, int):
            s = is_signal_valid(l, [r])
            if s != 0:
                return s

    return 0




def flatten(x):
    if isinstance(x, Iterable):
        return tuple([a for i in x for a in flatten(i)])
    else:
        return tuple([x])

if __name__ == "__main__":
    main()