import curve

def on_interval_passed(ambient_temp, max_comfortable_temp=26):
    # based on Verse.HediffGiver_Heat.OnIntervalPassed
    difference = ambient_temp - (max_comfortable_temp + 10)
    modified_difference = curve.post_process_curve(difference,
                                                   x=[0, 25, 50, 100, 200, 400, 4000],
                                                   y=[0, 25, 40, 60, 70, 100, 1000])
    a = modified_difference*6.45e-5
    min_a = max(a, 0.000375)
    print(difference, modified_difference, round(a, 6), round(min_a, 6))
    return a


for temp in range(26, 46):
    on_interval_passed(temp)
