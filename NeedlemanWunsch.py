from array import array
from enum import Enum
from typing import List


class Direction(Enum):
    UP = 0
    LEFT = 1
    DIAGONAL = 2
    NONE = 4

    @staticmethod
    def name(dir) -> str:
        if dir == Direction.UP:
            return 'UP'
        if dir == Direction.LEFT:
            return 'LEFT'
        if dir == Direction.DIAGONAL:
            return 'DIAGONAL'
        if dir == Direction.NONE:
            return 'NONE'

        return '*ERROR*'


class ScoringCriteria:
    def __init__(self, match: int, mismatch: int, gap: int):
        self.MATCH = match
        self.MISMATCH = mismatch
        self.GAP = gap


class Cell:
    def __init__(self, score: int, direction: Direction):
        self.score = score
        self.direction = direction

    def __repr__(self):
        return "{} - {}".format(self.score, Direction.name(self.direction))


def alignmentTable(seq1: str, seq2: str, scoring: ScoringCriteria) -> List[List[int]]:
    table = []

    tmp = seq1
    seq1 = " " + seq2
    seq2 = " " + tmp

    for index1, char1 in enumerate(seq1):
        row = []
        for index2, char2 in enumerate(seq2):

            # Top left corner of the table initializes to 0
            if index1 == 0 and index2 == 0:
                row.append(Cell(0, Direction.NONE))
                print(Cell(0, Direction.NONE), end=' | ')
                continue

            # Initialize to null in the case there is no cell
            # in that direction
            score_diagonal = None
            score_up = None
            score_left = None

            # If we are not in the top row and not in the left-most column
            if(index1 != 0 and index2 != 0):
                score_diagonal = table[index1 - 1][index2 - 1].score

                if(char1 == char2):
                    score_diagonal += scoring.MATCH
                else:
                    score_diagonal += scoring.MISMATCH

            # If we are not in the top row
            if(index1 != 0):
                score_up = table[index1 - 1][index2].score + scoring.GAP

            # If we are not in the left-most row
            if(index2 != 0):
                score_left = row[index2 - 1].score + scoring.GAP

            # Find max score of the three options
            # NOTE: This is really gross because `max` cannot handle null values
            max_score = max(
                score_diagonal if score_diagonal is not None else float(
                    '-inf'),
                score_up if score_up is not None else float('-inf'),
                score_left if score_left is not None else float('-inf')
            )

            # Find the direction of the smallest score
            direction = Direction.NONE

            if max_score == score_diagonal:
                direction = Direction.DIAGONAL
            elif max_score == score_up:
                direction = Direction.UP
            elif max_score == score_left:
                direction = Direction.LEFT

            row.append(Cell(max_score, direction))
            print(Cell(max_score, direction), end=' | ')

        table.append(row)
        print()

    return table
