from aoc.base_problem import BaseProblem

class Problem1(BaseProblem):

    def window_score(self, start_index: int, size: int = 3) -> int:
        """Calculates the sliding window score for a given index and window size"""
        result = 0
        for i in range(0, size):

            # return -1 if sliding windows cannot be calculated
            if start_index + i >= len(self.input_data):
                return -1

            result += int(self.input_data[start_index + i])

        return result

    def calculate_windows(self, size: int = 3) -> int:

        previous_window_score: int = 0
        increases_n: int = 0
        for i in range(len(self.input_data)):

            window_score = self.window_score(i, size)

            if window_score == -1:
                return increases_n

            # Special case for first index
            if i == 0:
                previous_window_score = window_score

            if window_score < previous_window_score:
                self.debug(f"{window_score} (decreased)")
            elif window_score > previous_window_score:
                increases_n += 1
                self.debug(f"{window_score} (increased)")
            else:
                self.debug(f"{window_score} (unchanged)")

            previous_window_score = window_score

        return increases_n

    def part_one(self) -> str:
        return str(self.calculate_windows(1))

    def part_two(self) -> str:
        return str(self.calculate_windows(3))