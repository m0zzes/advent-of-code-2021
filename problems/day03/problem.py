from itertools import count

from aoc.base_problem import BaseProblem

class Problem3(BaseProblem):

    def calculate_gamma_bit(self, index: int, values: list[str]) -> str:
        """Calculates the gamma-bit for the values at given index,
        The gamma-bit is deduced by taking the most common bit at index for all values.
        If the number of 1's and 0's are equal, the gamma-bit will always be 1
        """

        bits = [binary[index] for binary in values]
        one_n = bits.count("1")
        zero_n = bits.count("0")

        return "1" if one_n >= zero_n else "0"

    def calculate_gamma_binary(self) -> str:
        """Calculates the gamma binary string
        """

        length: int = len(self.input_data[0])
        gamma_binary = ""
        for i in range(0, length):
            gamma_binary += self.calculate_gamma_bit(i, self.input_data)

        return gamma_binary

    def filter_diagnostics_report(self, override_to_least_common: bool = False):
        """Filters the binary string in the diagnostics report according to
        their most common bits, until only one remains. Its is possible to
        invert the filtering and use least-common matching instead.
        """

        filtered = self.input_data
        for b_index in range(0, len(filtered[0])):

            match_bit = self.calculate_gamma_bit(b_index, filtered)

            # Invert to least-common if specified
            if override_to_least_common:
                match_bit = "0" if match_bit == "1" else "1"

            filtered = [v for v in filtered if v[b_index] == match_bit]

            if len(filtered) == 1:
                return filtered[0]

        return ""

    def part_one(self) -> str:

        gamma_binary: str = self.calculate_gamma_binary()
        epsilon_binary = "".join("1" if b == "0" else "0" for b in gamma_binary) #Epsilon is the inverse of gamma

        gamma_value = int(gamma_binary, 2)
        epsilon_value = int(epsilon_binary, 2)

        return str(gamma_value * epsilon_value)

    def part_two(self) -> str:

        oxygen_rating_binary = self.filter_diagnostics_report()
        co_scrubber_rating_binary = self.filter_diagnostics_report(override_to_least_common=True)

        oxygen_rating_value = int(oxygen_rating_binary, 2)
        co_scrubber_rating_value = int(co_scrubber_rating_binary, 2)

        return str(oxygen_rating_value * co_scrubber_rating_value)