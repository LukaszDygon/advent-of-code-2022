from __future__ import annotations

from dataclasses import dataclass
from aoc_helpers import input_helper
import re
from typing import List, Tuple
from enum import Enum 

class Resource(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4

@dataclass
class Blueprint:
    def __init__(self, ore_robot_cost: Tuple[int, int, int], clay_robot_cost: Tuple[int, int, int], obsidian_robot_cost: Tuple[int, int, int], geode_robot_cost: Tuple[int, int, int]):
        self.robot_cost = {
            Resource.ORE: { Resource.ORE: ore_robot_cost[0], Resource.CLAY: ore_robot_cost[1], Resource.OBSIDIAN: ore_robot_cost[2] },
            Resource.CLAY: { Resource.ORE: clay_robot_cost[0], Resource.CLAY: clay_robot_cost[1], Resource.OBSIDIAN: clay_robot_cost[2] },
            Resource.OBSIDIAN: { Resource.ORE: obsidian_robot_cost[0], Resource.CLAY: obsidian_robot_cost[1], Resource.OBSIDIAN: obsidian_robot_cost[2] },
            Resource.GEODE: { Resource.ORE: geode_robot_cost[0], Resource.CLAY: geode_robot_cost[1], Resource.OBSIDIAN: geode_robot_cost[2] }
        }

        self.max_cost = {
            Resource.ORE: max([self.robot_cost[robot_resource][Resource.ORE] for robot_resource in Resource]),
            Resource.CLAY: max([self.robot_cost[robot_resource][Resource.CLAY] for robot_resource in Resource]),
            Resource.OBSIDIAN: max([self.robot_cost[robot_resource][Resource.OBSIDIAN] for robot_resource in Resource])
        }

    def __getitem__(self, item: Resource):
         return self.robot_cost[item]

class Game:
    def __init__(self, blueprint: Blueprint, rounds: int):
        self.blueprint = blueprint
        self.rounds = rounds
        self.current_round = 0
        self.resources = {r: 0 for r in Resource}
        self.robots = {r: 0 for r in Resource}
        self.robots[Resource.ORE] = 1
        self.production_unsaturated: List[Resource] = [Resource.ORE, Resource.CLAY, Resource.OBSIDIAN]

    def run_round(self, build: Resource = None) -> bool:
        self.current_round += 1

        for resource in Resource:
            self.resources[resource] += self.robots[resource]

        if build is not None:
            for resource in [Resource.ORE, Resource.CLAY, Resource.OBSIDIAN]:
                self.resources[resource] -= self.blueprint[build][resource]
            self.robots[build] += 1

    def is_finished(self) -> bool:
        if self.current_round > self.rounds:
            raise Exception("Game is already finished and ran extra round!")
        
        return self.current_round == self.rounds
        
    def get_robot_options(self) -> List[Resource]:
        for resource in self.production_unsaturated:
            if self.robots[resource] == self.blueprint.max_cost[resource] \
                or self.robots[resource] * (self.rounds - self.current_round) + self.resources[resource] >= self.blueprint.max_cost[resource] * (self.rounds - self.current_round):
                self.production_unsaturated.remove(resource)

        if all([self.resources[cost_resource] >= self.blueprint.robot_cost[Resource.GEODE][cost_resource]
                for cost_resource in [Resource.ORE, Resource.OBSIDIAN]]):
                return [Resource.GEODE]


        options = [None]
        for robot_resource in self.production_unsaturated:
            if all([self.resources[cost_resource] >= self.blueprint.robot_cost[robot_resource][cost_resource]
                for cost_resource in [Resource.ORE, Resource.CLAY]]):
                options.append(robot_resource)
        return options
    
    def clone(self) -> Game:
        game = Game(self.blueprint, self.rounds)
        game.current_round = self.current_round
        game.resources = self.resources.copy()
        game.robots = self.robots.copy()
        game.production_unsaturated = self.production_unsaturated.copy()

        return game

    def get_geode_score(self) -> int:
        return self.resources[Resource.GEODE]

    def other_could_be_better(self, other: Game) -> bool:
        return any(
            [self.resources[resource] + self.robots[resource] * (self.rounds - self.current_round) 
            <= other.resources[resource] + other.robots[resource] * (other.rounds - other.current_round) 
            for resource in Resource]
        )

    def get_new_optimal(self, other: Game) -> Game:
        game = Game(self.blueprint, self.rounds)
        game.current_round = max(self.current_round, other.current_round)
        game.resources = {r: max(self.resources[r], other.resources[r]) for r in Resource}
        game.robots = {r: max(self.robots[r], other.robots[r]) for r in Resource}
        return game
        
def main():
    lines = input_helper.get_lines(19)
    blueprints = parse_lines(lines)
    games = [Game(blueprint, 24) for blueprint in blueprints]
    game_geode_scores = []
    for i, game in enumerate(games):
        optimal_game = game.clone()
        game_scenarios: List[Game] = [game]
        finished_games: List[Game] = []
        while game_scenarios:
            game = game_scenarios.pop()
            options = game.get_robot_options()
            for option in options:
                new_game = game.clone()
                new_game.run_round(option)
                if new_game.is_finished():
                    finished_games.append(new_game)
                elif optimal_game.other_could_be_better(new_game):
                    optimal_game = optimal_game.get_new_optimal(new_game)
                    game_scenarios.append(new_game)
        game_geode_scores.append(max([g.get_geode_score() * (i+1) for g in finished_games]))
        print(game_geode_scores[-1])
    print("1:", sum(game_geode_scores))
    print("2:", "")

def parse_lines(lines: List[str]) -> List[Tuple[int, int, int]]:
    pattern = re.compile(r"Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
    blueprints = []

    for line in lines:
        groups = pattern.match(line).groups()
        blueprints.append(Blueprint(
            ore_robot_cost=(int(groups[0]), 0, 0),
            clay_robot_cost=(int(groups[1]), 0, 0),
            obsidian_robot_cost=(int(groups[2]), int(groups[3]), 0),
            geode_robot_cost=(int(groups[4]), 0, int(groups[5])),
        ))

    return blueprints
    

if __name__ == "__main__":
    main()