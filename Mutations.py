from typing import List, Tuple

proteins_table = {
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
    'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
    'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
    'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
    'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
    'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
    'TAC': 'Y', 'TAT': 'Y', 'TAA': '_', 'TAG': '_',
    'TGC': 'C', 'TGT': 'C', 'TGA': '_', 'TGG': 'W',
}


def chunk(input: str, size: int = 3) -> List[str]:
    return [input[i:i+size] for i in range(0, len(input), size)]


class MutationCounts:
    def __init__(self, indel: int, non_syn: int, syn: int):
        self.indel = indel
        self.non_syn = non_syn
        self.syn = syn

    def __repr__(self):
        return "Indel: {}, Non-Synonymous: {}, Synonymous: {}".format(
            self.indel, self.non_syn, self.syn)


def count(seq1: str, seq2: str) -> MutationCounts:
    chunks1 = chunk(seq1)
    chunks2 = chunk(seq2)

    num_indel = 0
    num_nonsyn_mutation = 0
    num_syn_mutation = 0

    for pair in zip(chunks1, chunks2):

        # Identical
        if pair[0] == pair[1]:
            continue

        # Check for indel
        has_indel = False
        for index, base in enumerate(pair[0]):
            if pair[0][index] == '_' or pair[1][index] == '_':
                num_indel += 1
                has_indel = True

        # If there was an indel, don't check for point mutation
        if has_indel:
            continue

        # Mutation codes for different proteins
        if proteins_table[pair[0]] != proteins_table[pair[1]]:
            num_nonsyn_mutation += 1
            continue

        # Mutation codes for same protein
        num_syn_mutation += 1

    return MutationCounts(num_indel, num_nonsyn_mutation, num_syn_mutation)
