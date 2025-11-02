from aoc.base_problem import BaseProblem
from dataclasses import dataclass

@dataclass
class Submarine:
    horizontal: int = 0
    depth: int = 0
    aim: int = 0

@dataclass
class Instruction:
    heading: str
    value: int

class Problem2(BaseProblem):

    def parse_instructions(self) -> list[Instruction]:
        """Parses the input data into submarine instructions
        Each instruction consists of two parts, the heading and the value
        """
        instructions = []
        for line in self.input_data:
            parts = line.split(' ')
            instructions.append(Instruction(parts[0], int(parts[1])))

        return instructions

    def part_one(self) -> str:

        instructions = self.parse_instructions()
        submarine = Submarine()

        for instruction in instructions:

            if instruction.heading == "forward":
                submarine.horizontal += instruction.value
            elif instruction.heading == "up":
                submarine.depth -= instruction.value
            elif instruction.heading == "down":
                submarine.depth += instruction.value
            else:
                self.debug(f"Incorrect instruction {instruction}")

        return str(submarine.depth * submarine.horizontal)

    def part_two(self) -> str:

        instructions = self.parse_instructions()
        submarine = Submarine()

        for instruction in instructions:

            if instruction.heading == "forward":
                submarine.horizontal += instruction.value
                submarine.depth += submarine.aim * instruction.value
            elif instruction.heading == "up":
                submarine.aim -= instruction.value
            elif instruction.heading == "down":
                submarine.aim += instruction.value
            else:
                self.debug(f"Incorrect instruction {instruction}")

            s = 1

        return str(submarine.depth * submarine.horizontal)
