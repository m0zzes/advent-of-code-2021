from aoc.base_problem import BaseProblem

def get_empty_school() -> dict[str, int]:
   """Returns a dictionary of an empty school of fish,
   all fish-ages are pre-defined and set to 0 for an
   empty school
   """

   return {
        "0":0,
        "1":0,
        "2":0,
        "3":0,
        "4":0,
        "5":0,
        "6":0,
        "7":0,
        "8":0
    }

class Problem6(BaseProblem):

    def parse_initial_school(self) -> dict[str,int]:
        """Parses the initial school of fish outside the submarine
        """

        initial_school = get_empty_school()

        for fish in self.input_data[0].split(","):
            initial_school[fish] += 1

        return initial_school

    def simulate_days(self, initial_school: dict[str,int], days_n: int) -> dict[str,int]:
        """Simulates the life-cycle of a school of fish for N days given its initial state.
        Returns a dictionary of all fish-ages after simulation has completed
        """

        current_population = initial_school
        for day_i in range(0, days_n):

            next_population = get_empty_school()
            for age, n in current_population.items():

                if n == 0:
                    continue
                elif age == "0":
                    next_population["8"] += n
                    next_population["6"] += n
                else:
                    next_population[str(int(age)-1)] += n

            current_population = next_population
            self.debug(current_population)

        return current_population

    def part_one(self) -> str:

        initial_school = self.parse_initial_school()
        current_school = self.simulate_days(initial_school, 80)

        return str(sum(current_school.values()))

    def part_two(self) -> str:

        initial_school = self.parse_initial_school()
        current_school = self.simulate_days(initial_school, 256)

        return str(sum(current_school.values()))