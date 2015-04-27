class Solution:

    def __init__(self):
        self.sequence = ''
        self.overlaps = [] # (oligo1, oligo2, overlap_len, o1_pos)

    def __init__(self, solution):
        self.sequence = solution.sequence
        self.overlaps = solution.overlaps

    def used_oligos_count(self):
        return len(self.overlaps) + 1

class Instance:

    def __init__(self, oligos, result_length):
        self.oligos = oligos
        self.result_length = result_length
        self.solution = None

    @property
    def oligo_length(self):
        return len(self.oligos[1].nuc)

    def solve(self, pipeline):
        for proc in pipeline:
            self.solution = proc(self)
        return self.solution
