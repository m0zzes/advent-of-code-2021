from aoc.base_problem import BaseProblem
from aoc.common.grid import Grid

def fold_grid(grid: Grid, fold_x: int = -1, fold_y: int = -1, init_char: str = "."):
    """Folds a grid at the given fold_y or fold_x lines.
    LIMITATION: Cannot fold both x and y at the same time, one has to be 0

    When folding a large area onto a smaller one, we need to prepend some row or columns,
    otherwise points are lost 'out-of-bounds'.
    """

    if fold_x != -1 and fold_y != -1:
        raise Exception("Cannot fold both direction at the same time.")

    if fold_x == -1 and fold_y == -1:
        raise Exception("No fold lines were passed.")

    # Prepend to grid, when folding a large area
    if fold_y != -1 and fold_y < int(grid.height / 2):
        out_of_bounds = grid.height - fold_y
        for i in range(0, out_of_bounds):
            grid.new_row(0, init_char)

    if fold_x != -1 and fold_x < int(grid.width / 2):
        out_of_bounds = grid.width - fold_x
        for i in range(0, out_of_bounds):
            grid.new_column(0, init_char)

    for x,y,c in grid.points:

        if (c != "#") or (y <= fold_y) or (x <= fold_x):
            continue

        delta_x = abs(x - fold_x) if fold_x != -1 else 0
        delta_y = abs(y - fold_y) if fold_y != -1 else 0

        new_x = x if fold_x == -1 else fold_x - delta_x
        new_y = y if fold_y == -1 else fold_y - delta_y

        grid.set(new_x, new_y, "#")
        grid.set(x, y, init_char)

    # Delete row and columns that were folded over
    if fold_y != -1:
        out_of_bounds = grid.height - fold_y
        for i in range(0, out_of_bounds):
            grid.delete_row(-1)

    if fold_x != -1:
        out_of_bounds = grid.width - fold_x
        for i in range(0, out_of_bounds):
            grid.delete_column(-1)

class Problem13(BaseProblem):

    def parse_input(self, init_char: str) -> tuple[Grid, list[tuple[str,int]]]:

        points = []
        folds = []
        parse_switch: bool = False
        for line in self.input_data:

            if not parse_switch:

                if not line:
                    parse_switch = True
                    continue

                x,y = line.split(",")
                points.append((int(x), int(y)))

            else:
                fold_instruction = line.split()[-1]
                direction, value = fold_instruction.split("=")
                folds.append((direction, int(value)))

        grid = Grid(
            max([x for x,y in points]) + 1,
            max(y for x,y in points) + 1,
            init_char
        )

        for x,y in points:
            grid.set(x,y,"#")

        return grid, folds

    def part_one(self) -> str:

        init_char = " "
        grid, folds = self.parse_input(init_char)

        direction, value = folds[0]
        if direction == "x":
            fold_grid(grid, value, -1, init_char)
        else:
            fold_grid(grid, -1, value, init_char)

        return str(len([p for p in grid.points if p[2] == "#"]))

    def part_two(self) -> str:

        init_char = " "
        grid, folds = self.parse_input(init_char)

        for direction, value in folds:
            if direction == "x":
                fold_grid(grid, value, -1, init_char)
            else:
                fold_grid(grid, -1, value, init_char)

        grid.print()

        return "Human eyes required to observer results"
