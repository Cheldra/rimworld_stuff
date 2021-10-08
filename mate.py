import random
import math

def simulate_gestational(males=1, females=20, gestation=6.66*24, mate_mtb=12, rest_effectiveness=0.8, simulation_time=10**5, warmup_time=10**3, v=False):
    if rest_effectiveness != None:
        time_to_exhaustion = 18.189
        time_to_full_rest = 10.5*0.72/rest_effectiveness
        full_cycle = time_to_exhaustion + time_to_full_rest
    pregnant_list = [None for i in range(females)]
    time_between_pregnancy_tracker = [None for i in range(females)]
    inter_pregnancy_interval_list = []
    total_pregnant_time = 0
    for hour in range(simulation_time):  # each hour
        if rest_effectiveness == None or hour % full_cycle > time_to_full_rest:  # if awake
            for m in range(males):  # each male
                if random.random() < 1/mate_mtb:  # might mate
                    for f, pregnancy in enumerate(pregnant_list):  # he looks for a female
                        if pregnancy == None:  # that isn't pregnant
                            if random.random() < 0.5:  # if the impregnation is sucessful
                                pregnant_list[f] = 0  # she becomes pregnant
                                if time_between_pregnancy_tracker[f] != None:
                                    inter_pregnancy_interval_list.append(time_between_pregnancy_tracker[f])
                                time_between_pregnancy_tracker[f] = 0
                            break  # he stops looking to mate
        for f, pregnancy in enumerate(pregnant_list): # each female
            if pregnancy != None:  # if pregnant
                pregnant_list[f] +=  1 # her pregnancy progresses
                if hour > warmup_time:
                    total_pregnant_time += 1
                if pregnant_list[f] > gestation: # if her pregnancy is complete
                    pregnant_list[f] = None  # she becomes not pregnant
            else:
                if time_between_pregnancy_tracker[f] != None:
                    time_between_pregnancy_tracker[f] += 1        
        if v:
            print(hour, pregnant_list)
    ret = round(100*(total_pregnant_time/females/(simulation_time - warmup_time)), 4)
    if v:
        print(gestation)
        print(warmup_time)
        average_time_between_pregnancies = round(sum(inter_pregnancy_interval_list)/len(inter_pregnancy_interval_list), 5)
        print(f'average time between {len(inter_pregnancy_interval_list)} pregnancies: {average_time_between_pregnancies}h')
        if None in time_between_pregnancy_tracker:
            print(f'{time_between_pregnancy_tracker.count(None)} females were never pregnant')
        print(f'total of {total_pregnant_time}h of pregnancy, or {total_pregnant_time/females}h per female, or {ret}% of female-time was spent pregnant')
    return ret


def simulate_egglaying(males=1, females=20, egg_interval=24, mate_mtb=12, rest_effectiveness=0.8, simulation_time=10**5, warmup_time=10**3, v=False):
    if rest_effectiveness != None:
        time_to_exhaustion = 18.189
        time_to_full_rest = 10.5*0.72/rest_effectiveness
        full_cycle = time_to_exhaustion + time_to_full_rest
    egg_list = [0 for i in range(females)]
    fert_list = [False for i in range(females)]
    total_wasted_time = 0
    for hour in range(simulation_time):  # each hour
        if rest_effectiveness == None or hour % full_cycle > time_to_full_rest:  # if awake
            for m in range(males):  # each male
                if random.random() < 1/mate_mtb:  # might mate
                    for f, fert in enumerate(fert_list):  # he looks for a female
                        if fert == False:  # that isn't fertilised
                            fert_list[f] = True  # she becomes fertilised
                            break  # he stops looking to mate
        for f in range(females): # each female
            if egg_list[f] < 0.5*egg_interval:  # if her egg is less than 50%
                egg_list[f] += 1  # her egg progresses
            elif fert_list[f]:  # or if she's fertilised
                egg_list[f] += 1  # her egg progresses
            elif hour > warmup_time:
                total_wasted_time += 1
            if egg_list[f] >= egg_interval:  # if her egg is ready to be layed
                egg_list[f] = 0  # she beings forming a new egg
                fert_list[f] = False  # and her fertilisation resets
        if v:
            print(hour, egg_list)
    if v:
        print(total_wasted_time)
    ret = 100 - 100*(total_wasted_time/females/(simulation_time - warmup_time))
    return ret


def females_and_males_from_ratio(target_pop, female_ratio):
    min_males = max(math.floor(1/female_ratio), 1)
    min_females = female_ratio*min_males
    pop_scale = max(round(target_pop/(min_males+min_females)), 1)
    females = round(min_females*pop_scale)
    males = min_males*pop_scale
    return females, males


gestation_and_matemtbs = [(5.661, 8),  (6.66, 8),  (5.61, 12), (5.661, 12), (6, 12), (6.66, 12), (8.5, 12), (10, 12), (12, 12), (13.32, 12), (20, 12)]
egginterval_and_matemtbs = [(1, 8), (2, 8), (1.333, 12), (3.333, 12), (5.661, 12), (6.66, 12), (10, 12)]

def main_table():
    target_pop=20
    flattened_rows = []
    for rest_effectiveness in [None, 0.8, 1]:
        for female_ratio in  [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]:
            females, males = females_and_males_from_ratio(target_pop, female_ratio)
            gestation_and_matemtbs = sorted(gestation_and_matemtbs, key=lambda g_and_m: g_and_m[0]/g_and_m[1])
            egginterval_and_matemtbs = sorted(egginterval_and_matemtbs, key=lambda e_and_m: e_and_m[0]/e_and_m[1])
            for gestation, mate_mtb in gestation_and_matemtbs:
                pregnant_proportion = simulate_gestational(males=males, females=females, gestation=gestation*24, mate_mtb=mate_mtb, rest_effectiveness=rest_effectiveness)
                time_between_pregnancies = gestation/(0.01*pregnant_proportion) - gestation
                row = [round(pregnant_proportion, 4), round(time_between_pregnancies, 4), females, males, gestation, None, mate_mtb, rest_effectiveness]
                print(row)
                flattened_rows.append(row)
            for egg_interval, mate_mtb in egginterval_and_matemtbs:
                egg_growing_proportion = simulate_egglaying(males=males, females=females, egg_interval=egg_interval*24, mate_mtb=mate_mtb, rest_effectiveness=rest_effectiveness)
                egg_wasted_time = egg_interval/(0.01*egg_growing_proportion) - egg_interval
                row = [round(egg_growing_proportion, 4), round(egg_wasted_time, 4), females, males, None, egg_interval, mate_mtb, rest_effectiveness]
                print(row)
                flattened_rows.append(row)
            print()


    for rest_effectiveness in [1.25, 1.6]:
        females = 20
        males = 1
        mate_mtb = 12
        gestation = 6.66
        pregnant_proportion = simulate_gestational(males=males, females=females, gestation=gestation*24, mate_mtb=mate_mtb, rest_effectiveness=rest_effectiveness)
        time_between_pregnancies = gestation/(0.01*pregnant_proportion) - gestation
        row = [round(pregnant_proportion, 4), round(time_between_pregnancies, 4), females, males, gestation, None, mate_mtb, rest_effectiveness]
        print(row)
        flattened_rows.append(row)
        
        females = 15
        males = 3
        mate_mtb = 8
        egg_interval = 1
        egg_growing_proportion = simulate_egglaying(males=males, females=females, egg_interval=egg_interval*24, mate_mtb=mate_mtb, rest_effectiveness=rest_effectiveness)
        egg_wasted_time = egg_interval/(0.01*egg_growing_proportion) - egg_interval
        row = [round(egg_growing_proportion, 4), round(egg_wasted_time, 4), females, males, None, egg_interval, mate_mtb, rest_effectiveness]
        print(row)
        flattened_rows.append(row)
        

    flattened_rows = sorted(flattened_rows, key=lambda row: (row[4] is None, row[4], row[4] is None, row[5] is None, row[5], row[6] is None, row[6], row[7] is None, row[7], row[2] is None, row[2]))
    with open('output.csv', 'w') as f:
        f.write('productive female-time (%), wasted female-time per offspring (days), females,males,gestation (days),egg interval (days),mate mtb (h),rest effectiveness (none = never sleeps)\n')
        for row in flattened_rows:
            f.write(','.join(str(c) for c in row) + '\n')
            

def best_ratio_experiment():
    rows = []
    
    for rest_effectiveness in [None, 0.8, 1, 1.25, 1.6]:
        if rest_effectiveness != None:
            time_to_exhaustion = 18.189
            time_to_full_rest = 10.5*0.72/rest_effectiveness
            proportion_awake = time_to_exhaustion/(time_to_full_rest + time_to_exhaustion)
        else:
            proportion_awake = 1
        
        for gestation, mate_mtb in gestation_and_matemtbs:
            theoretical_ideal_ratio = 0.5*gestation*24/mate_mtb*proportion_awake
            females_upper, males = females_and_males_from_ratio(20, theoretical_ideal_ratio)
            for females in [females_upper - 2 , females_upper - 1, females_upper, females_upper + 1]:
                pregnant_proportion = simulate_gestational(females=females, males=males, gestation=gestation*24, mate_mtb=mate_mtb, rest_effectiveness=rest_effectiveness)
                time_between_pregnancies = gestation/(0.01*pregnant_proportion) - gestation
                row = [round(pregnant_proportion, 4), round(time_between_pregnancies, 4), females, males, gestation, None, mate_mtb, rest_effectiveness, round(theoretical_ideal_ratio, 4), round(females/males, 4)]
                print(row)
                rows.append(row)
            print()
        print()

    rows = sorted(rows, key=lambda row: (row[4] is None, row[4], row[4] is None, row[5] is None, row[5], row[6] is None, row[6], row[7] is None, row[7], row[2] is None, row[2]))
    with open('best_ratio_experiment.csv', 'w') as f:
        f.write('productive female-time (%), wasted female-time per offspring (days), females,males,gestation (days),egg interval (days),mate mtb (h),rest effectiveness (none = never sleeps), theoretical best ratio, this ratio\n')
        for row in rows:
            f.write(','.join(str(c) for c in row) + '\n')
            
        
best_ratio_experiment()
#main_table()

