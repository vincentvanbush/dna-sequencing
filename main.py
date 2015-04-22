import sys
import re
import solver

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
        (solution, used) = solver.solve(lines, result_length)

        print 'Used %d oligonucleotides' % used
        print solution
        sys.exit(0)
