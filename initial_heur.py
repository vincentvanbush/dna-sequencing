from solver import Solution
import random
import re

def create_initial_solution(instance, path):

	oligos = instance.oligos
	result_length = instance.result_length
	oligos_len = len(oligos[0].nuc)

	overlaps_pairs = create_overlaps_hash(oligos)
	starting_oligo = choose_starting_oligo(oligos, overlaps_pairs)
	sequence, overlaps = make_starting_solution(starting_oligo, result_length, oligos_len, overlaps_pairs)

	solution = Solution()
	solution.sequence = sequence
	solution.overlaps = overlaps

	log_to_file (solution, overlaps, sequence, oligos_len, path)

	return solution

def create_overlaps_hash (oligos):
	overlaps_pairs = {}
	
	for oligo1 in oligos:
		overlaps_pairs[oligo1] = {}
		for oligo2 in oligos:
			if oligo1 != oligo2:
				overlaps_pairs[oligo1][oligo2] = oligo1.overlap(oligo2)

	return overlaps_pairs

def choose_starting_oligo_alternative (oligos, overlaps_pairs):
	max_left_overlaps = {}
	for oligo in oligos:
		max_left_overlaps[oligo] = 0

	for oligo1 in overlaps_pairs:
		for oligo2 in overlaps_pairs[oligo1]:
			if overlaps_pairs[oligo1][oligo2] > max_left_overlaps[oligo2]:
				max_left_overlaps[oligo2] = overlaps_pairs[oligo1][oligo2]

	# we are choosing for the starting oligo, this one which has minimal global left overlap among other oligos
	# in case of many minimal global left overlap we are choosing first meet oligo
	oligo_with_min_left_overlap = oligos[0]
	min_left_ovarlap = max_left_overlaps[oligo_with_min_left_overlap]
	for oligo in oligos:
		if max_left_overlaps[oligo] < min_left_ovarlap:
			oligo_with_min_left_overlap = oligo
			min_left_ovarlap = max_left_overlaps[oligo_with_min_left_overlap]

	return oligo_with_min_left_overlap


def choose_starting_oligo (oligos, overlaps_pairs):

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

	return oligo_with_min_in_edges

def make_starting_solution(starting_oligo, result_length, oligos_len, overlaps_pairs):
	sequence = ''
	overlaps = []

	current_oligo = starting_oligo
	current_oligo.used_times += 1
	left_oligo_ind_in_seq = 0
	sequence += current_oligo.nuc

	# print "-----------------------------------------------------"
	# print "We are creating initial solution"
	# print "Oligo length is %d" % (len(current_oligo.nuc))
	# print "Desired sequence length is %d nucs" % (result_length)
	# print "-----------------------------------------------------"

	# searches starting sequence until its length is greater or equal desired length or until there ara no more unused oligos
	while len(sequence) < result_length:
		max_overlap = 0
		oligo_with_max_overlap = None
		for oligo2 in overlaps_pairs[current_oligo]:
			if overlaps_pairs[current_oligo][oligo2] > max_overlap and oligo2.used == False:
				max_overlap = overlaps_pairs[current_oligo][oligo2]
				oligo_with_max_overlap = oligo2
		if oligo_with_max_overlap != None:
			oligo_with_max_overlap.used_times += 1
			sequence += oligo_with_max_overlap.nuc[max_overlap:]
			overlaps.append((current_oligo, oligo_with_max_overlap, max_overlap, left_oligo_ind_in_seq))

			current_oligo = oligo_with_max_overlap
			left_oligo_ind_in_seq = left_oligo_ind_in_seq + oligos_len - max_overlap
		else:
			break
			
	second_while = False
	# if after first while, length of obtained sequence is less of desired length we glue yet used oligos
	while len(sequence) < result_length:
		second_while = True
		max_overlap = 0
		oligo_with_max_overlap = None
		for oligo2 in overlaps_pairs[current_oligo]:
			if overlaps_pairs[current_oligo][oligo2] > max_overlap:
				max_overlap = overlaps_pairs[current_oligo][oligo2]
				oligo_with_max_overlap = oligo2	
				# maybe we can break this loop if we find oligo with maximal possible overlap
		if oligo_with_max_overlap == None:
			oligo_with_max_overlap = random.choice(overlaps_pairs.keys())
		sequence += oligo_with_max_overlap.nuc[max_overlap:]
		overlaps.append((current_oligo, oligo_with_max_overlap, max_overlap, left_oligo_ind_in_seq))
		oligo_with_max_overlap.used_times += 1 # added this line because oligo is used one more time

		current_oligo = oligo_with_max_overlap
		left_oligo_ind_in_seq = left_oligo_ind_in_seq + oligos_len - max_overlap

	# we cut obtained sequence to exact length we want to get
	if len(sequence) > result_length:
		oligo_to_remove = overlaps[-1][1]
		# when we were in the second while loop we can't change used of last oligo to False because it was used somewhere erlier
		# if (not second_while):
		#	oligo_to_remove.used = False

		# now with used_times property we can just simply decrement used value
		oligo_to_remove.used_times -= 1
		overlaps = overlaps[0:-1]
		sequence = sequence[0:result_length]

	return sequence, overlaps

def log_to_file (solution, overlaps, sequence,  oligos_len, path):
	log_path = 'tests/sequence_' + path
	seq = open(log_path, 'a')


	m = re.search('[0-9]+\.([0-9]+)(\+|-)([0-9]+)', path)
	if re.search('.+\+', path) != None:
		desired_oligos_use = int(m.group(1))
	else:
		desired_oligos_use = int(m.group(1)) - int(m.group(3))
	percentage_use = (float(solution.used_oligos_count)/desired_oligos_use)*100.0
	seq.write('Used %d oligonucleotides\n' % solution.used_oligos_count)
	seq.write('Use rates is %.2f%%\n' % percentage_use)
	
	c = 0
	for i in xrange(len(sequence)):
		seq.write(sequence[i])
		c += 1
		if c % 50 == 0:
			seq.write('\n')
			c = 0

	seq.write('\n\n')

	shift = 0
	for tup in overlaps:
		shift = tup[3] % 100
		offset = shift * ' '
		seq.write(offset + tup[0].nuc + '\n')
	
	shift += oligos_len - overlaps[-1][2]
	offset = shift * ' '
	seq.write(offset + overlaps[-1][1].nuc + '\n')