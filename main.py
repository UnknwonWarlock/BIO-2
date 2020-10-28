from NeedlemanWunsch import ScoringCriteria, genTable

scoring_criteria = ScoringCriteria(1, -1, -2)
sequence1 = "AAAC"
sequence2 = "AGC"

if __name__ == "__main__":
    table = genTable(sequence1, sequence2, scoring_criteria)
    print('done.')
