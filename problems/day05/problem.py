from aoc.base_problem import BaseProblem
from aoc.common.grid import Grid, Line

import re

def bresenham_line(x0: int, y0: int, x1: int, y1: int, ignore_diagonals: bool = False) -> Line:
    """Bresenham algorithm for plotting lines in a grid.
    Code is written from pseudo-code found in the Wikipedia-page about bresenham-lines
    """

    # Ignore diagonals, used in part 0
    if ignore_diagonals and abs(x0 - x1) != 0 and abs(y0 - y1) != 0:
        return Line([])

    positions: list[tuple[int,int]] = []

    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    error = dx + dy

    while True:
        positions.append((x0,y0))
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break

            error = error + dy
            x0 = x0 + sx

        if e2 <= dx:
            if y0 == y1:
                break

            error = error + dx
            y0 = y0 + sy

    return Line(positions)

class Problem5(BaseProblem):

    def parse_lines(self, ignore_diagonals: bool = False) -> tuple[int, int, list[Line]]:

        grid_width: int = 0
        grid_height: int = 0
        lines: list[Line] = []

        line_pattern = r"(\d+),(\d+) -> (\d+),(\d+)"
        for line in self.input_data:
            values = re.findall(line_pattern, line)[0]
            values = [int(c) for c in values]

            # Calculate if grid gets bigger
            grid_width = max([grid_width, values[0], values[2]])
            grid_height = max([grid_height, values[1], values[3]])

            lines.append(bresenham_line(values[0], values[1], values[2], values[3], ignore_diagonals))

        return grid_width, grid_height, lines

    def part_one(self):

        grid_width, grid_height, lines = self.parse_lines(True)
        grid = Grid(grid_width + 1, grid_height + 1)

        # Mark collisions
        for line in lines:
            grid.set_line_func(line, lambda x,y: "#" if grid.at(x,y) != "." else "1")

        return str(sum([1 for v in grid.flat() if v == "#"]))

    def part_two(self) -> str:

        grid_width, grid_height, lines = self.parse_lines(False)
        grid = Grid(grid_width + 1, grid_height + 1)

        # Mark collisions
        for line in lines:
            grid.set_line_func(line, lambda x, y: "#" if grid.at(x, y) != "." else "1")

        return str(sum([1 for v in grid.flat() if v == "#"]))
