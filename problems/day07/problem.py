from aoc.base_problem import BaseProblem

def optimal_crab_position(crabs: list[int], cost_func) -> int:
    low_position = min(crabs)
    high_position = max(crabs)

    fuel_costs = {}
    for pos in range(low_position, high_position + 1):
        fuel_costs[pos] = 0
        for cs in crabs:
            cost = cost_func(pos, cs)
            fuel_costs[pos] += cost

    return min(list(fuel_costs.values()))

def single_cost(a: int, b: int) -> int:
    return abs(a-b)

def accumulative_cost(a: int, b: int) -> int:
    delta = abs(a - b)
    return int( (delta * delta + delta) / 2 )

class Problem7(BaseProblem):

    def part_one(self) -> str:

        crabs_submarines = self.input_data[0].split(",")
        crabs_submarines = [int(cs) for cs in crabs_submarines]

        return str(optimal_crab_position(crabs_submarines, single_cost))

    def part_two(self) -> str:

        crabs_submarines = self.input_data[0].split(",")
        crabs_submarines = [int(cs) for cs in crabs_submarines]

        return str(optimal_crab_position(crabs_submarines, accumulative_cost))