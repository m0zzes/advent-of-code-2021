import time
import logging

logger = logging.getLogger(__name__)

class BaseProblem:

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        if self.verbose:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        logging.basicConfig(
            format="%(message)s",
            level=log_level
        )

    def debug(self, message) -> None:
        logger.debug(message)

    def read_input_file(self, input_file: str) -> list[str]:
        """Reads the given input-file and returns its lines"""

        with open(input_file, "r") as ifile:
            return [l.strip() for l in ifile.readlines()]

        return []

    def run(self, input_file: str, run_part_one: bool = True, run_part_two: bool = True) -> None:

        self.input_data = self.read_input_file(input_file)

        if run_part_one:
            t0 = time.time()
            answer = self.part_one()
            t1 = time.time() - t0
            print(f"Part 1: {answer}, Execution-time: {t1}s")

        if run_part_two:
            t0 = time.time()
            answer = self.part_two()
            t1 = time.time() - t0
            print(f"Part 2: {answer}, Execution-time: {t1}s")


    def part_one(self) -> str:
        """Solves part one of the problem using the input file
        """
        return "NotImplemented"

    def part_two(self) -> str:
        """Solves part two of the problem using the input file
        """
        return "NotImplemented"