import xml.etree.ElementTree as ET
import os

import infobox_checker_core as core
import curve
from pprint import pprint as pp


def define_rules():
    return {
        'page verified for version': (core.keep, []),
        'name': (core.keep, ['label']),
        'image': (core.keep, []),
        'description': (core.para, ['description']),
        'type': (animal_type, ['race.thinkTreeMain']),
        'type2': (animal_subtype, ['race.thinkTreeMain']),
        'movespeed': 'statBases.MoveSpeed',
        'basemeatamount': 'statBases.MeatAmount',
        'baseleatheramount': (leather_default, ['statBases.LeatherAmount', 'race.leatherDef']),
        'leathername': (core.label_thing, ['race.leatherDef']),
        'armorblunt': (percent, ['statBases.ArmorRating_Blunt']),
        'armorsharp': (percent, ['statBases.ArmorRating_Sharp']),
        'armorheat': (percent, ['statBases.ArmorRating_Heat']),
        'min comfortable temperature': (core.default, ['statBases.ComfyTemperatureMin'], ['0']),
        'max comfortable temperature': (core.default, ['statBases.ComfyTemperatureMax',], ['40']),
        'flammability': 'statBases.Flammability',
        'marketvalue': 'statBases.MarketValue',
        'filth rate': 'statBases.FilthRate',
        'ridingspeed': 'statBases.CaravanRidingSpeedFactor',
        'milkname': (core.lc, ['comps.li.milkDef']),
        'milktime': 'comps.li.milkIntervalDays',
        'milk': (core.label_thing, ['comps.li.milkAmount']), # looks up Items_Resource_Stuff -> label
        'woolname': (core.label_thing, ['comps.li.woolDef']),
        'sheartime': 'comps.li.shearIntervalDays',
        'wool': 'comps.li.woolAmount',
        'eggsmin': (eggs, ['comps.li-CompProperties_EggLayer.eggCountRange'], ['min']),
        'eggsmax': (eggs, ['comps.li-CompProperties_EggLayer.eggCountRange'], ['max']),
        'eggs_avg': (eggs, ['comps.li-CompProperties_EggLayer.eggCountRange'], ['avg']),
        'eggtime': 'comps.li-CompProperties_EggLayer.eggLayIntervalDays',
        'eggs_unfertilized': (core.notfalse, ['comps.li-CompProperties_EggLayer.eggUnfertilizedDef']),
        'predator': (core.notfalse, ['race.predator']),
        'herdanimal': (core.notfalse, ['race.herdAnimal']),
        'bodysize': 'race.baseBodySize',
        'healthscale': 'race.baseHealthScale',
        'hungerrate': 'race.baseHungerRate',
        'diet': (diet, ['race.foodType']),
        'wildness': 'race.wildness',
        'petness': 'race.petness',
        'tameable': 'race.playerCanChangeMaster',
        'manhunter': (manhunt, ['race.manhunterOnDamageChance', 'race.playerCanChangeMaster', 'race.thinkTreeMain'], ['harm']),
        'manhuntertame': (manhunt, ['race.manhunterOnTameFailChance', 'race.playerCanChangeMaster', 'race.thinkTreeMain'], ['tame']),
        'roamMtb': 'race.roamMtbDays',
        'trainable': (trainable, ['race.trainability', 'race.thinkTreeMain']), 
        'nuzzleMtb': 'race.nuzzleMtbHours',
        'packanimal': 'race.packAnimal',
        'meatname': (meat_thing, ['race.meatLabel', 'race.useMeatFrom']),
        'gestation': (gestation, ['race.gestationPeriodDays', 'comps.li-CompProperties_EggLayer.eggCountRange']),
        'offspring': (offspring_lookup, ['comps.li-CompProperties_EggLayer.eggCountRange', 'race.litterSizeCurve.points.list', 'race.lifeStageAges.tuples'], ['range']),
        'avg offspring': (offspring_lookup, ['comps.li-CompProperties_EggLayer.eggCountRange', 'race.litterSizeCurve.points.list', 'race.lifeStageAges.tuples'], ['avg']),
        'mateMtb': 'race.mateMtbHours',
        'babyscale': (babyscale_lookup, ['race.lifeStageAges.1.def']),
        'lifespan': 'race.lifeExpectancy',
        'juvenileage': 'race.lifeStageAges.2.minAge',
        'maturityage': 'race.lifeStageAges.3.minAge',
        'tradeTags': (core.cat, ['tradeTag.list'], ['sort-reverse']),
        'attack1dmg': (tool_verb_splitter, ['tools.tuples'], [1, 'dmg']),
        'attack1type': (tool_verb_splitter, ['tools.tuples'], [1, 'type']),
        'attack1cool':  (tool_verb_splitter, ['tools.tuples'], [1, 'cool']),
        'attack1part':  (tool_verb_splitter, ['tools.tuples'], [1, 'part']),
        'attack1chancefactor':  (tool_verb_splitter, ['tools.tuples'], [1, 'chance']),
        'attack1stun':  (tool_verb_splitter, ['tools.tuples'], [1, 'stun']),
        'attack1ap':  (tool_verb_splitter, ['tools.tuples'], [1, 'ap']),
        'attack2dmg': (tool_verb_splitter, ['tools.tuples'], [2, 'dmg']),
        'attack2type': (tool_verb_splitter, ['tools.tuples'], [2, 'type']),
        'attack2cool':  (tool_verb_splitter, ['tools.tuples'], [2, 'cool']),
        'attack2part':  (tool_verb_splitter, ['tools.tuples'], [2, 'part']),
        'attack2chancefactor':  (tool_verb_splitter, ['tools.tuples'], [2, 'chance']),
        'attack2stun':  (tool_verb_splitter, ['tools.tuples'], [2, 'stun']),
        'attack2ap':  (tool_verb_splitter, ['tools.tuples'], [2, 'ap']),
        'attack3dmg': (tool_verb_splitter, ['tools.tuples'], [3, 'dmg']),
        'attack3type': (tool_verb_splitter, ['tools.tuples'], [3, 'type']),
        'attack3cool':  (tool_verb_splitter, ['tools.tuples'], [3, 'cool']),
        'attack3part':  (tool_verb_splitter, ['tools.tuples'], [3, 'part']),
        'attack3chancefactor':  (tool_verb_splitter, ['tools.tuples'], [3, 'chance']),
        'attack3stun':  (tool_verb_splitter, ['tools.tuples'], [3, 'stun']),
        'attack3ap':  (tool_verb_splitter, ['tools.tuples'], [3, 'ap']),
        'attack4dmg': (tool_verb_splitter, ['tools.tuples'], [4, 'dmg']),
        'attack4type': (tool_verb_splitter, ['tools.tuples'], [4, 'type']),
        'attack4cool':  (tool_verb_splitter, ['tools.tuples'], [4, 'cool']),
        'attack4part':  (tool_verb_splitter, ['tools.tuples'], [4, 'part']),
        'attack4chancefactor':  (tool_verb_splitter, ['tools.tuples'], [4, 'chance']),
        'attack4stun':  (tool_verb_splitter, ['tools.tuples'], [4, 'stun']),
        'attack4ap':  (tool_verb_splitter, ['tools.tuples'], [4, 'ap']),
        'attack5dmg': (tool_verb_splitter, ['tools.tuples'], [5, 'dmg']),
        'attack5type': (tool_verb_splitter, ['tools.tuples'], [5, 'type']),
        'attack5cool':  (tool_verb_splitter, ['tools.tuples'], [5, 'cool']),
        'attack5part':  (tool_verb_splitter, ['tools.tuples'], [5, 'part']),
        'attack5chancefactor':  (tool_verb_splitter, ['tools.tuples'], [5, 'chance']),
        'attack5stun':  (tool_verb_splitter, ['tools.tuples'], [5, 'stun']),
        'attack5ap':  (tool_verb_splitter, ['tools.tuples'], [5, 'ap']),
        'attack6dmg': (tool_verb_splitter, ['tools.tuples'], [6, 'dmg']),
        'attack6type': (tool_verb_splitter, ['tools.tuples'], [6, 'type']),
        'attack6cool':  (tool_verb_splitter, ['tools.tuples'], [6, 'cool']),
        'attack6part':  (tool_verb_splitter, ['tools.tuples'], [6, 'part']),
        'attack6chancefactor':  (tool_verb_splitter, ['tools.tuples'], [6, 'chance']),
        'attack6stun':  (tool_verb_splitter, ['tools.tuples'], [6, 'stun']),
        'attack6ap':  (tool_verb_splitter, ['tools.tuples'], [6, 'ap']),
        'livesin_temperateforest': (biome_lookup, ['defName'], ['TemperateForest']),
        'livesin_temperateswamp': (biome_lookup, ['defName'], ['TemperateSwamp']),
        'livesin_borealforest': (biome_lookup, ['defName'], ['BorealForest']),
        'livesin_tundra': (biome_lookup, ['defName'], ['Tundra']),
        'livesin_coldbog': (biome_lookup, ['defName'], ['ColdBog']),
        'livesin_icesheet': (biome_lookup, ['defName'], ['IceSheet']),
        'livesin_seaice': (biome_lookup, ['defName'], ['SeaIce']),
        'livesin_aridshrubland': (biome_lookup, ['defName'], ['AridShrubland']), 
        'livesin_desert': (biome_lookup, ['defName'], ['Desert']),
        'livesin_extremedesert': (biome_lookup, ['defName'], ['ExtremeDesert']),
        'livesin_tropicalrainforest': (biome_lookup, ['defName'], ['TropicalRainforest']),
        'livesin_tropicalswamp': (biome_lookup, ['defName'], ['TropicalSwamp'])
        }


def animal_type(thinktree):
    if thinktree == 'Mechanoid':
        return 'Mechanoid'
    return 'Animal'

def animal_subtype(thinktree):
    if thinktree == 'Dryad':
        return 'Dryad'
    elif thinktree == 'Humanlike':
        return 'Human'

def leather_default(actual, leatherdefname):
    if actual != None and actual != '40':
        return actual
    if leatherdefname == None:
        return '0'

def percent(string_number):
    return(str(float(string_number)*100))

def eggs(minmaxavg, eggsrange):
    eggsmin = eggsrange.split('~')[0]
    if minmaxavg == 'min':
        return eggsmin
    eggsmax = eggsrange.split('~')[-1]
    if minmaxavg == 'max':
        return eggsmax
    eggsavg = str(round((float(eggsmin) + float(eggsmax)) / 2, 3))
    return eggsavg

def diet(foodtypes):
    diet_dict = {
        'OmnivoreHuman': 'omnivorous',
        'OmnivoreAnimal': 'omnivorous',
        'OmnivoreRoughAnimal': 'omnivorous grazer',
        'CarnivoreAnimal': 'carnivorous',
        'OvivoreAnimal': 'ovivorous',
        'AnimalProduct': 'animal products',
        'VegetarianRoughAnimal': 'herbivorous',
        'DendrovoreAnimal': 'dendrovorous',
        'CarnivoreAnimalStrict': 'raw meat and corpses',
        }
    diets = []
    for foodtype in foodtypes.split(','):
        if foodtype.strip() in diet_dict:
            diets.append(diet_dict[foodtype.strip()])
    if len(diets) > 0:
        return ' and '.join(diets)
    
def manhunt(tame_or_harm, actual, tameable, thinktree):
    if actual != None:
        return actual
    if thinktree in ['Mechanoid', 'Humanlike']:
        return
    if tame_or_harm == 'harm' or (tame_or_harm == 'tame' and (tameable == None or tameable.lower() != 'false')):
        return '0'

def trainable(trainability, thinktree):
    if trainability != None:
        return '!' + trainability.lower()
    if thinktree not in ['Mechanoid', 'Humanlike']:
        return 'none'
    
def meat_thing(all_propagated_dicts, meat_label, use_meat_from):
    if use_meat_from == None:
        return meat_label
    meat_source = all_propagated_dicts[use_meat_from]
    if 'race.meatLabel' in meat_source:
        return meat_source['race.meatLabel']
    source_label = meat_source['label']
    return f'{source_label} meat'

def gestation(gestation_period, egg_range):
    if egg_range == None:
        return gestation_period

def offspring_lookup(range_or_avg, base_dir, egg_range, *littersizepoints_and_lifestagetuples):
    if egg_range != None:
        return
    # check whether or not it is reproductive
    max_lifestage = -1
    for arg in littersizepoints_and_lifestagetuples:
        if type(arg) != tuple:
            continue
        lifestage = arg[0].split('.')[2]
        if int(lifestage) >= max_lifestage and arg[0][-4:] == '.def':
            final_lifestagedef = arg[1]
            max_lifestage = int(lifestage)
    root = ET.parse(base_dir + 'Core/Defs/Misc/LifeStageDefs/LifeStages.xml').getroot()
    for lifestagedef in root.findall('LifeStageDef'):
        if lifestagedef.find('defName') != None and lifestagedef.find('defName').text == final_lifestagedef:
            for tag in lifestagedef:
                if tag.tag == 'reproductive' and tag.text.lower() == 'true':
                    break
            else:
                return
    if max_lifestage == -1:
        return
    littersizepoints = [arg for arg in littersizepoints_and_lifestagetuples if type(arg) == str]
    x = [float(pair.strip().lstrip('(').rstrip(')').split(',')[0].strip()) for pair in littersizepoints]
    y = [float(pair.strip().lstrip('(').rstrip(')').split(',')[1].strip()) for pair in littersizepoints]
    if range_or_avg == 'range':
        if len(x) == 0:
            return '1'
        return f'{round(min(x)+0.001)}-{round(max(x)-0.001)}'
    if len(x) == 0:
        return
    return str(round(curve.expected_from_discrete_curve(x, y), 3))

def babyscale_lookup(base_dir, baby_defname):
    root = ET.parse(base_dir + 'Core/Defs/Misc/LifeStageDefs/LifeStages.xml').getroot()
    for lifestagedef in root.find('LifeStageDef'):
        if lifestagedef.find('defName') != baby_defname:
            continue
        babyscale = lifestagedef.find('bodySizeFactor').text
        if babyscale == '0.2':
            return
        return babyscale    

def tool_verb_splitter(attack_number, stat, *tooltuples):
    capacities_by_part = {i: 0 for i in range(1, 7)}
    for location_string, value in tooltuples:
        if 'capacities' not in location_string:
            continue
        part_number = int(location_string.split('.')[1])
        capacities_by_part[part_number] += 1
    tools_dict = {location_string: value for location_string, value in tooltuples}
    current_attack = 0
    for part_number in range(1, 7):
        part_number = int(part_number)
        for capacity_number in range(1, capacities_by_part[part_number] + 1):
            capacity_number = str(capacity_number)
            current_attack += 1
            if current_attack != attack_number:
                continue
            if stat == 'dmg':
                location_string = f'tools.{part_number}.power'
                if location_string in tools_dict:
                    return tools_dict[location_string]
                return
            if stat == 'type':
                location_string = f'tools.{part_number}.capacities.{capacity_number}'
                if location_string in tools_dict:
                    return tools_dict[location_string]
                return
            if stat == 'cool':
                location_string = f'tools.{part_number}.cooldownTime'
                if location_string in tools_dict:
                    return tools_dict[location_string]
                return
            if stat == 'part':
                location_string = f'tools.{part_number}.linkedBodyPartsGroup'
                if location_string in tools_dict:
                    body_part_dict = {'HeadAttackTool': 'head', 'HornAttackTool': 'horn'}
                    if tools_dict[location_string] in body_part_dict:
                        return body_part_dict[tools_dict[location_string]]
                    return core.breakup(tools_dict[location_string]).lower()
                return
            if stat == 'chance':
                location_string = f'tools.{part_number}.chanceFactor'
                if location_string in tools_dict:
                    return tools_dict[location_string]
                return
            if stat == 'stun':
                location_string = f'tools.{part_number}.surpriseAttack.extraMeleeDamages.1.amount'  # animals only ever have stun damage
                if location_string in tools_dict:
                    return tools_dict[location_string]
                return
            if stat == 'ap':
                location_string = f'tools.{part_number}.armorPenetration'
                if location_string in tools_dict:
                    return str(round(float(tools_dict[location_string])*100))
                return

def biome_lookup(biome_defname, base_dir, animal_defname):
    folder = 'Core/Defs/BiomeDefs/'
    for filename in os.listdir(base_dir + folder):
        root = ET.parse(base_dir + folder + filename).getroot()
        for biome_def in root.findall('BiomeDef'):
            if biome_def.find('defName').text != biome_defname:
                continue
            break
        else:
            continue
        break
    else:
        raise RuntimeError(f'biome not found: \"{biome_defname}\"')
    wild = biome_def.find('wildAnimals')
    if wild == None:
        return
    for tag in wild:
        if tag.tag == animal_defname:
                return tag.text            
    
