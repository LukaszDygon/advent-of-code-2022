from typing import List, Tuple, Dict, Union
from aoc_helpers import input_helper
import re

def main():
    lines = input_helper.get_lines(21)
    equasions = get_equations(lines)
    print("1:", resolve_equations(equasions.copy()))
    print("2:", find_humn(equasions.copy()))


def get_equations(lines: List[str]) -> Dict[str, Union[int, Tuple[str, str, str]]]:
    equations = [line.split(": ") for line in lines]
    equation_map = {}
    for eqation in equations:
        if re.search(r"\d", eqation[1]):
            equation_map[eqation[0]] = int(eqation[1])
        else:
            groups = re.match("([a-z]{4}) ([+-/*]) ([a-z]{4})", eqation[1]).groups()
            equation_map[eqation[0]] = (groups[0], groups[2], groups[1])
    return equation_map

def resolve_equations(equations: Dict[str, Union[int, Tuple[str, str, str]]]) -> int:
    is_resolved = False
    i = 0
    while not is_resolved:
        is_resolved = True
        for key, value in equations.items():
            if isinstance(value, tuple):
                if isinstance(equations[value[0]], int) and isinstance(equations[value[1]], int):
                    if value[2] == "+":
                        equations[key] = equations[value[0]] + equations[value[1]]
                    elif value[2] == "-":
                        equations[key] = equations[value[0]] - equations[value[1]]
                    elif value[2] == "*":
                        equations[key] = equations[value[0]] * equations[value[1]]
                    elif value[2] == "/":
                        if equations[value[0]] % equations[value[1]] == 0:
                            equations[key] = equations[value[0]] // equations[value[1]]
                        else:
                            raise ValueError("Not divisible")
                else:
                    is_resolved = False

    return equations['root']

def find_humn(equations_initial: Dict[str, Union[int, Tuple[str, str, str]]]) -> int:
    equations_initial['root'] = equations_initial['root'][0], equations_initial['root'][1], '-'
    equations = equations_initial.copy()
    high, low = 0, 1000000000000000000
    while equations['root'] != 0:
        equations = equations_initial.copy()
        try:
            resolve_equations(equations)
        except:
            equations_initial['humn'] -= 1
            continue

        print(equations['root'], equations['humn'], low, high)

        if equations['root'] < 0:  # swap if not getting result
            low = equations['humn']
        else:
            high = equations['humn']
            
        equations_initial['humn'] = (high + low) // 2
    return equations['humn']

if __name__ == "__main__":
    main()