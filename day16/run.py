from __future__ import annotations
from aoc_helpers import input_helper
from typing import List, Tuple
import re


class Node:
    def __init__(self, name: str, flow_rate: int, tunnels: List[str]) -> None:
        self.name = name
        self.flow_rate = flow_rate
        self.edges: List[Tuple[str, int]] = [(tunnel, 2) for tunnel in tunnels] # 2 is the time to travel through a tunnel + opne the valve
    
    def remove_edge(self, edge: Node):
        new_edges = [e for e in self.edges if e[0] != edge.name]
        self.edges = new_edges

    def clone(self):
        return Node(self.name, self.flow_rate, [e[0] for e in self.edges])

    def __repr__(self):
        return f"Node({self.name}, {self.flow_rate})"

    def __eq__(self, other):
        if isinstance(other, Node):
            return ((self.name == other.name))
        else:
            return False
    
    def __hash__(self):
        return hash(self.name)


class Graph:

    def __init__(self, nodes: List[Node], starting_valve: str, time_total: int = 30, agents=1) -> None:
        self.nodes = {node.name: node for node in nodes}
        self.starting_valve = starting_valve
        self.total_time = time_total
        self.agents = agents
        self.candidates : List[Tuple[List[Node], int]]= []
        self.prune_edges()
        self.prune_nodes()
    
    def run(self):
        unvisited_nodes = self.nodes.copy()
        starting_node = unvisited_nodes.pop(self.starting_valve)
        trace = [starting_node]
        for edge in starting_node.edges:
            self.run_dfs(self.nodes[edge[0]], trace, unvisited_nodes, edge[1], 0)


    def run_dfs(self, node: Node, trace: List[Node], unvisited_nodes: List[str], time: int, total_flow: int):
        if time > self.total_time:
            self.candidates.append((trace, total_flow))
            return
        next_candidates = { e[0]: e for e in node.edges if e[0] in unvisited_nodes and e[0] != node.name }

        new_trace = trace.copy()
        new_trace.append(node)
        total_flow += node.flow_rate * (self.total_time - time)

        for edge_name, edge in next_candidates.items():
            self.run_dfs(self.nodes[edge_name], new_trace, next_candidates, time + edge[1], total_flow)
        
        self.candidates.append((new_trace, total_flow))

    def prune_edges(self):
        original_nodes = {n.name: n.clone() for n in self.nodes.values()}
        for node_name, node in self.nodes.items():
            nodes_to_visit = list(self.nodes.keys())
            nodes_to_visit.remove(node_name)
            while nodes_to_visit:
                unvisited_edges = [t for t in node.edges if t[0] in nodes_to_visit]
                for edge_name, edge_weight in unvisited_edges:
                    nodes_to_visit.remove(edge_name)
                    edge_node = original_nodes[edge_name]
                    for next_node_name, _ in edge_node.edges:
                        if next_node_name not in [e_name for e_name, _ in node.edges]:
                            node.edges.append((next_node_name, edge_weight+1))

        for node in self.nodes.values():
            for edge, _ in [e for e in node.edges if e[0]]:
                edge_node = self.nodes[edge]
                if edge_node.flow_rate == 0: 
                    node.remove_edge(edge_node)
                        
    def prune_nodes(self):
        new_nodes = {}
        for node_name in self.nodes.keys():
            node = self.nodes[node_name]
            if node.name == self.starting_valve or node.flow_rate > 0:
                new_nodes[node_name] = node
        self.nodes = new_nodes

    def get_best_candidate(self):
        return max(self.candidates, key=lambda x: x[1])

def main():
    lines = input_helper.get_lines(16)
    starting_valve = "AA"
    nodes = parse_input(lines)
    graph = Graph(nodes, starting_valve)
    graph.run()
    print("1:", graph.get_best_candidate()[1])
    print("2:", "")

def parse_input(lines: List[str]) -> List[Node]:
    pattern = re.compile(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
    parsed_input = []
    for line in lines:
        match = pattern.match(line)
        parsed_input.append(Node(match.group(1), int(match.group(2)), match.group(3).split(", ")))
    
    parsed_input.sort(key=lambda x: x.flow_rate, reverse=True)
    
    return parsed_input
if __name__ == "__main__":
    main()