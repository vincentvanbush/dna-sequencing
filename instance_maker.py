import sys
import random

def rand_nuc():
	oligo = random.randint(0, 3)
	nucs = { 0: 'A', 1: 'C', 2: 'G', 3: 'T' }
	return nucs[oligo]

if len(sys.argv) < 5:
	print 'Please enter required number of params for maker'
	sys.exit(1)
else:
	first_name_part = sys.argv[1]
	oligos_number = int(sys.argv[2])
	negatives = int(sys.argv[3])
	positives = int(sys.argv[4])

	result_errors = positives - negatives

	if result_errors <= 0:
		instance_name = first_name_part+'.'+str(oligos_number)+'-'+str(abs(result_errors))
	else:
		instance_name = first_name_part+'.'+str(oligos_number)+'+'+str(result_errors)
	

	oligo_length = 10
	seq_length = oligos_number + result_errors + oligo_length - 1
	sequence = ''

	first_oligo = ''
	for i in range(0, oligo_length):
		first_oligo += rand_nuc()
	oligos_list = []	
	oligos_list.append(first_oligo)
	sequence += first_oligo

	for i in range(0, oligos_number-1):
		without_first = oligos_list[-1][1:]
		new_oligo = without_first + rand_nuc()
		while any(new_oligo in oligo for oligo in oligos_list):
			new_oligo = without_first + rand_nuc()
		oligos_list.append(new_oligo)
		sequence += new_oligo[-1]

	# print oligos_list
	
	# removing from oligos_list 'negative' number of oligos
	for i in range(0, negatives):
		oligos_list.pop(random.randrange(len(oligos_list)))

	# print oligos_list

	for i in range(0, positives):
		new_oligo = ''
		for j in range(0, oligo_length):
			new_oligo += rand_nuc()
		while any(new_oligo in oligo for oligo in oligos_list):
			for j in range(0, oligo_length):
				new_oligo += rand_nuc()
		oligos_list.append(new_oligo)

	# print oligos_list
	f = open(instance_name, 'w')
	for oligo in oligos_list:
		f.write(oligo+'\n')
