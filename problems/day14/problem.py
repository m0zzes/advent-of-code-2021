from aoc.base_problem import BaseProblem
from math import floor

def alphabet_in_polymer(polymer: dict[str, int], start: str, end: str) -> dict[str, int]:
    """Constructs the alphabet from a polymer, and counts each letter. Every letter except the start and end,
    will be counted twice, therefore these conflicts need to be resolved in order to count accurately.
    """

    alphabet = {}

    for pair, N in polymer.items():
        letter_a = pair[0]
        letter_b = pair[1]

        if alphabet.get(letter_a, None):
            alphabet[letter_a] += N
        else:
            alphabet[letter_a] = N


        if alphabet.get(letter_b, None):
            alphabet[letter_b] += N
        else:
            alphabet[letter_b] = N

    # Remove duplicates
    for letter, N in alphabet.items():

        if letter in [start, end]:
            alphabet[letter] = int(floor(N / 2)) + 1
        else:
            alphabet[letter] = int(N / 2)

    return alphabet

def parse_polymer_string(polymer_string: str) -> dict[str, int]:
    """Parses a polymer from its string form into its dictionary form"""

    polymer = {}

    for i in range(len(polymer_string) - 1):
        pair = polymer_string[i] + polymer_string[i + 1]

        if polymer.get(pair, None):
            polymer[pair] += 1
        else:
            polymer[pair] = 1

    return polymer

def expand_polymer(polymer: dict[str, int], insertion_map: dict[str, list[str]]) -> dict[str, int]:
    """Expands a given polymer (dictionary of pairs) and expands it using an insertion map
    """

    new_polymer = {}
    for pair, N in polymer.items():

        new_pairs = insertion_map[pair]
        for new_pair in new_pairs:

            if new_polymer.get(new_pair, None):
                new_polymer[new_pair] += N
            else:
                new_polymer[new_pair] = N

    return new_polymer

def construct_insertion_map(insertion_rules: list[str]) -> dict[str, list[str]]:
    """Constructs a map with all pairs and their expanded form from the insertion rules given in input
    """

    insertion_map = {}
    for rule in insertion_rules:
        parts = rule.split()

        pair = parts[0]
        pair_parts = list(pair)
        insertion = parts[-1]

        insertion_map[pair] = [pair_parts[0] + insertion, insertion + pair_parts[1]]

    return insertion_map

class Problem14(BaseProblem):

    def part_one(self) -> str:

        polymer_string = self.input_data[0]
        polymer = parse_polymer_string(polymer_string)
        insertion_rules = construct_insertion_map(self.input_data[2:])

        N = 10
        for i in range(N):
            polymer = expand_polymer(polymer, insertion_rules)

        alphabet = alphabet_in_polymer(polymer, polymer_string[0], polymer_string[-1])

        return str(max(alphabet.values()) - min(alphabet.values()))

    def part_two(self) -> str:

        polymer_string = self.input_data[0]
        polymer = parse_polymer_string(polymer_string)
        insertion_rules = construct_insertion_map(self.input_data[2:])

        N = 40
        for i in range(N):
            polymer = expand_polymer(polymer, insertion_rules)

        alphabet = alphabet_in_polymer(polymer, polymer_string[0], polymer_string[-1])

        return str(max(alphabet.values()) - min(alphabet.values()))