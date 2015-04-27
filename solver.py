class Solution:

    def __init__(self):
        self.sequence = ''
        self.overlaps = [] # (oligo1, oligo2, overlap_len, oligo1_starting_index)

    def used_oligos_count(self):
        return len(self.overlaps) + 1

class Instance:

    def __init__(self, oligos, result_length):
        self.oligos = oligos
        self.result_length = result_length
        self.solution = None

    def solve(self, pipeline):
        # for proc in pipeline:
        #     self.solution = proc(self)

        # now only one procedure returning solution
        self.solution = pipeline[0](self)
        
        return self.solution
