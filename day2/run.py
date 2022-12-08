from typing import List, Tuple
from aoc_helpers import input_helper

scores = {
    "A": 1,
    "B": 2,
    "C": 3,
    "Z": 6,
    "Y": 3,
    "X": 0,
}
rps = {
    "X": "A",
    "Y": "B",
    "Z": "C",
}

rps_response = {
    "A X": "C",
    "A Y": "A",
    "A Z": "B",
    "B X": "A",
    "B Y": "B",
    "B Z": "C",
    "C X": "B",
    "C Y": "C",
    "C Z": "A"
}

def main():
    lines = input_helper.get_lines(2)
    rounds_rps = parse_rounds_rps(lines)
    total_score = sum([get_round_score(a, b) for a, b in rounds_rps])

    print("1:", total_score)
    print("2:", get_score_2(lines))


def parse_rounds_rps(lines: List[str]) -> List[Tuple[str, str]]: 
    rounds = []
    for line in lines:
        if line == "":
            continue
        rounds.append((line[0], rps[line[2]]))
    return rounds

def get_round_score(a: str, b: str) -> int:
    if a == b:
        score = scores["Y"]
    if a == "A" and b == "B":
        score = scores["Z"]
    if a == "A" and b == "C":
        score = scores["X"]
    if a == "B" and b == "A":
        score = scores["X"]
    if a == "B" and b == "C":
        score = scores["Z"]
    if a == "C" and b == "A":
        score = scores["Z"]
    if a == "C" and b == "B":
        score = scores["X"]

    return score + scores[b]

def get_score_2(lines: List[str]) -> int:
    return sum([scores[rps_response[l]] + scores[l[2]] for l in lines if l != ""])

if __name__ == "__main__":
    main()