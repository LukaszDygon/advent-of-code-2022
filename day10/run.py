from aoc_helpers import input_helper
from typing import List

def main():
    lines = input_helper.get_lines(10)
    signal_history = run_cycles(lines)
    print("1:", get_1(signal_history))

    for l in render_signal(signal_history[1:]):
        print(l)

def run_cycles(lines: List[str]) -> List[int]:
    X = 1
    signal_history = [X, X]
    for l in lines:
        if l == "noop":
            signal_history.append(X)
            continue
        else:
            signal_history.append(X)
            v = int(l.split(" ")[1])
            X += v
            signal_history.append(X)

    return signal_history

def get_strengths(signal_history: List[int]) -> List[int]:
    strengths = signal_history.copy()

    for i in range(len(strengths)):
        strengths[i] = strengths[i] * i
    return strengths

def get_1(signal_history: List[int]) -> int:
    strengths = get_strengths(signal_history)

    return sum(strengths[i] for i in range(20, 221, 40))

def render_signal(signal_history: List[int]) -> List[List[str]]:
    lines = []
    j = 0
    while j < len(signal_history) // 40:
        lines.append("")
        for i in range(40):
            lines[j] += get_char(signal_history[j*40+i], i)
        
        j += 1
    return lines

def get_char(X: int, i: int) -> str:
    if abs(X - i) <= 1:
        return "#"
    else:
        return "."
if __name__ == "__main__":
    main()