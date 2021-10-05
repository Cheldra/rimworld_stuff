import curve

def heastroke_increase(degrees_above_comfortable):
    # based on Verse.HediffGiver_Heat.OnIntervalPassed
    difference = degrees_above_comfortable - 10
    if difference < 0:
        return 0
    modified_difference = curve.post_process_curve(difference,
                                                   x=[0, 25, 50, 100, 200, 400, 4000],
                                                   y=[0, 25, 40, 60, 70, 100, 1000])
    growth_per_60_ticks = modified_difference*0.0000645
    growth_per_60_ticks = max(growth_per_60_ticks, 0.000375)
    return growth_per_60_ticks


def heastroke_decrease_graph():
    severity = 1
    x = ['0']
    y = ['1']
    for tick_60 in range(1, 200):
        decrease = max(0.0015, min(0.015, 0.027*severity))
        severity -= decrease
        print(tick_60, round(decrease, 4), round(severity, 4))
        if severity <= 0:
            severity = 0
        x.append(str(round(tick_60*60/2500, 5)))
        y.append(str(round(severity, 5)))
        if severity == 0:
            break
    print('|x= ' + ', '.join(x))
    print('|y= ' + ', '.join(y))
            

def hypothermia_increase(degrees_below_comfortable):
    growth_per_60_ticks = max(0.00075, (degrees_below_comfortable - 10)*0.0000645)
    return growth_per_60_ticks
    


def increase_graph(increase_function = heastroke_increase):
    # graph
    x = []
    y = []
    for temp_difference in range(10, 101):
        if temp_difference % 2 != 0:
            continue
        ticks = 1/increase_function(temp_difference)*60
        result = round(ticks/2500, 1)
        print(temp_difference, result)
        x.append(str(temp_difference))
        y.append(str(result))

    print('|x = ' + ', '.join(x))
    print('|y = ' + ', '.join(y))

    # table
    for temp_difference in [10, 15, 20, 25, 50, 100, 300]:
        growth_per_60_ticks = increase_function(temp_difference)
        ticks = 1/growth_per_60_ticks*60
        secs = round(ticks/60, 1)
        in_game_hour = round(ticks/2500, 1)
        in_game_day = round(ticks/60000, 1)
        print('| ' + ' || '.join([str(i) for i in [temp_difference, round(growth_per_60_ticks, 6), round(ticks), in_game_hour, in_game_day]]))
        print('|-')

heastroke_decrease_graph()
increase_graph(hypothermia_increase)
