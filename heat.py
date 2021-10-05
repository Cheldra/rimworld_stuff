import curve

def on_interval_passed(degrees_above_comfortable):
    # based on Verse.HediffGiver_Heat.OnIntervalPassed
    difference = degrees_above_comfortable - 10
    if difference < 0:
        return 0
    modified_difference = curve.post_process_curve(difference,
                                                   x=[0, 25, 50, 100, 200, 400, 4000],
                                                   y=[0, 25, 40, 60, 70, 100, 1000])
    growth_per_60_ticks = modified_difference*6.45e-5
    growth_per_60_ticks = max(growth_per_60_ticks, 0.000375)
    return growth_per_60_ticks

x = []
y = []
for temp_difference in range(10, 101):
    if temp_difference % 2 != 0:
        continue
    ticks = 1/on_interval_passed(temp_difference)*60
    result = round(ticks/2500, 1)
    print(temp_difference, result)
    x.append(str(temp_difference))
    y.append(str(result))

print(', '.join(x))
print(', '.join(y))

for temp_difference in [10, 15, 20, 25, 100, 300, 4000]:
    growth_per_60_ticks = on_interval_passed(temp_difference)
    ticks = 1/growth_per_60_ticks*60
    secs = round(ticks/60, 1)
    in_game_hour = round(ticks/2500, 1)
    in_game_day = round(ticks/60000, 1)
    print(temp_difference, round(growth_per_60_ticks, 6), round(ticks, 1), secs, in_game_hour, in_game_day)
