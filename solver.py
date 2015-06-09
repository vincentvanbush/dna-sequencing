import re

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

    def solve(self, pipeline, path):
        for proc in pipeline:
            self.solution = proc(self, path)

        return self.solution

def log_to_file (instance, solution, overlaps, sequence,  oligos_len, path, time, stage):
    log_path = 'tests/sequence_' + path
    seq = open(log_path, 'a')


    m = re.search('[0-9]+\.([0-9]+)(\+|-)([0-9]+)', path)
    if re.search('.+\+', path) != None:
        desired_oligos_use = int(m.group(1))
    else:
        desired_oligos_use = int(m.group(1)) - int(m.group(3))
    # percentage_use = (float(solution.used_oligos_count)/desired_oligos_use)*100.0
    percentage_use = (float(len(filter(lambda o: o.used, instance.oligos)))/desired_oligos_use)*100.0
    if stage == 'INITIAL':
        seq.write('Initial solution\n')
        seq.write('Searching time: %.2f\n' % time)
    elif stage == 'ANNEALING':
        seq.write('Solution after annealing')
    seq.write('Used %d oligonucleotides\n' % len(filter(lambda o: o.used, instance.oligos)))
    seq.write('Use rates is %.2f%%\n' % percentage_use)

    c = 0
    for i in xrange(len(sequence)):
        seq.write(sequence[i])
        c += 1
        if c % 50 == 0:
            seq.write('\n')
            c = 0

    seq.write('\n\n')

    # result sequence with offsets
    # shift = 0
    # for tup in overlaps:
    #     shift = tup[3] % 100
    #     offset = shift * ' '
    #     seq.write(offset + tup[0].nuc + '\n')

    # shift += oligos_len - overlaps[-1][2]
    # offset = shift * ' '
    # seq.write(offset + overlaps[-1][1].nuc + '\n')
