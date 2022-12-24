from aoc_helpers import input_helper
from typing import List, Tuple, Set
from collections import Counter

class Simulation:
    def __init__(self, space: Set[Tuple[int]]) -> None:
        self.space = space
        self.current_round = 1

    def run(self, rounds: int) -> int:
        for round in range(rounds):
            intentions = self.__calculate_intentions(self.current_round-1)
            if len(intentions) == 0:
                break
            pruned_intentions = self.__prune_intentions(intentions)
            self.__update_state(pruned_intentions)
            print("after round:", self.current_round)
            print(self)
            self.current_round += 1
        
        return self.__get_empty()

    def __calculate_intentions(self, r: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        intentions = []
        for x, y in self.space:
            if all([s not in self.space for s in [(x, y-1), (x, y+1), (x-1, y), (x+1, y), (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]]):
                continue
            moves = [
                ((x, y - 1) not in self.space and (x - 1, y - 1) not in self.space and (x + 1, y - 1) not in self.space, (x, y - 1)),
                ((x, y + 1) not in self.space and (x - 1, y + 1) not in self.space and (x + 1, y + 1) not in self.space, (x, y + 1)),
                ((x - 1, y) not in self.space and (x - 1, y + 1) not in self.space and (x - 1, y - 1) not in self.space, (x - 1, y)),
                ((x + 1, y) not in self.space and (x + 1, y + 1) not in self.space and (x + 1, y - 1) not in self.space, (x + 1, y))
            ]
            for i in [(i + r) % 4 for i in range(4)]:
                if moves[i][0]:
                    intentions.append(((x, y), moves[i][1]))
                    break
        return intentions

    def __update_state(self, intentions: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        for intention in intentions:
            self.space.remove(intention[0])
            self.space.add(intention[1])
        
        pass

    def __prune_intentions(self, intentions: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        duplicates = {k for k, count in Counter([intention[1] for intention in intentions]).items() if count > 1}
        return [intention for intention in intentions if intention[1] not in duplicates]

    def __get_empty(self) -> int:
        x_min, x_max = min([s[0] for s in self.space]), max([s[0] for s in self.space])
        y_min, y_max = min([s[1] for s in self.space]), max([s[1] for s in self.space])
        elves = len(self.space)
        return (x_max - x_min + 1) * (y_max - y_min + 1) - elves

    def __str__(self):
        x_min, x_max = min([s[0] for s in self.space]), max([s[0] for s in self.space])
        y_min, y_max = min([s[1] for s in self.space]), max([s[1] for s in self.space])
        output = ""
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if (x, y) in self.space:
                    output += "#"
                else:
                    output += "."
            output += "\n"
        return output

def main():
    lines = input_helper.get_lines(23)
    positions = get_positions(lines)
    sim = Simulation(positions)
    empty_spaces = sim.run(10)
    print("1:", empty_spaces)
    sim.run(1000)
    print("2:", sim.current_round)

def get_positions(lines: List[str]) -> Set[Tuple[int, int]]:
    positions = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                positions.append((x, y))
    return set(positions)

if __name__ == "__main__":
    main()