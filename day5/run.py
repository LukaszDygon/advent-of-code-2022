from typing import List, Tuple
from aoc_helpers import input_helper
from collections import defaultdict

def main():
    lines = input_helper.get_lines(5)
    initial_stacks, moves = parse_input(lines)
    stacks = do_moves(initial_stacks, moves)

    initial_stacks, moves = parse_input(lines)
    stacks_cartmover9001 = do_moves(initial_stacks, moves, True)
    print("1:", "".join([stacks[k][-1] for k in stacks.keys() if stacks[k]]))
    print("2:", "".join([stacks_cartmover9001[k][-1] for k in stacks_cartmover9001.keys() if stacks_cartmover9001[k]]))

def parse_input(lines: List[str]):
    stack_lines = []
    move_lines = []
    for i, l in enumerate(lines):
        if l.startswith(" 1"):
            break
    stack_lines = lines[:i]
    move_lines = lines[i+1:]
    return parse_stacks(stack_lines), parse_moves(move_lines)

def parse_stacks(lines: List[str]) -> defaultdict:
    lines.reverse()
    stacks = defaultdict(list)

    for line in lines:
        for i, char in enumerate(line):
            if char not in " []":
                stacks[str((i+3) // 4)].append(char)
        if line == "":
            continue
    return stacks

def parse_moves(lines: List[str]) -> List[Tuple[int, str, str]]:
    moves = []

    for line in lines:
        if line == "":
            continue
        words = line.split(" ")
        moves.append((int(words[1]), words[3], words[5]))
    return moves

def do_moves(stacks: defaultdict, moves: List[Tuple[int, str, str]], is_cartmover_9001=False):
    for (c, f, t) in moves:
        for i in range(c):
            stacks[t].append(stacks[f].pop())
        if is_cartmover_9001:
            s = stacks[t].copy()
            stacks[t] = s[:-c] + s[-1:-c-1:-1]
    return stacks
if __name__ == "__main__":
    main()