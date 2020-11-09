from array import array
from enum import Enum
from typing import List, Tuple

from Mutations import chunk


class Direction(Enum):
    UP = 0
    LEFT = 1
    DIAGONAL = 2
    NONE = 3

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


def score(table: List[List[int]]) -> int:
    return table[-1][-1].score


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

        table.append(row)

        progress = round(100 * (index1 + 1) / len(seq1), 2)
        progressStr = str(progress)[::-1].zfill(5)[::-1]
        print("{}%".format(progressStr), end="\r")

    print()
    return table


def optimalAlignment(seq1: str, seq2: str, table: List[List[int]]) -> (str, str):
    # rows and columns amounts
    rows = len(table) - 1
    columns = len(table[0]) - 1

    # check if the sequences are at least suitable in size for the table dimensions
    if rows != len(seq2) or columns != len(seq1):
        print("ERROR: Sequence lengths don't match table dimensions")
        return

    # start at the end of the table
    rows = -1
    columns = -1

    align1 = ""
    align2 = ""
    while True:
        entry = table[rows][columns]
        if entry.direction == Direction.DIAGONAL:
            align1 += seq1[columns]
            align2 += seq2[rows]
            rows -= 1
            columns -= 1
        elif entry.direction == Direction.LEFT:
            align1 += seq1[columns]
            align2 += "_"
            columns -= 1
        elif entry.direction == Direction.UP:
            align1 += "_"
            align2 += seq2[rows]
            rows -= 1
        elif entry.direction == Direction.NONE:
            break
        else:
            print("ERROR: bad direction found during traceback")
            return

    return (align1[::-1], align2[::-1])


def writeTableToFile(file_name: str, table: List[List[Cell]]) -> None:
    arrows = ['\u2B06', '\u2B05', '\u2196', '']

    f = open(file_name, "w")
    for row in table:
        for cell in row:
            f.write("{} {},".format(arrows[cell.direction.value], cell.score))
        f.write('\n')

    f.close()


def writeAlignmentToFile(file_name: str, alignment: Tuple[str, str], line_length: int = 80) -> None:
    chunk1 = chunk(alignment[0], line_length)
    chunk2 = chunk(alignment[1], line_length)

    f = open(file_name, "w")
    for index, pair in enumerate(zip(chunk1, chunk2)):
        f.write("{}-{}\n".format(index * line_length,
                                 index * line_length + len(pair[0])))
        f.write(pair[0] + '\n')
        f.write('|' * len(pair[0]) + '\n')
        f.write(pair[1] + '\n')
        f.write('\n')

    f.close()
