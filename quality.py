import random
import math


def gaussian_aymmetric(centerx=0, lower_width_factor=1, upper_width_factor=1):
    r_1 = random.random()
    r_2 = random.random()
    num = (-2*math.log(r_1))**0.5*math.sin(math.pi*2*r_2)
    if num <= 0:
        return num*lower_width_factor + centerx
    return num*upper_width_factor + centerx


def generate_quality(skill_level):
    # based on QualityCategory.GenerateQualityCreatedByPawn
    base_num_dict = {0: 0.7, 1: 1.1, 2: 1.5, 3: 1.8, 4: 2, 5: 2.2, 6: 2.4, 7: 2.6, 8: 2.8, 9: 2.95, 10: 3.1, 11: 3.25, 12: 3.4, 13: 3.5, 14: 3.6, 15: 3.7, 16: 3.8, 17: 3.9, 18: 4, 19: 4.1, 20: 4.2}
    base_num = base_num_dict[skill_level]
    
    value = math.floor(gaussian_aymmetric(base_num, 0.6, 0.8))
    value = max(min(value, 5), 0)
    if value == 5 and random.random() < 0.5:  # an additional chance to not get a masterwork
        value = math.floor(gaussian_aymmetric(base_num, 0.6, 0.95))
        value = max(min(value, 5), 0)
    return value


iterations = 10**5
for skill_level in range(21):
    outcomes = {o: 0 for o in range(6)}
    for iteration in range(iterations):
        outcomes[generate_quality(skill_level)] += 1
    chances = []
    for q in range(6):
        chances.append(round(outcomes[q]/iterations*100, 2))
        
    print(skill_level, chances)
    
