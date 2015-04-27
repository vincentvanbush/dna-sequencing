from solver import Solution

def create_initial_solution(instance):

	oligos = instance.oligos
	result_length = instance.result_length

	sequence = ''
	overlaps = []
	used_oligos_count = 0

	overlaps_pairs = {}
	
	for oligo1 in oligos:
		overlaps_pairs[oligo1] = {}
		for oligo2 in oligos:
			if oligo1 != oligo2:
				overlaps_pairs[oligo1][oligo2] = oligo1.overlap(oligo2)
	
	# for oligo1 in overlaps_pairs:
	# 	for oligo2 in overlaps_pairs[oligo1]:
	# 		print oligo1, oligo2
	# 		print overlaps_pairs[oligo1][oligo2]

	in_edges_for_nucs = {}
	for oligo in oligos:
		in_edges_for_nucs[oligo] = 0
	
	for oligo1 in overlaps_pairs:
		for oligo2 in overlaps_pairs[oligo1]:
			in_edges_for_nucs[oligo2] += overlaps_pairs[oligo1][oligo2]
	
	oligo_with_min_in_edges = oligos[0]
	min_in_edges_val = in_edges_for_nucs[oligo_with_min_in_edges]
	
	for oligo in in_edges_for_nucs:
		if in_edges_for_nucs[oligo] < min_in_edges_val:
			min_in_edges_val = in_edges_for_nucs[oligo]
			oligo_with_min_in_edges = oligo

	# print oligo_with_min_in_edges.nuc
	# print min_in_edges_val




	
		


	return Solution()
