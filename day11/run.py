from dataclasses import dataclass
from functools import reduce
from aoc_helpers import input_helper
from typing import List

@dataclass
class Monkey:
    name: str
    items: List[int]
    operation: str
    test_modulo: int
    if_true: int
    if_false: int
    inspections: int = 0

class Simulation():
    monkeys: List[Monkey]
    rounds: int
    worry_modifier: int
    current_round: int = 0

    def __init__(self, lines: List[str], rounds: int, worry_modifier: int = 1):
        self.monkeys = self.parse_monkeys(lines)
        self.rounds = rounds
        self.mod_product = reduce(lambda x, y: x * y, [monkey.test_modulo for monkey in self.monkeys])
        self.worry_modifier = worry_modifier
    
    def parse_monkeys(self, lines: List[str]) -> List[Monkey]:
        monkeys = []
        for i in range(0, len(lines), 7):
            monkeys.append(self.parse_monkey(lines[i:i+6]))

        return monkeys

    def parse_monkey(self, lines: List[str]) -> Monkey:
        return (Monkey(lines[0][:-1],  
            [int(x) for x in lines[1].split(": ")[1].split(", ")],
            lines[2].split(" = ")[1],
            int(lines[3].split(" by ")[1]),
            int(lines[4].split(" monkey ")[1]),
            int(lines[5].split(" monkey ")[1])
        ))

    def run(self):
        while self.current_round < self.rounds:
            self.run_round()
            self.current_round += 1

    def run_round(self):
        for monkey in self.monkeys:
            self.run_monkey(monkey)
    
    def run_monkey(self, monkey: Monkey):
        monkey.inspections += len(monkey.items)
        while monkey.items:
            old = monkey.items.pop(0)
            new = ((eval(monkey.operation)) // self.worry_modifier) % self.mod_product
            if new % monkey.test_modulo  == 0:
                self.monkeys[monkey.if_true].items.append(new)
            else:
                self.monkeys[monkey.if_false].items.append(new)
            

def main():
    lines = input_helper.get_lines(11)
    sim1 = Simulation(lines, 20, 3)
    sim1.run()
    inspections_desc1 = sorted([m.inspections for m in sim1.monkeys], reverse=True)
    print("1:", inspections_desc1[0] * inspections_desc1[1])
    sim2 = Simulation(lines, 10_000, 1)
    sim2.run()
    inspections_desc2 = sorted([m.inspections for m in sim2.monkeys], reverse=True)
    print("2:", inspections_desc2[0] * inspections_desc2[1])

if __name__ == "__main__":
    main()