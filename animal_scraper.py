import os
from pathlib import Path
import xml.etree.ElementTree as ET
import copy
import curve


base_dir = str(Path.home()) + '/games/rimworld/RimWorld1-3-3117Linux/Data/Core/Defs/ThingDefs_Races/'

rows = []
for filename in os.listdir(base_dir):
    if filename in ['Races_Animal_Base.xml', 'Races_Humanlike.xml', 'Races_Mechanoid.xml', 'Races_Animal_Insect.xml']: 
        continue
    print(filename)
    tree = ET.parse(base_dir + filename)
    root = tree.getroot()
    known_bases = {}
    for thing_def in root.findall('ThingDef'):
        row = {'Source file': filename}
        if 'Name' in thing_def.attrib.keys():
            base_name = thing_def.attrib['Name']
        elif thing_def.attrib['ParentName'] in known_bases.keys():
            row = copy.deepcopy(known_bases[thing_def.attrib['ParentName']])
            base_name = None
        else:
            base_name = None
        try:
            row['Animal'] = thing_def.find('label').text.capitalize()
            print(thing_def.find('label').text.capitalize())
        except AttributeError:
            print(f'handling base {base_name}')
        race = thing_def.find('race')
        try:
            row['Base size'] = float(race.find('baseBodySize').text)
        except AttributeError:
            pass
        try:
            row['Base hunger'] = float(race.find('baseHungerRate').text)
        except AttributeError:
            pass
        try:
            row['Gestation period'] = float(race.find('gestationPeriodDays').text)
        except AttributeError:
            pass
        try:
            for life_stage in race.find('lifeStageAges').findall('li'):
                if life_stage.find('def').text == 'AnimalJuvenile':
                    row['Juvenile age'] = float(life_stage.find('minAge').text)
        except AttributeError:
            pass
        try:
            for life_stage in race.find('lifeStageAges').findall('li'):
                if life_stage.find('def').text == 'AnimalAdult':
                    row['Adult age'] = float(life_stage.find('minAge').text)
        except AttributeError:
            pass
        try:
            litter_x = []
            litter_y = []
            for point in race.find('litterSizeCurve').find('points').findall('li'):
                p = [float(n) for n in point.text.lstrip('(').rstrip(')').split(', ')]
                #print(p)
                litter_x.append(p[0])
                litter_y.append(p[1])
            row['Expected litter size'] = round(curve.expected_from_discrete_curve(litter_x, litter_y), 4)
            #print(row['Expected litter size'])
        except AttributeError:
            pass
        try:
            for comp in thing_def.find('comps').findall('li'):
                if comp.attrib['Class'] == 'CompProperties_EggLayer':
                    row['Egg interval'] = float(comp.find('eggLayIntervalDays').text)
        except AttributeError:
            pass
        try:
            for comp in thing_def.find('comps').findall('li'):
                if comp.attrib['Class'] == 'CompProperties_EggLayer':
                    egg_range = [int(i) for i in  comp.find('eggCountRange').text.split('~')]
                    if len(egg_range) == 1:
                        row['Expected clutch size'] = egg_range[0]
                    else:
                        row['Expected clutch size'] = (egg_range[0] + egg_range[1])/2
        except AttributeError:
            pass
        try:
            for comp in thing_def.find('comps').findall('li'):
                if comp.attrib['Class'] == 'CompProperties_Milkable':
                    row['Milk interval'] = float(comp.find('milkIntervalDays').text)
        except AttributeError:
            pass
        try:
            for comp in thing_def.find('comps').findall('li'):
                if comp.attrib['Class'] == 'CompProperties_Milkable':
                    row['Milk amount'] = float(comp.find('milkAmount').text)
        except AttributeError:
            pass
        try:
            row['Tame manhunter chance'] = race.find('manhunterOnTameFailChance').text
        except AttributeError:
            pass
        try:
            row['Hunt manhunter chance'] = race.find('manhunterOnDamageChance').text
        except AttributeError:
            pass
        try:
            row['Wildness'] = race.find('wildness').text
        except AttributeError:
            pass
        try:
            row['Filth rate'] = thing_def.find('statBases').find('FilthRate').text
        except AttributeError:
            pass
        try:
            row['Nuzzle interval'] = race.find('nuzzleMtbHours').text
        except AttributeError:
            pass
        try:
            row['Roam mtb'] = race.find('roamMtbDays').text
        except AttributeError:
            pass
        try:
            row['Mate mtb'] = race.find('mateMtbHours').text
        except AttributeError:
            pass

        try:
            row['Riding speed'] = thing_def.find('statBases').find('CaravanRidingSpeedFactor').text
        except AttributeError:
            pass


        
        if base_name:
            known_bases[base_name] = row
        else:
            if 'Expected litter size' not in row.keys() and 'Egg interval' not in row.keys():
                row['Expected litter size'] = 1
            if 'Egg interval' in row.keys() and 'Gestation period' in row.keys():
                del row['Gestation period']
            rows.append(row)
        print(row)
    print()

for row in rows:
    if row['Animal'] not in ['Chicken', 'Duck', 'Megascarab', 'Spelopede', 'Megaspider', 'Goose']:
        row['A. Leather amount'] = round(curve.post_process_curve(40*row['Base size']))
        row['Base leather'] = 40
    elif row['Animal'] == 'Goose':
        row['A. Leather amount'] =         round(curve.post_process_curve(36*row['Base size']))
        row['Base leather'] = 36
    else:
        row['Base leather'] = 0
    row['A. hunger'] = round(row['Base hunger']*1.6, 2)
    row['J. hunger'] = round(row['A. hunger']*0.75, 2)
    row['B. hunger'] = round(row['A. hunger']*0.4, 2)
    row['J. size'] = round(row['Base size']*0.5, 2)
    row['B. size'] = (round(row['Base size']*0.2, 2) if row['Source file'] not in ['Races_Animal_BigBirds.xml', 'Races_Animal_ChickenGroup.xml'] else round(row['Base size']*0.1, 2))
    row['A. meat'] = round(curve.post_process_curve(140*row['Base size']))
    row['J. meat'] = round(curve.post_process_curve(140*row['J. size']))
    row['B. meat'] = round(curve.post_process_curve(140*row['B. size']))
    row['A. leather'] = round(curve.post_process_curve(row['Base leather']*row['Base size']))
    row['J. leather'] = round(curve.post_process_curve(row['Base leather']*row['J. size']))
    row['B. leather'] = round(curve.post_process_curve(row['Base leather']*row['B. size']))
    if 'Gestation period' in row.keys():
        row['Idealised offspring rate per female'] = row['Expected litter size']/row['Gestation period']
    elif 'Egg interval' in row.keys():
        row['Idealised offspring rate per female'] = row['Expected clutch size']/row['Egg interval']
    else:
        row['Idealised offspring rate per female'] = 0
    if 'Milk interval' in row.keys():
        row['Milk per day'] = round(row['Milk amount']/row['Milk interval'], 2)
    row['9F1MASl tot. cons.'] = round(10*row['A. hunger'] + 9*row['B. hunger']*row['Idealised offspring rate per female']*row['Juvenile age']*60 + 9*row['J. hunger']*row['Idealised offspring rate per female']*(row['Adult age'] - row['Juvenile age'])*60, 2)
    row['9F milk prod.'] = (9*row['Milk per day'] if 'Milk per day' in row.keys() else 0)
    row['9F1MASl tot. prod.'] = round(9*row['Idealised offspring rate per female']*row['A. meat']*0.05 + row['9F milk prod.']*0.05, 2)
    row['9F1MASl eff.'] = round(row['9F1MASl tot. prod.']/row['9F1MASl tot. cons.'], 2)
    
    
    row['9F1MBSl tot. cons.'] = round(10*row['A. hunger'], 2)
    row['9F1MBSl tot. prod.'] = round(9*row['Idealised offspring rate per female']*row['B. meat']*0.05 + row['9F milk prod.']*0.05, 2)
    row['9F1MBSl eff.'] = round(row['9F1MBSl tot. prod.']/row['9F1MBSl tot. cons.'], 2)


    
    print(row['Animal'], row['9F1MASl tot. cons.'], row['9F1MASl tot. prod.'], row['9F1MASl eff.'])
    print(row['Animal'], row['9F1MBSl tot. cons.'], row['9F1MBSl tot. prod.'], row['9F1MBSl eff.'])

    print(row['9F milk prod.']*0.05)


    

#headers = ['Animal', 'Base size', 'Base hunger', 'Juvenile age', 'Adult age', 'Gestation period', 'Expected litter size', 'Egg interval', 'Expected clutch size', 'Milk interval', 'Milk amount', 'Tame manhunter chance', 'Hunt manhunter chance', 'Roam mtb', 'Riding speed', 'Wildness', 'Filth rate', 'Nuzzle interval', 'A. hunger', 'J. hunger', 'B. hunger', 'J. size', 'B. size', 'A. meat', 'J. meat', 'B. meat', 'A. leather', 'J. leather', 'B. leather', '9F1MASl tot. cons.', '9F1MASl tot. prod.', '9F1MASl eff.', '9F1MBSl tot. cons.', '9F1MBSl tot. prod.', '9F1MBSl eff.', '9F milk prod.']
headers = ['Animal', 'Base size', 'Base hunger', 'Juvenile age', 'Adult age', 'Gestation period', 'Expected litter size', 'Egg interval', 'Expected clutch size', 'Mate mtb',  'Milk interval', 'Milk amount', 'Tame manhunter chance', 'Hunt manhunter chance', 'Roam mtb', 'Riding speed', 'Wildness', 'Filth rate', 'Nuzzle interval', 'A. hunger', 'J. hunger', 'B. hunger', 'J. size', 'B. size', 'A. meat', 'J. meat', 'B. meat', 'A. leather', 'J. leather', 'B. leather']
with open('animal_productivity.csv', 'w') as f:
    f.write(','.join(headers) + '\n')
    for row in rows:
        f.write(','.join([str(row[header]) if header in row.keys() else '' for header in headers]) + '\n')
    
    
