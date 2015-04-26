class Oligo:
    def __init__(self, nuc):
        self.nuc = nuc
        self.used = False

    @property
    def length(self):
        return len(self.nuc)

    def overlap(self, r_oli):
        if r_oli.length != self.length:
            raise Exception('Oligonucleotide lengths do not match')

        r_nuc = r_oli.nuc

        for i in range(self.length + 1):
            r_beginning = r_nuc[0:self.length-i]
            l_end = self.nuc[i:]
            if l_end == r_beginning:
                return len(l_end)

    def __str__(self):
        return self.nuc
