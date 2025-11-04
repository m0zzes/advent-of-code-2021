from aoc.base_problem import BaseProblem
from dataclasses import dataclass

@dataclass
class Display:
    signals: list[str]
    outputs: list[str]

def number_of_common_wires(signal_a: str, signal_b: str) -> int:
    """Returns the number of common wires between two signals
    """
    return len( "".join( set(signal_a).intersection(signal_b) ) )

def shares_wires(signal: str, related_signals: list[tuple[str, int]]) -> bool:
    """Checks if given signal is related to given related_signals.
    - A signal is related to another if they share N number of wires.
    - A related signal consists of two parts: A signal, and the number of shared wires.

    If the given signal truly is related to all given "related signals", the functions true, else false
    """

    for rs,n in related_signals:
        if number_of_common_wires(signal, rs) != n:
            return False

    return True

def detangle_wires(display: Display) -> dict[str, str]:
    """Detangles the wires in a display and returns the resulting wire-schematic.
    Detangling the wires are pretty straight-forward:

    Numbers 1,4,7 and 8 use a unique number of wires, so they are easy to find.
    ex. If we find a signal that uses only two wires, it has to be a 1.

    Ones we have found the easy numbers, these can be used to deduce the rest. All the numbers int
    the 7-segment display, share some segments with eachother. It just so happens, that each of the "hard" numbers
    share a unique number of segments with (1,4,7,8).
    Ex. the number 2:
        - shares 1 wire with n=1
        - shares 2 wires with n=4
        - shares 2 wires with n=7
        - shares 5 wires with n=8

    These relations, are a unique signature/identifier of the number 4. If we see a signal, that has this signature,
    it has to be a 4. The rest of the numbers also have a unique relationship-signature,
    meaning we can deduce all the numbers by just using the easy ones.

    """

    schematic: dict[str,str] = {}

    # Deduce the easy numbers
    for signal in display.signals:
        if len(signal) == 2:
            schematic["1"] = signal
        elif len(signal) == 3:
            schematic["7"] = signal
        elif len(signal) == 4:
            schematic["4"] = signal
        elif len(signal) == 7:
            schematic["8"] = signal

    # Deduce the hard numbers
    for signal in display.signals:
        if len(signal) == 5:

            if shares_wires(signal, [
                (schematic["1"], 1),
                (schematic["4"], 2),
                (schematic["7"], 2),
                (schematic["8"], 5)
            ]):
                schematic["2"] = signal

            elif shares_wires(signal, [
                (schematic["1"], 2),
                (schematic["4"], 3),
                (schematic["7"], 3),
                (schematic["8"], 5)
            ]):
                schematic["3"] = signal

            elif shares_wires(signal, [
                (schematic["1"], 1),
                (schematic["4"], 3),
                (schematic["7"], 2),
                (schematic["8"], 5)
            ]):
                schematic["5"] = signal

            else:
                raise Exception(f"Could not detangle signal {signal}")

        elif len(signal) == 6:

            if shares_wires(signal, [
                (schematic["1"], 1),
                (schematic["4"], 3),
                (schematic["7"], 2),
                (schematic["8"], 6)
            ]):
                schematic["6"] = signal

            elif shares_wires(signal, [
                (schematic["1"], 2),
                (schematic["4"], 4),
                (schematic["7"], 3),
                (schematic["8"], 6)
            ]):
                schematic["9"] = signal

            elif shares_wires(signal, [
                (schematic["1"], 2),
                (schematic["4"], 3),
                (schematic["7"], 3),
                (schematic["8"], 6)
            ]):
                schematic["0"] = signal

            else:
                raise Exception(f"Could not detangle signal {signal}")

    return schematic

class Problem8(BaseProblem):

    def parse_input(self) -> list[Display]:
        """Parses input file into a list of signals and outputs
        """

        result: list[Display] = []
        for line in self.input_data:
            delimiter_parts = line.split('|')
            signals = delimiter_parts[0].split(' ')
            outputs = delimiter_parts[1].split(' ')

            result.append(Display(
                [s for s in signals if s != ''],
                [o for o in outputs if o != '']
            ))

        return result

    def part_one(self) -> str:

        lengths = [2, 4, 3, 7]

        data: list[Display] = self.parse_input()

        count = 0
        for display in data:
            for output in display.outputs:
                if len(output) in lengths:
                    count += 1

        return str(count)

    def part_two(self) -> str:

        data: list[Display] = self.parse_input()
        result: int = 0

        for display in data:
            schematic = detangle_wires(display)

            digits = []
            for output in display.outputs:
                o_sort = "".join(sorted(output))

                # Find correct signal
                for number, signal in schematic.items():
                    s_sort = "".join(sorted(signal))

                    if o_sort == s_sort:

                        digits.append(number)
                        break

            result += int("".join(digits))


            self.debug("".join(digits))

        return str(result)