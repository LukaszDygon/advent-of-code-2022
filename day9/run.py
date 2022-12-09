from collections import Counter
from typing import List, Tuple
from aoc_helpers import input_helper

class Simulation:
    def __init__(self, tail_length: int = 1):
        self.visited = Counter()
        self.tail = [(0, 0) for _ in range(tail_length)]
        self.head = (0, 0)
        self.visited[self.head] = 1

    def run(self, lines: List[Tuple[str, int]]) -> Counter[Tuple[str, int]]:
        for direction, distance in lines:
            self._move(direction, distance)

    def _move(self, direction: str, distance: int):
        if direction == "U":
            for _ in range(distance):
                self.head = self.head[0], self.head[1] + 1
                self._move_tail()
        elif direction == "D":
            for _ in range(distance):
                self.head = self.head[0], self.head[1] - 1
                self._move_tail()
        elif direction == "R":
            for _ in range(distance):
                self.head = self.head[0] + 1, self.head[1]
                self._move_tail()
        elif direction == "L":
            for _ in range(distance):
                self.head = self.head[0] - 1, self.head[1]
                self._move_tail()

    def _move_tail(self):
        previous = self.head
        for i in range(len(self.tail)):
            if previous[0] - self.tail[i][0] == 2:
                self.tail[i] = self.tail[i][0] + 1, self._drift(self.tail[i][1], previous[1])
            elif previous[0] - self.tail[i][0] == -2:
                self.tail[i] = self.tail[i][0] - 1, self._drift(self.tail[i][1], previous[1])
            elif previous[1] - self.tail[i][1] == 2:
                self.tail[i] = self._drift(self.tail[i][0], previous[0]), self.tail[i][1] + 1
            elif previous[1] - self.tail[i][1] == -2:
                self.tail[i] = self._drift(self.tail[i][0], previous[0]), self.tail[i][1] - 1
            else:
                previous = self.tail[i]
                continue
            if i == len(self.tail) - 1:
                self.visited[self.tail[i]] += 1
            previous = self.tail[i]

    def _drift(self, a: int, b: int) -> int:
        if a > b:
            return a - 1
        elif a < b:
            return a + 1
        else:
            return a

def main():
    lines = input_helper.get_lines(9)
    lines = [(x[0], int(x[1])) for x in [x.split(" ") for x in lines]]
    simulation1 = Simulation()
    simulation2 = Simulation(9)
    simulation1.run(lines)
    simulation2.run(lines)
    print("1:", len(simulation1.visited.keys()))
    print("2:", len(simulation2.visited.keys()))



if __name__ == "__main__":
    main()