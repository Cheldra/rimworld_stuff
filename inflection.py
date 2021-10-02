import curve

def eff(f, m, size, hunger, gestation, avg_offspring, juvenile_age, maturity_age):
    baby_hunger = hunger*0.4
    juvenile_hunger = hunger*0.75 
    baby_meat = round(curve.post_process_curve(140*size*0.2))
    baby_leather = round(curve.post_process_curve(40*size*0.2))
    adult_meat = round(curve.post_process_curve(140*size))
    adult_leather = round(curve.post_process_curve(40*size))
    
    offspring_per_day = f*avg_offspring/gestation

    baby_slaughter_meat_nutr_production = baby_meat*0.05*offspring_per_day
    baby_slaughter_leather_production = baby_leather*offspring_per_day
    
    adult_slaughter_meat_nutr_production = adult_meat*0.05*offspring_per_day
    adult_slaughter_leather_production = adult_leather*offspring_per_day
    
    adult_consumption = (f + m)*hunger
    baby_consumption = offspring_per_day*juvenile_age*baby_hunger
    juvenile_consumption = offspring_per_day*(maturity_age - juvenile_age)*juvenile_hunger
    
    baby_slaughter_nutr_eff = baby_slaughter_meat_nutr_production/adult_consumption
    baby_slaughter_leather_eff = baby_slaughter_leather_production/adult_consumption
    
    adult_slaughter_nutr_eff = adult_slaughter_meat_nutr_production/(adult_consumption + baby_consumption + juvenile_consumption)
    adult_slaughter_leather_eff = adult_slaughter_leather_production/(adult_consumption + baby_consumption + juvenile_consumption)
    
    return (baby_slaughter_nutr_eff, adult_slaughter_nutr_eff), (baby_slaughter_leather_eff, adult_slaughter_leather_eff)  
    

nutr_inflection_found = False
nutr_inflection = -1
leather_inflection_found = False
leather_inflection = -1
m = 100
for f in range(1, 250): # must increase
    meat_effs, leather_effs = eff(m=m, f=f, size=0.35, hunger=round(0.124*1.6, 10), gestation=5.66, avg_offspring=1.75, juvenile_age=0.1*60, maturity_age=0.2222*60)
    
    print(f'{f}:{m} {[round(meat_eff, 4) for meat_eff in meat_effs]}, {[round(leather_eff, 4) for leather_eff in leather_effs]}')
    if not nutr_inflection_found:
        if meat_effs[0] > meat_effs[1]:
            nutr_inflection_found = True
            nutr_inflection = f
    if not leather_inflection_found:
        if leather_effs[0] > leather_effs[1]:
            leather_inflection_found = True
            leather_inflection = f


print(f'nutr inflected at {nutr_inflection}')
print(f'leather inflected at {leather_inflection}')        
    
