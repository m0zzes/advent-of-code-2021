from aoc.base_problem import BaseProblem
from aoc.common.nodegraph import Node, Edge, depth_first_search

from copy import copy

class Problem12(BaseProblem):

    def parse_graph(self) -> dict[str, Node]:

        parsed_nodes = {}
        for line in self.input_data:
            source_label, destination_label = line.split("-")

            source_node = parsed_nodes.get(source_label, None)
            if not source_node:
                weight = 1 if source_label.islower() else 100
                source_node = Node(source_label, weight)
                parsed_nodes[source_label] = source_node

            destination_node = parsed_nodes.get(destination_label, None)
            if not destination_node:
                weight = 1 if destination_label.islower() else 100
                destination_node = Node(destination_label, weight)
                parsed_nodes[destination_label] = destination_node

            edge = Edge(
                label=line,
                weight=0,
                source=source_node,
                destination=destination_node
            )

            source_node.add_outgoing(edge)
            destination_node.add_incoming(edge)

        return parsed_nodes

    def part_one(self) -> str:

        nodes = self.parse_graph()
        paths = []
        current_path = []
        visited = {n.label: n.weight for n in nodes.values()}

        depth_first_search(nodes["start"], nodes["end"], visited, current_path, paths)

        return str(len(paths))

    def part_two(self) -> str:

        nodes = self.parse_graph()
        paths = []
        visited = {n.label:n.weight for n in nodes.values()}
        small_caves = [c for c in nodes.keys() if c.islower() and c not in ["start", "end"]]

        # We calculate all the paths through the graph
        # for each small cave with 1 more allowed pass,
        # this method is simple, but will result in double
        # calculation for some paths
        for sc in small_caves:
            current_path = []
            visited_snapshot = copy(visited)
            visited_snapshot[sc] += 1

            depth_first_search(nodes["start"], nodes["end"], visited_snapshot, current_path, paths)

        # We remove duplicate paths
        unique = set(["-".join(p) for p in paths])
        return str(len(unique))