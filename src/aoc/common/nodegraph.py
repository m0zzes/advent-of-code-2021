from dataclasses import dataclass
from copy import copy, deepcopy

class Node:

    def __init__(self, label: str, weight: int = -1):
        self.label = label
        self.weight = weight
        self.outgoing: list[Edge] = []
        self.incoming: list[Edge] = []

    def add_outgoing(self, edge):
        self.outgoing.append(edge)

    def add_incoming(self, edge):
        self.incoming.append(edge)


@dataclass
class Edge:
    label: str
    weight: int
    source: Node
    destination: Node

def depth_first_search(
        start: Node,
        end: Node,
        visited: dict[str,int],
        current_path: list[str],
        all_paths: list[list[str]]
) -> None:

    if visited[start.label] == 0:
        return

    visited[start.label] -= 1
    current_path.append(start.label)

    if start == end:
        all_paths.append(current_path)
        return

    next_destinations = [edge.destination for edge in start.outgoing] + [edge.source for edge in start.incoming]
    valid_destinations = [d for d in next_destinations if visited[d.label] != 0]
    for destination in valid_destinations:
        new_path = copy(current_path)
        new_visited = copy(visited)

        depth_first_search(destination, end, new_visited, new_path, all_paths)
