class Solution:

    def __init__(self, solution=None):
        self.sequence = '' if solution == None else solution.sequence
        self.overlaps = [] # if solution == None else solution.overlaps
        # (oligo1, oligo2, overlap_len, oligo1_starting_index)

    @property
    def used_oligos_count(self):
        return len(self.overlaps) + 1

class Instance:

    def __init__(self, oligos, result_length):
        self.oligos = oligos
        self.oligos_dict = { o.nuc: o for o in oligos }
        self.result_length = result_length
        self.solution = None

    @property
    def oligo_length(self):
        return len(self.oligos[1].nuc)

    def solve(self, pipeline):
        for proc in pipeline:
            self.solution = proc(self)

        return self.solution
