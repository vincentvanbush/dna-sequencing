class Solution:

    def __init__(self):
        self.sequence = ''
        self.overlaps = []
        self.used_oligos_count = 0

class Instance:

    def __init__(self, oligos, result_length):
        self.oligos = oligos
        self.result_length = result_length
        self.solution = None

    def solve(self, pipeline):
        for proc in pipeline:
            self.solution = proc(self)
        return self.solution
