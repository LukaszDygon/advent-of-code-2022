from aoc_helpers import input_helper
from typing import List
from functools import reduce

def main():
    lines = input_helper.get_lines(8)
    for i in range(len(lines)):
        lines[i] = [int(x) for x in lines[i]]
    visible_matrix = find_visible_trees(lines)
    scenic_scores = get_scenic_scores(lines)
    print("1:", sum([sum(x) for x in visible_matrix]))
    print("2:", max([max(x) for x in scenic_scores]))

def find_visible_trees(lines: List[List[int]]) -> List[List[int]]:
    x = len(lines[0])
    y = len(lines)
    visible = [[0 for _ in range(x)] for _ in range(y)]
    for i in range(x):
        biggest = -1
        for j in range(y):
            if lines[j][i] > biggest:
                visible[j][i] = 1
                biggest = lines[j][i]
    
    for i in range(x):
        biggest = -1
        for j in range(-1, -y-1, -1):
            if lines[j][i] > biggest:
                visible[j][i] = 1
                biggest = lines[j][i]

    for j in range(y):
        biggest = -1
        for i in range(x):
            if lines[j][i] > biggest:
                visible[j][i] = 1
                biggest = lines[j][i]

    for j in range(y):
        biggest = -1
        for i in range(-1, -x-1, -1):
            if lines[j][i] > biggest:
                visible[j][i] = 1
                biggest = lines[j][i]
    
    return visible

def get_scenic_scores(lines: List[List[int]]) -> List[int]:
    x = len(lines[0])
    y = len(lines)
    scores = [[0 for _ in range(x)] for _ in range(y)]
    for i in range(x):
        for j in range(y):
            scores[j][i] = get_scenic_score(lines, i, j)
    return scores

def get_scenic_score(lines: List[List[int]], i_s, j_s) -> int:
    x = len(lines[0])
    y = len(lines)
    scenic_score = [0, 0, 0, 0]

    for j in range(j_s, y):
        if j == j_s: continue
        scenic_score[0] += 1
        if lines[j][i_s] >= lines[j_s][i_s]:
            break

    for j in range(j_s, -1, -1):
        if j == j_s: continue
        scenic_score[1] += 1
        if lines[j][i_s] >= lines[j_s][i_s]:
            break

    for i in range(i_s, x):
        if i == i_s: continue
        scenic_score[2] += 1
        if lines[j_s][i] >= lines[j_s][i_s]:
            break

    for i in range(i_s, -1, -1):
        if i == i_s: continue
        scenic_score[3] += 1
        if lines[j_s][i] >= lines[j_s][i_s]:
            break

    return reduce(lambda x, y: x * y, scenic_score)

if __name__ == "__main__":
    main()