from random import random
def by_curve(x, y):
    sum_of_area = 0
    for i in range(len(x) - 1):
        sum_of_area += (x[i+1] - x[i])*(y[i] + y[i+1])
    #print(sum_of_area)
    random_number = random()*sum_of_area
    #print(random_number)
    for j in range(len(x) - 1):
        current_section_area = (x[j+1] - x[j])*(y[j] + y[j+1])
        if current_section_area < random_number:
            random_number -= current_section_area
            continue
        section_width = x[j+1] - x[j]
        num5 = random_number/(y[j] + y[j+1])
        
        #print(num5+x[j])
        if random()*(y[j] + y[j+1])/2 > y[j] + (y[j+1] - y[j])*min(1, max(0, num5/section_width)):
            num5 = section_width - num5
        return num5 + x[j]

class capybara:
    def __init__(self):
        self.x = [0.5, 1, 1.5, 2]
        self.y = [0, 1, 1, 0]

class squirrel:
    def __init__(self):
        self.x = [0.5, 1, 1.8, 2.4]
        self.y = [0, 1, 1, 0]

class rat:
    def __init__(self):
        self.x = [0.5, 1, 2.2, 2.8]
        self.y = [0, 1, 1, 0]


target = rat()
iterations = 10**6
sum = 0
rounded_sum = 0
for i in range(iterations):
    ran = by_curve(target.x, target.y)
    sum += ran
    rounded_sum += round(ran)
    print(i, i/iterations, round(ran), ran)
print(sum/iterations)
print(rounded_sum/iterations)
