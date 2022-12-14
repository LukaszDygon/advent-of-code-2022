from typing import Dict, List, Tuple
from aoc_helpers import input_helper

class Simulation:
    sim_map: Dict[Tuple[int,int], str]
    start_sand = (500, 0)
    max_y = 0

    def __init__(self, lines: List[str], is_infinite: bool = False):
        self.sim_map = self._build_rocks(lines)
        self.max_y = max([y for _, y in self.sim_map.keys()])
        if is_infinite:
            self._add_infinite_line(self.max_y+2)
            self.max_y += 3  # should never reach this
    
    def simulate_sand(self) -> bool:
        x, y = self.start_sand
        while not self._is_void(y) and self.sim_map.get(self.start_sand) != "o":
            if not self.sim_map.get((x, y+1)):
                y += 1
            elif not self.sim_map.get((x-1, y+1)):
                y += 1
                x -= 1

            elif not self.sim_map.get((x+1, y+1)):
                y += 1
                x += 1
            else:
                self.sim_map[(x, y)] = "o"
                return True
        
        return False

    def simulation(self):
        while self.simulate_sand():
            pass
        return list(self.sim_map.values()).count("o")

    def _is_void(self, y) -> bool:
        return y >= self.max_y

    def _build_rocks(self, lines: List[str]):
        sim_map = {}
        for l in lines:
            paths = [(int(p.split(",")[0]), int(p.split(",")[1])) for p in l.split(" -> ") ]
            for i in range(len(paths)-1):
                x, y = paths[i] 
                x2, y2 = paths[i+1]
                if x == x2:
                    for y in range(min(y, y2), max(y, y2) + 1):
                        sim_map[(int(x), int(y))] = "#"
                else:
                    for x in range(min(x, x2), max(x, x2) + 1):
                        sim_map[(int(x), int(y))] = "#"
        return sim_map
    
    def _add_infinite_line(self, y: int):
        for x in range(0, 1000):  # enough for the problem
            self.sim_map[(x, y)] = "#"

def main():
    lines = input_helper.get_lines(14)
    sim = Simulation(lines)
    sim2 = Simulation(lines, True)

    print("1:", sim.simulation())
    print("2:", sim2.simulation())

if __name__ == "__main__":
    main()