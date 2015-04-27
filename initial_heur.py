from solver import Solution

def create_initial_solution(instance):

	oligos = instance.oligos
	result_length = instance.result_length

	sequence = ''
	overlaps = []
	used_oligos_count = 0

	overlaps_pairs = {}
	
	for oligo1 in oligos:
		for oligo2 in oligos:
			if oligo1 != oligo2:
				overlaps_pairs[(oligo1, oligo2)] = oligo1.overlap(oligo2)
	for o1, o2 in overlaps_pairs:
		print o1, o2
		print overlaps_pairs[(o1, o2)]
		


	return Solution()
