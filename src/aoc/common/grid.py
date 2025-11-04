import os
from dataclasses import dataclass

@dataclass
class Line:
    coordinates: list[tuple[int,int]]

class Grid:
    """Defines any kind of board/grid or map that have x and y coordinates.
    These kind of setups are very common in Advent of Code problems. And it is therefore
    efficient to create a common Grid type that can be reused instead of redefining for each problem.

    It is possible to initialize the grid with elements from start, if init_width and init_height are defined
    """

    def __init__(self, init_width: int = None, init_height: int = None, init_char: str = '.'):

        if (not init_width) or (not init_height):
            self.data: list[list[str]] = []
        else:
            self._init_grid(init_width, init_height, init_char)

    def _init_grid(self, w: int, h: int, init_char: str):
        self.data = []
        for i in range(0, h):
            self.data.append([init_char for i in range(0, w)])

    @property
    def height(self):
        return len(self.data)

    @property
    def width(self):
        return len(self.data[0])

    def at(self, x, y):
        return self.data[y][x]

    def set(self, x, y, value):
        self.data[y][x] = value

    def set_line_func(self, line: Line, func):
        for point in line.coordinates:
            value = func(point[0], point[1])
            self.set(point[0], point[1], value)

    def set_line(self, line: Line, value):
        for point in line.coordinates:
            self.set(point[0], point[1], value)

    def neighbours(self, x, y, diagonal: bool = False, exclude: list[str] = []) -> list[tuple[int,int,str]]:
        """Returns a list of neighbours, their coordinates and values.
        Diagonal tiles are not counted as neighbours by default.
        Values/Walls/Collision-boxes can be excluded by using exclude list
        """

        result = []
        for xn in [x - 1, x, x + 1]:
            for yn in [y - 1, y, y + 1]:

                # skip itself
                if xn == x and yn == y:
                    continue

                # out-of-bounds
                if xn < 0 or yn < 0 or xn >= len(self.data[0]) or yn >= len(self.data):
                    continue

                # skip diagonal-neighbours if not selected
                if (not diagonal) and abs(x - xn) == 1 and abs(y - yn) == 1:
                    continue

                point = self.at(xn, yn)
                if point in exclude:
                    continue

                result.append((xn,yn,point))

        return result


    def flat(self) -> list[str]:
        """Returns the grid values in a flat format
        useful for counting positions.
        """
        result = []
        for row in self.data:
            result.extend(row)

        return result

    def print(self):
        """Prints the grid at its current state
        """

        for row in self.data:
            print("".join(row))

    def interact(self, f):
        """Interactive view, prints the grid in between function f calls
        """

        while True:

            # Clear screen
            os.system("clear")
            self.print()

            c = input('>')
            if c == 'q':
                return

            f() # Function call