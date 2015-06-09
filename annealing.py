from solver import Solution
from math import exp
from copy import copy
from math import tanh
import os
import random

COOLING = 0
WARMING = 1
max_revert_attempts = 100
revert_attempts = 0

def simulated_annealing(instance):
    global revert_attempts, max_revert_attempts

    # print "press enter"
    # raw_input()
    random.seed()

    oligo_length = instance.oligo_length
    # print instance.solution



    def transform(solution):
        new_solution = Solution(solution)
        used_oligos = filter(lambda x: x.used, instance.oligos)
        unused_oligos = filter(lambda x: not x.used, instance.oligos)

        def choose_used():
            probability = 0.8 * ((float(len(used_oligos)) / len(used_oligos + unused_oligos)) ** 2)
            dice = random.random()
            return (dice < probability)

        if len(used_oligos) == 0: choose_from = unused_oligos
        elif len(unused_oligos) == 0: choose_from = used_oligos
        else: choose_from = used_oligos if choose_used() else unused_oligos
        chosen_oligo = random.choice(choose_from)

        new_oligo_pos = -1
        # print len(solution.overlaps)
        if len(solution.overlaps) > 0:
            tabu_filtered_overlaps = filter(lambda x: x not in tabu_overlaps, solution.overlaps)
            min_overlap = min(tabu_filtered_overlaps, key=lambda(o1,o2,len,pos): len)
            # Add overlap to tabu list if exceeded limit
            global revert_attempts, max_revert_attempts
            if revert_attempts >= max_revert_attempts:
                revert_attempts = 0
                tabu_overlaps.append(min_overlap)
            left_trailing = -1 * solution.overlaps[0][3]
            right_trailing = -1 * (len(instance.solution.sequence) - solution.overlaps[-1][3] - 2 * oligo_length + solution.overlaps[-1][2])
            o1, o2, overlap_len, o1_pos = min_overlap

            # print overlap_len, left_trailing, right_trailing

            while not (new_oligo_pos in range(0, len(solution.sequence) - oligo_length + 1)):
                if (overlap_len <= min(left_trailing, right_trailing)) or (left_trailing == 0 and right_trailing == 0):
                    # print "Inserting in the middle"
                    # calculate offset defined as distance from the overlap's beginning
                    offset = random.randint(0, oligo_length + o1.overlap(o2)) - oligo_length
                    new_oligo_pos = o1_pos + oligo_length - overlap_len + offset

                elif (overlap_len > left_trailing) and (overlap_len > right_trailing):
                    # print "Inserting in random trailing space"
                    # left_index = random.randint(0, -1 * left_trailing)
                    # right_index = random.randint(len(solution.sequence) - oligo_length - (-1 * right_trailing) + 1, len(solution.sequence) - oligo_length + 1)
                    left_index = 0
                    right_index = len(solution.sequence) - oligo_length
                    new_oligo_pos = random.choice([left_index, right_index])

                elif overlap_len > left_trailing:
                    # print "Inserting in left trailing space"
                    # new_oligo_pos = random.randint(0, -1 * left_trailing)
                    new_oligo_pos = 0

                elif overlap_len > right_trailing:
                    # print "Inserting in right trailing space"
                    # new_oligo_pos = random.randint(len(solution.sequence) - oligo_length - (-1 * right_trailing) + 1, len(solution.sequence) - oligo_length + 1)
                    new_oligo_pos = len(solution.sequence) - oligo_length

                else:
                    new_oligo_pos = random.randint(0, len(solution.sequence) - oligo_length)
        else:
            new_oligo_pos = random.randint(0, len(solution.sequence) - oligo_length)
        # print "Inserting %s at %d" % (chosen_oligo, new_oligo_pos)

        new_oligo_end = new_oligo_pos + (oligo_length - 1)

        # this is some info returned for reverting changes
        old_overlaps = copy(solution.overlaps)
        old_oligo_usage = { oligo: oligo.used_times for oligo in instance.oligos }

        # substitute the newly chosen oligo into the sequence
        new_solution.sequence = solution.sequence[:new_oligo_pos] + chosen_oligo.nuc + solution.sequence[new_oligo_end + 1:]
        # print new_solution.sequence

        # calculate new usage of oligos
        new_overlaps = []
        previous = None
        for oligo in instance.oligos: oligo.used_times = 0
        for i in range(len(new_solution.sequence) - oligo_length + 1):
            nuc = new_solution.sequence[i:i+oligo_length]
            if instance.oligos_dict.has_key(nuc):
                oligo = instance.oligos_dict[nuc]
                oligo.used_times += 1
                if previous == None: # next iteration if it's the first found oligo
                    previous = (oligo, i)
                    continue
                else:
                    prev_oligo, prev_pos = previous
                    overlap_len = oligo_length - i + prev_pos
                    new_overlaps.append((prev_oligo, oligo, overlap_len, prev_pos))
                    previous = (oligo, i)

        x = len(filter(lambda o: o.used, instance.oligos))
        # print x, "used out of", len(instance.oligos)
        if x > len(instance.oligos):
            raw_input()

        new_solution.overlaps = new_overlaps

        return new_solution, old_overlaps, old_oligo_usage

        pass

    mode = WARMING
    alpha_cooling = 0.99
    alpha_warming = 3
    cooling_age_length = 100
    initial_temp = 100.0
    max_moves_without_improvement = 5000
    modulation = 0.01
    warming_threshold = 0.98
    # revert_threshold = 0.97
    revert_threshold = tanh(pow(instance.result_length, 1.0/7)) ** 2

    def success():
        chance = random.random()
        # print new_quality, quality, temperature, modulation
        result = exp(-1*(float(quality) / float(new_quality))/(temperature * modulation))
        # print "chance=%f, result=%f" % (chance, result)
        return True if chance <= result else False

    phase = WARMING
    accepted_moves = 0
    accepted_moves_out_of_last_n = 0
    last_moves_size = 500
    last_moves = [False] * last_moves_size

    temperature = initial_temp
    max_temperature = 0
    time_exc = False
    moves_without_improvement = 0
    best_quality = 0

    def update_last_moves_acceptance(acc, prev):
        last_moves.append(acc)
        x = not acc
        last = last_moves.pop(0)
        if last == x:
            return prev + 1 if acc else prev - 1
        else:
            return prev

    best_quality = instance.solution.used_oligos_count
    best_usages = { oligo: oligo.used_times for oligo in instance.oligos }
    best_solution = instance.solution

    # Tabu oligo list
    tabu_overlaps = []

    # Main loop
    while (moves_without_improvement < max_moves_without_improvement) and (not time_exc) \
          and len(filter(lambda x: not x.used, instance.oligos)) > 0:
        # os.system('clear')
        # print ''
        # print len(filter(lambda x: not x.used, instance.oligos))
        quality = instance.solution.used_oligos_count
        attempts = 0
        transformed_solution, old_overlaps, old_oligo_usage = transform(instance.solution)
        new_quality = len(filter(lambda o: o.used, instance.oligos))# transformed_solution.used_oligos_count

        def revert_oligo_usage():
            for (oligo, old_usage) in old_oligo_usage.items():
                oligo.used_times = old_usage
            instance.solution.overlaps = old_overlaps

        if (new_quality > quality): # better
            # print "ACCEPTED BETTER"
            if mode == WARMING: accepted_moves_out_of_last_n = update_last_moves_acceptance(True, accepted_moves_out_of_last_n)
            accepted_moves += 1
            quality = new_quality
            if new_quality > best_quality:
                moves_without_improvement = 0
                best_quality = new_quality
                best_solution = transformed_solution
                best_usages = { oligo: oligo.used_times for oligo in instance.oligos }
                tabu_overlaps = []
                revert_attempts = 0
            instance.solution = transformed_solution
        else: # worse
            moves_without_improvement += 1
            succ = success()
            # print succ
            accepted_moves_out_of_last_n = update_last_moves_acceptance(succ, accepted_moves_out_of_last_n)
            if succ:
                # print "WORSE ACCEPTED"
                accepted_moves += 1
                quality = new_quality
                instance.solution = transformed_solution
            else:
                # print "WORSE REJECTED"
                revert_oligo_usage()
                if mode == WARMING and accepted_moves > cooling_age_length/10:
                    accepted_moves = 0
                    temperature += alpha_warming * initial_temp

        if mode == WARMING and float(accepted_moves_out_of_last_n) / last_moves_size >= warming_threshold:
            accepted_moves = 0
            mode = COOLING
            max_temperature = temperature
        elif mode == COOLING and accepted_moves >= cooling_age_length:
            temperature *= alpha_cooling
            accepted_moves = 0


        mode_str = "+" if mode == WARMING else "-"
        print "Mode:%s\tQual:%d\tBest:%d\tTemp:%d\tAccM:%d\tAccPerc:%f\tMw/oI:%d\tRev:%d\tTabu:%d" \
                % (mode_str, quality, best_quality, temperature, accepted_moves_out_of_last_n, \
                   float(accepted_moves_out_of_last_n) / last_moves_size, moves_without_improvement, revert_attempts, len(tabu_overlaps))

        def revert_to_best():
            global revert_attempts
            for (oligo, old_usage) in best_usages.items():
                oligo.used_times = old_usage
            instance.solution = best_solution
            revert_attempts += 1
            # print "Reverting to best"

        # Revert to best if quality drops below 0.9 * best
        # print "Threshold: ", revert_threshold * best_quality, ", quality: ", quality
        if quality <= revert_threshold * best_quality:
            revert_to_best()
        else:
            pass
            # print "Not reverting"

        # print 'Press enter...'
        # raw_input()


    revert_to_best()
    return best_solution
