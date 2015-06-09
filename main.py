import sys
import re
import solver
from solver import Instance
from annealing import simulated_annealing
from initial_heur import create_initial_solution
from oligo import Oligo

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
        lines = [l for l in lines if l != '']
        oligo_len = len(lines[0])
        result_length = oligo_len - 1 + int(m.group(1))
        
        
        print 'Instance has %d lines, result length = %s' % (len(lines), result_length)

        oligos = [Oligo(x) for x in lines]

        # based on what we've read, create the problem instance
        instance = Instance(oligos, result_length)
        solution = instance.solve([create_initial_solution, simulated_annealing], fname)

        if re.search('.+\+', fname) != None:
            desired_oligos_use = int(m.group(1))
        else:
            desired_oligos_use = len(instance.oligos)

            

        # percentage_use = (float(solution.used_oligos_count)/desired_oligos_use)*100.0
        percentage_use = (float(len(filter(lambda o: o.used, instance.oligos)))/desired_oligos_use)*100.0

        # print 'File name: %s' % fname
        print 'Used %d oligonucleotides' % solution.used_oligos_count
        print 'Sequence length is %d' % len(solution.sequence)
        print 'Use rates is %.2f%%' % percentage_use
        print ''

        sys.exit(0)
