# Introduction to Bioinformatics
# Project-2: Sequence Alignment (Pairwise Alignment)
# Implement Pairwise Alignment for an equivalent gene in SARS and MERS
# Assigned Gene: S
# SARS_COV_2 Range: [21563:25384], MERS_COV Range: [21456:25517]
import os

from Mutations import count as countMutations
from NeedlemanWunsch import (ScoringCriteria, alignmentTable, optimalAlignment,
                             score, writeAlignmentToFile, writeTableToFile)

if __name__ == "__main__":
    log_flag = False

    scoring_criteria = ScoringCriteria(1, -1, -2)

    sars_filename = "Data/SARS_COV_2.fasta"
    mers_filename = "Data/MERS_COV.fasta"

    sars_file = open(sars_filename, "r")
    mers_file = open(mers_filename, "r")

    sars_comment = sars_file.readline()
    mers_comment = mers_file.readline()

    print("Retrieving Genomes from: " + sars_filename + " " + mers_filename)
    sars_genome = sars_file.read()
    mers_genome = mers_file.read()

    sars_genome = sars_genome.replace("\n", "")
    mers_genome = mers_genome.replace("\n", "")

    print("Isolating the S gene from the genomes")
    sars_s = sars_genome[21562:25384]
    mers_s = mers_genome[21455:25517]

    print("Generating alignment table ...")
    table = alignmentTable(sars_s, mers_s, scoring_criteria)

    if log_flag:
        writeTableToFile("table.csv", table)
        print("Alignment table written to table.csv")

    alignment_score = score(table)
    print("Alignment score: {}".format(alignment_score))

    optimal_alignment = optimalAlignment(sars_s, mers_s, table)

    if log_flag:
        writeAlignmentToFile("alignment.txt", optimal_alignment)
        print("Optimal alignment written to alignment.txt")

    mutation_counts = countMutations(
        optimal_alignment[0], optimal_alignment[1])
    print("Mutations: {}".format(mutation_counts))

    print('done.')
