from aoc.base_problem import BaseProblem
from aoc.common.grid import Grid
from math import prod

def find_low_points(cave) -> list[tuple[int, int]]:
    """Find all low points in a cave"""

    low_points = []
    for x in range(0, cave.width):
        for y in range(0, cave.height):

            point = cave.at(x, y)
            neighbours = cave.neighbours(x, y)
            high_neighbours = [n for n in neighbours if int(n[2]) > int(point)]

            # corners
            if ((x == 0) or (x == cave.width - 1)) and ((y == 0) or (y == cave.height - 1)):
                if len(neighbours) == 2 and len(high_neighbours) == 2:
                    low_points.append((x, y))
                    continue

            # edges
            if (x == 0) or (x == cave.width - 1) or (y == 0) or (y == cave.height - 1):
                if len(neighbours) == 3 and len(high_neighbours) == 3:
                    low_points.append((x, y))
                    continue

            if len(neighbours) == 4 and len(high_neighbours) == 4:
                low_points.append((x, y))
                continue

    return low_points


def find_basin_size(cave: Grid, low_point: tuple[int,int]) -> int:
    """Finds basin size from a single low-point.
    """

    points_to_search = cave.neighbours(low_point[0], low_point[1], False, ["9"])
    marked: list = [low_point]

    while len(points_to_search) != 0:

        point = points_to_search.pop()

        neighbours = cave.neighbours(point[0], point[1], False, ["9"])
        points_to_search.extend([(x,y) for x,y,v in neighbours if (x,y) not in marked])

        marked.append((point[0], point[1]))
        marked = list(set(marked))

    return len(marked)

class Problem9(BaseProblem):

    def parse_intput(self) -> Grid:

        cave: Grid = Grid()
        for row in self.input_data:
            data = []
            for char in row:
                data.append(char)

            cave.data.append(data)

        return cave

    def part_one(self) -> str:

        cave = self.parse_intput()
        low_points = find_low_points(cave)

        return str(sum([int(cave.at(x,y)) + 1 for x,y in low_points]))

    def part_two(self) -> str:

        cave = self.parse_intput()
        low_points = find_low_points(cave)

        basins = []
        for lp in low_points:
            basins.append(find_basin_size(cave, lp))

        basins.sort(reverse=True)

        return str(prod([basins[0], basins[1], basins[2]]))