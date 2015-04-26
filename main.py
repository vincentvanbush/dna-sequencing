import sys
import re
import solver
from solver import Instance
from annealing import simulated_annealing
from initial_heur import create_initial_solution

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Please enter instance filename for the problem'
        sys.exit(1)
    else:
        fname = sys.argv[1]
        try:
            f = open(fname, 'r')
        except IOError as e:
            print "Error: " + e.strerror
            sys.exit(1)

        # infer the length of desired result from filename
        m = re.search('[0-9]+\.([0-9]+)', fname)
        lines = f.read().split('\n')
        oligo_len = len(lines[0])
        result_length = oligo_len - 1 + int(m.group(1))

        print 'Instance has %d lines, result length = %s' % (len(lines), result_length)

        # based on what we've read, create the problem instance
        instance = Instance(lines, result_length)
        solution = instance.solve([create_initial_solution, simulated_annealing])

        print 'Used %d oligonucleotides' % solution.used_oligos_count
        print solution.sequence
        sys.exit(0)
