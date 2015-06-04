from solver import Solution
from math import exp
from copy import copy
import random

COOLING = 0
WARMING = 1

def simulated_annealing(instance):
    print "press enter"
    raw_input()
    random.seed()

    oligo_length = instance.oligo_length
    print instance.solution

    def transform(solution):
        new_solution = Solution(solution)
        used_oligos = filter(lambda x: x.used, instance.oligos)
        unused_oligos = filter(lambda x: not x.used, instance.oligos)

        # print "Used:"
        # for o in used_oligos: print o, " %d" % o.used_times,
        # print "\nUnused:"
        # for o in unused_oligos: print o, " %d" % o.used_times,
        # print

        def choose_used():
            print "USED %d UNUSED %d" % (len(used_oligos), len(unused_oligos))
            probability = 0.8 * ((float(len(used_oligos)) / len(used_oligos + unused_oligos)) ** 2)
            dice = random.random()
            return (dice < probability)

        # find minimally overlapping pair of oligas
        # TODO: lookup all minimums, not just one
        print "%d overlaps" % len(solution.overlaps)
        min_overlap = min(solution.overlaps, key=lambda(o1,o2,len,pos): len)
        o1, o2, overlap_len, o1_pos = min_overlap

        # insert random oligo with random offset
        # print "used %d, unused %d" % (len(used_oligos), len(unused_oligos))
        choose_from = used_oligos if choose_used() else unused_oligos
        chosen_oligo = random.choice(choose_from)

        # offset is defined as distance from the beginning of the overlap
        # (oligo length 10, minimum offset -9, overlap len 3, max offset 3)
        offset = random.randint(0, oligo_length + o1.overlap(o2)) - (oligo_length - 1)

        new_oligo_pos = o1_pos + oligo_length - overlap_len + offset
        new_oligo_end = new_oligo_pos + (oligo_length - 1)
        # the area of new oligo's potential impact (inclusive)
        impact_left = new_oligo_pos - (oligo_length - 1)
        impact_right = new_oligo_pos + 2 * (oligo_length - 1)
        # the area to update overlaps (inclusive)
        update_left = impact_left - (oligo_length - 1)
        update_right = impact_right + (oligo_length - 1)

        # calculate the current number of used oligos in the area
        oligos_in_impact_area = [o1 for (o1, o2, l, p) in solution.overlaps if p in range(impact_left, new_oligo_end)]
        used_oligos_before_sub = len(oligos_in_impact_area)

        # decrement used_times for each oligo; we'll increment each one again later
        deleted_oligos = []
        for oligo in oligos_in_impact_area:
            oligo.used_times -= 1
            deleted_oligos.append(oligo)

        # insert the chosen_oligo in the chosen position
        new_solution.sequence = new_solution.sequence[:new_oligo_pos] + chosen_oligo.nuc + new_solution.sequence[new_oligo_end + 1:]

        # new solution's count of oligos used in sequence

        # update oligos in impact area
        added_oligos = []
        for i in range(impact_left, impact_right - oligo_length + 1):
            nuc = new_solution.sequence[i:i + oligo_length]
            if instance.oligos_dict.has_key(nuc):
                oligo = instance.oligos_dict[nuc]
                oligo.used_times += 1
                added_oligos.append(oligo)

        # update all the overlaps
        old_affected_overlaps = [o for o in solution.overlaps if o[3] in range(update_left, new_oligo_end + oligo_length)]
        new_overlaps = []
        previous = None
        for i in range(update_left, update_right - oligo_length + 1):
            nuc = new_solution.sequence[i:i + oligo_length]
            if instance.oligos_dict.has_key(nuc):
                oligo = instance.oligos_dict[nuc]
                if previous == None: continue
                prev_oligo, prev_pos = previous
                overlap_len = prev_oligo.overlap(oligo)
                new_overlaps.append((prev_oligo, oligo, overlap_len, prev_pos))
                previous = (oligo, i)

        old_overlaps_l = [o for o in solution.overlaps if o[3] < update_left]
        old_overlaps_r = [o for o in solution.overlaps if o[3] >= new_oligo_end + oligo_length]
        new_solution.overlaps = old_overlaps_l + new_overlaps + old_overlaps_r
        print "New: ", len(new_solution.overlaps)

        print new_solution.sequence
        # print 'Press enter...'
        # raw_input()
        return new_solution, added_oligos, deleted_oligos, copy(solution.overlaps)

    mode = WARMING
    alpha_cooling = 0.9
    alpha_warming = 1
    cooling_age_length = 300
    initial_temp = 100.0
    max_moves_without_improvement = 1000
    modulation = 0.1
    warming_threshold = 0.9

    def success():
        chance = random.random()
        # print new_quality, quality, temperature, modulation
        result = exp((new_quality - quality)/(temperature * modulation))
        print "chance=%f, result=%f" % (chance, result)
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

    # while (moves_without_improvement < max_moves_without_improvement) and (not time_exc) \
    #       and len(filter(lambda x: not x.used, instance.oligos)):
    while (moves_without_improvement < max_moves_without_improvement) and (not time_exc):
        print ''
        print len(filter(lambda x: not x.used, instance.oligos))
        quality = instance.solution.used_oligos_count
        attempts = 0
        transformed_solution, added_oligos, deleted_oligos, old_overlaps = transform(instance.solution)
        new_quality = transformed_solution.used_oligos_count

        def revert_oligo_usage():
            for oligo in added_oligos: oligo.used_times -= 1
            for oligo in deleted_oligos: oligo.used_times += 1
            # print "*** Reverting. Old overlaps count: %d, new: %d" % (len(old_overlaps), len(instance.solution.overlaps))
            # instance.solution.overlaps = old_overlaps

        if (new_quality > quality): # better
            print "NAJSYS"
            if mode == WARMING: accepted_moves_out_of_last_n = update_last_moves_acceptance(True, accepted_moves_out_of_last_n)
            accepted_moves += 1
            quality = new_quality
            if new_quality > best_quality:
                moves_without_improvement = 0
                best_quality = new_quality
                best_solution = transformed_solution
            instance.solution = transformed_solution
        elif new_quality == quality: # the same
            print "NIHIL NOVI"
            accepted_moves += 1
            moves_without_improvement += 1
            if mode == WARMING: accepted_moves_out_of_last_n = update_last_moves_acceptance(True, accepted_moves_out_of_last_n)
            instance.solution = transformed_solution
        else: # worse
            print "WORST"
            moves_without_improvement += 1
            succ = success()
            print succ
            accepted_moves_out_of_last_n = update_last_moves_acceptance(succ, accepted_moves_out_of_last_n)
            if succ:
                accepted_moves += 1
                quality = new_quality
                instance.solution = transformed_solution
            else:
                print "REJECTED"
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
        print "Mode:%s\tQual:%d\tBest:%d\tTemp:%d\tAccM:%d\tAccPerc:%f\tMw/oI:%d" \
                % (mode_str, quality, best_quality, temperature, accepted_moves_out_of_last_n, \
                   float(accepted_moves_out_of_last_n) / last_moves_size, moves_without_improvement)



    return instance.solution
