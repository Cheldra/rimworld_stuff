from math import e

adulthood_ticks = 10000
interval = 1
juv_age = 0.1
adult_age = 0.3333
juv_relative_age = juv_age/adult_age


growth = 0

for tick in range(adulthood_ticks):
    if tick % interval == 0:
        growth += interval/(adulthood_ticks - tick)
        print(tick, growth)
        if growth > juv_relative_age:
            break


progress_to_intended_adulthood = tick/adulthood_ticks


juv_eqn = 1-1/e**juv_relative_age
print(progress_to_intended_adulthood, juv_eqn, progress_to_intended_adulthood - juv_eqn)

adult_eqn = 1-1/e
print(adult_eqn)
print(f'prediction of actual juvenile age: {adult_age*progress_to_intended_adulthood}')

print(f'actual adult age: {adult_age*adult_eqn}')

ages = []
growth = 0
growths = []
ticks = 1000
steps = 50
for i in range(0, ticks):
    age = i/ticks
    growth += 1/(ticks-i)
    if growth > 1:
        growth = 1
    if i % (ticks/steps) == 0:
        print(age, round(growth, 5))
        ages.append(str(age))
        growths.append(str(round(growth, 5)))

print('ages:')
print(', '.join(ages))
print(('growths:'))
print(', '.join(growths))

print(1-1/e)
