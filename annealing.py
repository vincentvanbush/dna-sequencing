from solver import Solution
from math import exp
import random

COOLING = 0
WARMING = 1

def simulated_annealing(instance):
    random.seed()

    oligo_length = instance.oligo_length
    print instance.solution
    used_oligos = filter(lambda x: x.used, instance.oligos)
    unused_oligos = filter(lambda x: not x.used, instance.oligos)

    def transform(solution):
        new_solution = Solution(solution)

        def choose_used():
            probability = 0.8 * ((float(len(used_oligos)) / len(used_oligos + unused_oligos)) ** 2)
            dice = random.random()
            return (dice < probability)

        # find minimally overlapping pair of oligas
        # TODO: lookup all minimums, not just one
        min_overlap = min(solution.overlaps, key=lambda(o1,o2,len,pos): len)
        o1, o2, overlap_len, o1_pos = min_overlap

        # insert random oligo with random offset
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


        # insert the chosen_oligo in the chosen position
        new_solution.sequence = new_solution.sequence[:new_oligo_pos] + chosen_oligo.nuc + new_solution.sequence[new_oligo_end + 1:]

        # new solution's count of oligos used in sequence

        print new_solution.sequence
        print 'Press enter...'
        raw_input()
        return new_solution

    mode = WARMING
    alpha_cooling = 0.9
    alpha_warming = 1
    cooling_age_length = 300
    initial_temp = 100.0
    max_moves_without_improvement = 1000
    modulation = 3.0
    warming_threshold = 0.9

    def success():
        chance = random.random()
        print new_quality, quality, temperature, modulation
        result = exp((new_quality - quality)/(temperature * modulation))
        return True if chance <= result else False

    phase = WARMING
    accepted_moves = 0
    accepted_moves_out_of_last_n = 0
    last_moves = [False] * 500
    temperature = initial_temp
    max_temperature = 0
    time_exc = False
    moves_without_improvement = 0
    best_quality = 0

    def update_last_moves_acceptance(acc, previous):
        last_moves.append(acc)
        x = not acc
        if last_moves[0] == x:
            return previous + 1 if acc else previous - 1
        last_moves.popleft()

    while moves_without_improvement < max_moves_without_improvement and not time_exc:
        quality = instance.solution.used_oligos_count
        attempts = 0
        transformed_solution = transform(instance.solution)
        new_quality = transformed_solution.used_oligos_count

        if (new_quality > quality): # better
            if mode == WARMING: accepted_moves_out_of_last_n = update_last_moves_acceptance(True, accepted_moves_out_of_last_n)
            accepted_moves += 1
            quality = new_quality
            if new_quality > best_quality:
                moves_without_improvement = 0
                best_quality = new_quality
                best_solution = transformed_solution
            instance.solution = transformed_solution
        elif new_quality == quality: # the same
            accepted_moves += 1
            moves_without_improvement += 1
            if mode == WARMING: accepted_moves_out_of_last_n = update_last_moves_acceptance(True, accepted_moves_out_of_last_n)
            instance.solution = transformed_solution
        else: # worse
            moves_without_improvement += 1
            succ = success()
            accepted_moves_out_of_last_n = update_last_moves_acceptance(succ, accepted_moves_out_of_last_n)
            if succ:
                accepted_moves += 1
                quality = new_quality
            else:
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



    return instance.solution
