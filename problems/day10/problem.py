from aoc.base_problem import BaseProblem
from dataclasses import dataclass

@dataclass
class LineState:
    isCorrupted: bool
    last_char: str
    stack_trace: list[str]

class SyntaxRelationMap:
    """Bidirectional dictionary for syntax pairs. In reality there is probably a better way
    of solving this problem, than using this random self-defined class. But I thought it was nice
    to make something fun.
    """

    def __init__(self, syntax_pairs: list[tuple[str,str]]):
        self.syntax_pairs = syntax_pairs

    def __getitem__(self, key: str) -> str:

        for p1, p2 in self.syntax_pairs:
            if p1 == key:
                return p2
            elif p2 == key:
                return p1

        raise Exception(f"No such item {key}")

    def is_pair(self, key: str, value: str) -> bool:
        for p1, p2 in self.syntax_pairs:
            if (p1 == key and p2 == value) or (p2 == key and p1 == value):
                return True
        return False

    def keys(self) -> list[str]:
        return [p1 for p1,p2 in self.syntax_pairs]

    def values(self) -> list[str]:
        return [p2 for p1, p2 in self.syntax_pairs]


def syntax_checker(line: str, relation_map: SyntaxRelationMap) -> LineState:
    """Checks the syntax by going through each chunk in the line and searching for incorrect closing of chunks.
    The given relations-dict will determine how the syntax-checking occurs.

    Returns a LineState containing syntax debugging information
    """

    opening_chars: list[str] = relation_map.keys()
    closing_chars: list[str] = relation_map.values()
    stack: list[str] = []

    for i, c in enumerate(line):

        # If opening chunk, save in stack
        if c in opening_chars:
            stack.append(c)
            continue

        # Exit if incorrect state
        if (c in closing_chars) and (len(stack) < 1 or not relation_map.is_pair(c, stack[-1])):
            return LineState(True, c, stack)

        # Close chunk
        stack.pop(-1)

    return LineState(False, line[-1], stack)

def autocomplete(stack: list[str], relation_map: SyntaxRelationMap) -> str:
    """Autocorrects an incomplete chunk-string, by closing the chunks in the right order
    """

    completion: str = ""

    for open_c in reversed(stack):
        completion += relation_map[open_c]

    return completion

def calculate_completion_score(completion_string: str, completion_score_map: dict[str,int]) -> int:
    """Calculates the completion score for a given completion string
    """

    base_multiplier: int = 5
    total_score: int = 0
    for c in completion_string:
        total_score *= base_multiplier
        total_score += completion_score_map[c]

    return total_score

def get_syntax_relation_map() -> SyntaxRelationMap:
    return SyntaxRelationMap([
        ("(", ")"),
        ("[", "]"),
        ("{", "}"),
        ("<", ">")
    ])


class Problem10(BaseProblem):

    def part_one(self) -> str:

        relation_map: SyntaxRelationMap = get_syntax_relation_map()
        syntax_scores = {
            ")" : 3,
            "]" : 57,
            "}" : 1197,
            ">" : 25137
        }

        lines = self.input_data
        score: int = 0

        for line in lines:
            state: LineState = syntax_checker(line, relation_map)

            if state.isCorrupted:
                self.debug(f"Found corrupted chunk. last_char={state.last_char}")
                score += syntax_scores[state.last_char]

        return str(score)

    def part_two(self) -> str:

        relation_map: SyntaxRelationMap = get_syntax_relation_map()
        completion_scores = {
            ")" : 1,
            "]" : 2,
            "}" : 3,
            ">" : 4
        }

        lines = self.input_data
        scores: list[int] = []

        for line in lines:
            state: LineState = syntax_checker(line, relation_map)

            if not state.isCorrupted:
                completion_string = autocomplete(state.stack_trace, relation_map)
                scores.append(calculate_completion_score(completion_string, completion_scores))

        return str(sorted(scores)[int(len(scores)/2)])