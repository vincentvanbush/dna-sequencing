from solver import Solution

def create_initial_solution(instance):

	oligos = instance.oligos
	result_length = instance.result_length
	oligos_len = len(oligos[0].nuc)

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

	current_oligo = oligo_with_min_in_edges
	current_oligo.used = True
	left_oligo_ind_in_seq = 0
	sequence += current_oligo.nuc

	while len(sequence) < result_length: # poprawic warunek
		max_overlap = 0
		oligo_with_max_overlap = None
		for oligo2 in overlaps_pairs[current_oligo]:
			if overlaps_pairs[current_oligo][oligo2] > max_overlap and oligo2.used == False:
				max_overlap = overlaps_pairs[current_oligo][oligo2]
				oligo_with_max_overlap = oligo2
		if oligo_with_max_overlap != None:
			oligo_with_max_overlap.used = True
			sequence += oligo_with_max_overlap.nuc[max_overlap:]
			overlaps.append((current_oligo, oligo_with_max_overlap, max_overlap, left_oligo_ind_in_seq))

			current_oligo = oligo_with_max_overlap
			left_oligo_ind_in_seq = left_oligo_ind_in_seq + oligos_len - max_overlap

		else:
			pass
			# sytuacja gdy nie mozna znalezc nastepnika

	# print sequence
	# for tup in overlaps:
	# 	o1, o2, ov, ind = tup
	# 	print o1, o2, ov, ind

	solution = Solution()
	solution.sequence = sequence
	solution.overlaps = overlaps

	return solution
