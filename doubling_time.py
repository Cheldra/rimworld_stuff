def pop_simulator(maturity_age=12, starting_females=1, final_day=60):
    young_females_by_age = [0 for i in range(maturity_age)]
    mature_females = starting_females
    for day in range(final_day):
        mature_females += young_females_by_age.pop(-1)
        young_females_by_age = [mature_females*0.5] + young_females_by_age
        print(f'{day}: {mature_females}', young_females_by_age, sum(young_females_by_age))
        
pop_simulator()
        
    
