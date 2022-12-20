import numpy as np
from cpmpy import *
from aoc_helpers import input_helper
import re
from typing import List, Tuple

np.set_printoptions(edgeitems=30, linewidth=100000)
 
  
def parse_lines(lines: List[str]) -> List[Tuple[int]]:
    pattern = re.compile(r"Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
    blueprints = []

    for line in lines:
        groups = pattern.match(line).groups()
        blueprints.append(list(map(int, groups)))


    return blueprints

# Read input
blueprints = parse_lines(input_helper.get_lines(19))

    
ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
 
for N_STEPS, N_BLUEPRINTS in [(24, len(blueprints)), (32, 3)]:
    qualityLevels = []
    for index in range(N_BLUEPRINTS):
        bp = blueprints[index]
        a, b, c, d, e, f = bp
        costArray = cpm_array([
            [0, 0, 0, 0],
            [a, 0, 0, 0],
            [b, 0, 0, 0],
            [c, d, 0, 0],
            [e, 0, f, 0],
        ])
        # Lengths are NR_OF_STEPS+1 so we can have starting values at Minute 0
        botsPerStep = intvar(0, 999, shape=(4, N_STEPS + 1), name="bots")  # Array of amount of bots per step per type
        resourcesPerStep = intvar(0, 999, shape=(4, N_STEPS + 1), name="resources")  # Array of amount of resources per step per type
    
        building = intvar(-1, 3, shape=(1, N_STEPS+1), name="building")  # -1 = not building anything, bigger x means "building a robot that can harvest resource x"
        blueprintModel = Model(
        )
        for r in range(4):  # For every resource type...
            blueprintModel += (botsPerStep[r, 0] == (1 if r == ORE else 0))  # Start with 1 ore robot
            blueprintModel += (resourcesPerStep[r, 0] == 0)  # Start with 0 resources
    
            for s in range(1, N_STEPS+1):
                blueprintModel += (resourcesPerStep[r, s] == resourcesPerStep[r, s-1] >= costArray[building[0, s] + 1, r])
                blueprintModel += (resourcesPerStep[r, s] == resourcesPerStep[r, s-1] + botsPerStep[r, s-1] - costArray[building[0, s]+1, r])  # Spend resources to build bots
                blueprintModel += (botsPerStep[r, s] == (botsPerStep[r, s-1]) + (building[0, s] == r))  # If you are building a robot of type r, add 1 to the amount of bots
    
        blueprintModel.maximize(resourcesPerStep[3][N_STEPS])  # Objective: maximize the number of geodes in the end
        if blueprintModel.solve():
            print(f"blueprint {(index+1)}: {resourcesPerStep[3][N_STEPS].value()}")
            qualityLevels.append((index+1) * resourcesPerStep[3][N_STEPS].value())
        else:
            print("No solution found")
    print(qualityLevels)
    print("p1:", sum(qualityLevels))

