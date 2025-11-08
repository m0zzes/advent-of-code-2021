from aoc.base_problem import BaseProblem
from aoc.common.grid import Grid


def observe_flash_wave_r(x: int, y: int, grid: Grid) -> None:
    flashing_neighbours = []

    # Retrieve all adjacent tiles, exclude flashed neighbours
    neighbours = grid.neighbours(x, y, True, ["0"])
    for xn, yn, value_n in neighbours:
        energy_level = int(value_n) + 1
        if energy_level > 9:
            energy_level = 0
            flashing_neighbours.append((xn, yn))
        grid.set(xn, yn, str(energy_level))

    for n in flashing_neighbours:
        observe_flash_wave_r(n[0], n[1], grid)

def increment_energy_levels(grid: Grid) -> dict[str,int]:

    # increment energy levels
    for point in grid.points:
        next_level = int(point[2]) + 1
        if next_level > 9:
            next_level = 0
        grid.set(point[0], point[1], str(next_level))

    # Simulate flash waves
    for x, y, value in grid.points:
        if value != "0":
            continue
        observe_flash_wave_r(x, y, grid)

    has_flashed = [p for p in grid.flat() if p == "0"]

    is_sync = 0
    if len(has_flashed) == len(grid.points):
        is_sync = 1

    return {
        "flashed_n" : len(has_flashed),
        "is_sync" : is_sync
    }

class Problem11(BaseProblem):

    def parse_grid(self) -> Grid:

        grid: Grid = Grid()

        for line in self.input_data:
            row = []
            for c in line:
                row.append(c)
            grid.data.append(row)

        return grid

    def part_one(self) -> str:

        grid: Grid = self.parse_grid()

        if self.verbose:
            grid.print()

        outputs = grid.simulate(
            f=increment_energy_levels,
            f_args=[grid],
            iterations=100,
            debug=self.verbose,
            debug_sleep_s=0.1
        )

        return str(sum([o["flashed_n"] for o in outputs]))

    def part_two(self) -> str:

        grid: Grid = self.parse_grid()

        if self.verbose:
            grid.print()

        outputs = grid.simulate(
            f=increment_energy_levels,
            f_args=[grid],
            iterations=300,
            debug=self.verbose,
            debug_sleep_s=0.1
        )

        # Find first sync
        for i, o in enumerate(outputs):
            if o["is_sync"]:
                return str(i+1)

        return ""