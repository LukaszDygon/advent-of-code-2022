from __future__ import annotations

from aoc_helpers import input_helper
from typing import Dict, Union, List

class FileNode:
    def __init__(self, name: str, size: int, parent: DirectoryNode=None):
        self.name = name
        self.size = size
        self.parent = parent

    def get_size(self):
        return self.size
    def __repr__(self):
        return f"FileNode({self.name}, {self.size}, {self.parent})"

class DirectoryNode:
    def __init__(self, name: str = "/", parent: DirectoryNode=None):
        self.name = name
        self.parent = parent
        self.children: Dict[str, Union[DirectoryNode, FileNode]] = {}

    def __repr__(self):
        return f"DirectoryNode({self.name})"

    def add_node(self, node):
        self.children[node.name] = node

    def get_node(self, name) -> Union[DirectoryNode, FileNode]:
        return self.children[name]

    def get_size(self) -> int:
        return sum([child.get_size() for child in self.children.values()])
    
def main():
    lines = input_helper.get_lines(7)
    file_system = scan_file_system(lines)
    dir_sizes = crawl_file_system(file_system)
    total_space = 70_000_000
    required_space = 30_000_000
    free_space = total_space - file_system.get_size()
    space_needed = required_space - free_space
    print("1:", sum([dir for dir in dir_sizes if dir < 100_000]))
    print("2:", min([dir for dir in dir_sizes if dir > space_needed]))

def scan_file_system(lines: List[str]) -> DirectoryNode:
    root = DirectoryNode()
    current_node = root
    i = 1
    while i < len(lines):
        command = lines[i].split(" ")
        if command[1] == "cd":
            if command[2] == "..":
                current_node = current_node.parent
            else:
                current_node = current_node.get_node(command[2])
            i += 1
        elif command[1] == "ls":
            i += 1
            while i < len(lines) and lines[i][0] != "$":
                item = lines[i].split(" ")
                if item[0] == "dir":
                    current_node.add_node(DirectoryNode(item[1], current_node))
                else:
                    current_node.add_node(FileNode(item[1], int(item[0]), current_node))
                i += 1
        else:
            raise Exception("Invalid command")
    return root
            
def crawl_file_system(root: DirectoryNode) -> List[int]:
    print(root)
    sizes = [root.get_size()]
    for child in [child for child in root.children.values() if isinstance(child, DirectoryNode)]:
        sizes += crawl_file_system(child)
    return sizes


if __name__ == "__main__":
    main()