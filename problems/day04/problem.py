from aoc.base_problem import BaseProblem

class BingoBoard:
    """BingoBoard class describes and implements a bingo-board and helpful functions
    """

    def __init__(self):
        self.values: list[list[int]] = []

    def at(self, x:int, y: int) -> int:
        return self.values[y][x]

    def mark(self, number: int):

        for y in range(0, len(self.values)):
            for x in range(0, len(self.values[y])):
                if self.at(x,y) == number:
                    self.values[y][x] = -1

    def has_bingo(self):

        height = len(self.values)
        width = len(self.values[0])

        # Calculate vertical scores
        for x in range(0, width):
            column = [self.at(x,y) for y in range(0, height)]
            if column.count(-1) == height:
                return True

        # Check horizontal rows:
        for row in self.values:
            if row.count(-1) == width:
                return True

        return False

    def calculate_board(self) -> int:
        score: int = 0
        for row in self.values:
            for element in row:
                score += element if element != -1 else 0

        return score

class Problem4(BaseProblem):

    def parse_boards(self):
        """Parses the input lines into the correct Bingo Boards
        """

        boards = []
        current_board = None
        for i, line in enumerate(self.input_data):

            # Skip first line
            if i == 0:
                continue

            # Empty line, means we start with a new board
            if line == "":
                boards.append(current_board)
                current_board = BingoBoard()
                continue

            row = [int(e) for e in line.split(' ') if e != '']
            current_board.values.append(row)

        boards.append(current_board)
        boards.pop(0) # First board is undefined, remove it
        return boards

    def win_at_bingo(self, called_numbers: list[int], boards: list[BingoBoard]) -> int:
        """Finds the first board that wins at bingo, returns the winning score"""

        for value in called_numbers:
            for board in boards:
                board.mark(value)

                if board.has_bingo():
                    return value * board.calculate_board()

        return 0

    def lose_at_bingo(self, called_numbers: list[int], boards: list[BingoBoard]) -> int:
        """Finds the last board that wins at bingo, returns the winning score"""

        winners: list[BingoBoard] = []
        for value in called_numbers:

            players: list[BingoBoard] = [b for b in boards if b not in winners]
            for board in players:
                board.mark(value)

                if board.has_bingo():

                    # Last board to win
                    if len(players) == 1:
                        score = value * board.calculate_board()
                        return score

                    winners.append(board)

        return 0

    def part_one(self) -> str:

        called_numbers = [int(n) for n in self.input_data[0].split(',')]
        boards: list[BingoBoard] = self.parse_boards()

        return str(self.win_at_bingo(called_numbers, boards))

    def part_two(self) -> str:

        called_numbers = [int(n) for n in self.input_data[0].split(',')]
        boards: list[BingoBoard] = self.parse_boards()

        return str(self.lose_at_bingo(called_numbers, boards))