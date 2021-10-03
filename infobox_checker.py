import os
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import OrderedDict
import copy
import curve


base_dir = str(Path.home()) + '/games/rimworld/RimWorld1-3-3117Linux/'
input_file = 'input.txt'
output_file = 'output.txt'

infobox_to_xml = OrderedDict([
    ('page verified for version', 'keep'),
    ('name', 'label'),
    ('image', 'keep'), # keep indicates to maintain whatever's in the input infobox
    ('description', 'description'),
    ('type', ''),  # set manually by the base thingDefs
    ('type2', 'tradeTags.list'), # requires processing - uses a manual dictionary type_dict
    ('type3', 'tradeTags.list'), # requires processing - uses a manual dictionary type_dict
    ('movespeed', 'statBases.MoveSpeed'),
    ('basemeatamount', 'statBases.MeatAmount'),
    ('baseleatheramount', 'statBases.LeatherAmount'),
    ('armorblunt', 'statBases.ArmorRating_Blunt'),
    ('armorsharp', 'statBases.ArmorRating_Sharp'),
    ('armorheat', 'statBases.ArmorRating_Heat'),
    ('min comfortable temperature', 'statBases.ComfyTemperatureMin'),
    ('max comfortable temperature', 'statBases.ComfyTemperatureMax'),
    ('marketvalue', 'statBases.MarketValue'),
    ('filth rate', 'statBases.FilthRate'),
    ('ridingspeed', 'statBases.CaravanRidingSpeedFactor'),
    ('milkname', 'comps.li.milkDef'),
    ('milktime', 'comps.li.milkIntervalDays'),
    ('milk', 'comps.li.milkAmount'), # looks up Items_Resource_Stuff -> label
    ('woolname', 'comps.li.woolDef'),
    ('sheartime', 'comps.li.shearIntervalDays'),
    ('wool', 'comps.li.woolAmount'),
    ('eggsmin', 'comps.li.eggCountRange'),
    ('eggsmax', 'comps.li.eggCountRange'),
    ('eggs_avg', 'comps.li.eggCountRange'),
    ('eggtime', 'comps.li.eggLayIntervalDays'),
    ('eggs_unfertilized', 'comps.li.eggUnfertilizedDef'),
    ('predator', 'race.predator'),
    ('bodysize', 'race.baseBodySize'),
    ('healthscale', 'race.baseHealthScale'),
    ('hungerrate', 'race.baseHungerRate'),
    ('diet', 'race.foodType'), # requires processing - uses a manual dictionary diet_dict
    ('leathername', 'race.leatherDef'), # requires processing - looks up Items_Resource_Stuff_Leather -> label
    ('wildness', 'race.wildness'),
    ('petness', 'race.petness'),
    ('tameable', 'race.playerCanChangeMaster'),
    ('manhuntertame', 'race.manhunterOnTameFailChance'),
    ('manhunter', 'race.manhunterOnDamageChance'),
    ('roamMtb', 'race.roamMtbDays'),
    ('trainable', 'race.trainability'), # fails on carrier dryad - should be "hauling only"
    ('nuzzleMtb', 'race.nuzzleMtbHours'),
    ('packanimal', 'race.packAnimal'),
    ('meatname', ('race.meatLabel', 'race.useMeatFrom')),  # if given as a tuple, all are examined
    ('gestation', 'race.gestationPeriodDays'),
    ('offspring', ('race.litterSizeCurve.points.list#1', 'race.lifeStageAges.3.def')),  # list indcates an <li> list to be further processed
    ('avg offspring', ('race.litterSizeCurve.points.list#2', 'race.lifeStageAges.3.def')), # #n is a tag to prevent merging
    ('babyscale', 'race.lifeStageAges.1.def'),
    ('lifespan', 'race.lifeExpectancy'),
    ('juvenileage', 'race.lifeStageAges.2.minAge'), # list: 1 indicates first of list
    ('maturityage', 'race.lifeStageAges.3.minAge'),
    ('attack1dmg', 'tool_verb_spliter?1?power'), # calls tool_verb_spliter(thing_def, 1, power)
    ('attack1type', 'tool_verb_spliter?1?type'), 
    ('attack1cool', 'tool_verb_spliter?1?cooldownTime'), 
    ('attack1part', 'tool_verb_spliter?1?label'),
    ('attack1chancefactor', 'tool_verb_spliter?1?chanceFactor'),
    ('attack1stun', 'tool_verb_splitter?1?surpriseAttack.extraMeleeDamages.li.amount'),
    ('attack1ap', 'tool_verb_splitter?1?armorPenetration'),
    ('attack2dmg', 'tool_verb_spliter?2?power'),
    ('attack2type', 'tool_verb_spliter?2?type'), 
    ('attack2cool', 'tool_verb_spliter?2?cooldownTime'), 
    ('attack2part', 'tool_verb_spliter?2?label'),
    ('attack2chancefactor', 'tool_verb_spliter?2?chanceFactor'),
    ('attack2stun', 'tool_verb_splitter?2?surpriseAttack.extraMeleeDamages.li.amount'),
    ('attack2ap', 'tool_verb_splitter?2?armorPenetration'),
    ('attack3dmg', 'tool_verb_spliter?3?power'),
    ('attack3type', 'tool_verb_spliter?3?type'), 
    ('attack3cool', 'tool_verb_spliter?3?cooldownTime'), 
    ('attack3part', 'tool_verb_spliter?3?label'),
    ('attack3chancefactor', 'tool_verb_spliter?3?chanceFactor'),
    ('attack3stun', 'tool_verb_splitter?3?surpriseAttack.extraMeleeDamages.li.amount'),
    ('attack3ap', 'tool_verb_splitter?3?armorPenetration'),
    ('attack4dmg', 'tool_verb_spliter?4?power'),
    ('attack4type', 'tool_verb_spliter?4?type'), 
    ('attack4cool', 'tool_verb_spliter?4?cooldownTime'), 
    ('attack4part', 'tool_verb_spliter?4?label'),
    ('attack4chancefactor', 'tool_verb_spliter?4?chanceFactor'),
    ('attack4stun', 'tool_verb_splitter?4?surpriseAttack.extraMeleeDamages.li.amount'),
    ('attack4ap', 'tool_verb_splitter?4?armorPenetration'),
    ('attack5dmg', 'tool_verb_spliter?5?power'),
    ('attack5type', 'tool_verb_spliter?5?type'), 
    ('attack5cool', 'tool_verb_spliter?5?cooldownTime'), 
    ('attack5part', 'tool_verb_spliter?5?label'),
    ('attack5chancefactor', 'tool_verb_spliter?5?chanceFactor'),
    ('attack5stun', 'tool_verb_splitter?5?surpriseAttack.extraMeleeDamages.li.amount'),
    ('attack5ap', 'tool_verb_splitter?5?armorPenetration'),
    ('attack6dmg', 'tool_verb_spliter?6?power'),
    ('attack6type', 'tool_verb_spliter?6?type'), 
    ('attack6cool', 'tool_verb_spliter?6?cooldownTime'), 
    ('attack6part', 'tool_verb_spliter?6?label'),
    ('attack6chancefactor', 'tool_verb_spliter?6?chanceFactor'),
    ('attack6stun', 'tool_verb_splitter?6?surpriseAttack.extraMeleeDamages.li.amount'),
    ('attack6ap', 'tool_verb_splitter?6?armorPenetration'),
    ('livesin_temperateforest', 'defName#1'), # looks up from BiomeDefs/
    ('livesin_temperateswamp', 'defName#2'),
    ('livesin_borealforest', 'defName#3'),
    ('livesin_tundra', 'defName#4'),
    ('livesin_coldbog', 'defName#5'),
    ('livesin_icesheet', 'defName#6'),
    ('livesin_seaice', 'defName#7'),
    ('livesin_aridshrubland', 'defName#8'), 
    ('livesin_desert', 'defName#9'),
    ('livesin_extremedesert', 'defName#10'),
    ('livesin_tropicalrainforest', 'defName#11'),
    ('livesin_tropicalswamp', 'defName#12')])
xml_to_infobox = OrderedDict([(v, k) for k, v in infobox_to_xml.items()])

diet_dict = {
    'OmnivoreRoughAnimal': 'omnivorous',
    'CarnivoreAnimal': 'carnivorous',
    'OvivoreAnimal': 'ovivorous',
    'VegetarianRoughAnimal': 'herbivorous',
    'OmnivoreAnimal': 'omnivorous',
    'AnimalProduct': 'animal products',
    'CarnivoreAnimalStrict': 'raw meat and corpses',
    'DendrovoreAnimal': 'dendrovorous',
    'None': 'none',
    'OmnivoreHuman': 'omnivorous'}

type_dict = OrderedDict({
    'AnimalDryad': 'Dryad',
    'AnimalInsect': 'Insect',
    'AnimalPet': 'Pet',
    'AnimalFarm': 'Farm',
    'AnimalExotic': 'Wild',
    'AnimalFighter': 'Wild',
    'AnimalUncommon': 'Wild',
    'AnimalCommon': 'Wild'})


def stat_finder(thing_def, location_string):
    stages = location_string.split('.')
    current_stage = thing_def
    for next_stage in location_string.split('.'):
        if next_stage.isdigit():
            try:
                current_stage = current_stage.findall('li')[int(next_stage) - 1]
            except IndexError:
                return '-'
        elif next_stage == 'cat':
            return '/'.join([list_member.text for list_member in current_stage.findall('li')])
        elif next_stage == 'list':
            return [list_member.text for list_member in current_stage.findall('li')]
        else:
            current_stage = current_stage.find(next_stage)
        if current_stage == None:
            return '-'
    return current_stage.text

def generate_leather_dict(base_dir):
    tree = ET.parse(base_dir + 'Data/Core/Defs/ThingDefs_Items/Items_Resource_Stuff_Leather.xml')
    leather_dict = {}
    for thing_def in tree.getroot().findall('ThingDef'):
        try:
            leather_dict[thing_def.find('defName').text] = thing_def.find('label').text
        except AttributeError:
            continue
    return leather_dict

def generate_wool_dict(base_dir):
    tree = ET.parse(base_dir + 'Data/Core/Defs/ThingDefs_Items/Items_Resource_Stuff.xml')
    wool_dict = {}
    for thing_def in tree.getroot().findall('ThingDef'):
        try:
            wool_dict[thing_def.find('defName').text] = thing_def.find('label').text
        except AttributeError:
            continue
    return wool_dict

def generate_lifestage_dict(base_dir):
    tree = ET.parse(base_dir + 'Data/Core/Defs/Misc/LifeStageDefs/LifeStages.xml')
    lifestage_dict = {}
    for lifestage_def in tree.getroot().findall('LifeStageDef'):
        lifestage_dict[lifestage_def.find('defName').text] = {}
        for stat in ['bodySizeFactor', 'reproductive']:
            try:
                lifestage_dict[lifestage_def.find('defName').text][stat] = lifestage_def.find(stat).text
            except AttributeError:
                continue
    return lifestage_dict


def generate_biome_dict(base_dir):
    biome_dict = {} # dict of form {animal_defName: {biome_lowercasedefname: weight}}
    for filename in os.listdir(base_dir + 'Data/Core/Defs/BiomeDefs/'):
        tree = ET.parse(base_dir + 'Data/Core/Defs/BiomeDefs/' + filename)
        for biome_def in tree.getroot().findall('BiomeDef'):
            biome_lowercasedefname = biome_def.find('defName').text.casefold()
            biome_dict[biome_lowercasedefname] = {}
            try:
                for animal in biome_def.find('wildAnimals'):
                    biome_dict[biome_lowercasedefname][animal.tag] = animal.text
            except TypeError:
                pass
    return biome_dict


def tool_verb_spliter(thing_def, attack, stat):
    attack = int(attack)
    if 'tools' not in [stat.tag for stat in thing_def]:
        return '-'
    separated_tool_verbs = []
    for tool in thing_def.find('tools').findall('li'):
        verbs = [verb.text for verb in tool.find('capacities').findall('li')]
        for verb in verbs:
            separated_tool_verbs.append((tool, verb))
    if attack <= len(separated_tool_verbs):
        if stat == 'type':
            return separated_tool_verbs[attack - 1][1]
        try:
            print(thing_def.find('defName').text, attack, stat, stat_finder(separated_tool_verbs[attack - 1][0], stat))
        except: pass
        print()
        value = stat_finder(separated_tool_verbs[attack - 1][0], stat)
        if value == '-' and stat == 'label':
            value = stat_finder(separated_tool_verbs[attack - 1][0], 'linkedBodyPartsGroup').casefold()
        return value
    else:
        return '-'

def add_to_infobox(parent_infobox, thing_def):
    new_infobox = {}
    for infobox_stat, xml_stat in infobox_to_xml.items():
        if type(xml_stat) is tuple:
            xml_value = [stat_finder(thing_def, single_xml_stat.split('#')[0]) for single_xml_stat in  xml_stat]
        elif xml_stat.split('?')[0] == 'tool_verb_spliter':
            xml_value = tool_verb_spliter(thing_def, attack=xml_stat.split('?')[1], stat=xml_stat.split('?')[2])
        else:  # for the ones given as tuples
            xml_value = stat_finder(thing_def, xml_stat.split('#')[0])
        new_infobox[infobox_stat] = xml_value
    new_infobox = post_process_infobox(new_infobox)
    combined_infobox = copy.deepcopy(parent_infobox)
    for infobox_stat, xml_value in new_infobox.items():
        combined_infobox[infobox_stat] = xml_value
    return combined_infobox


def post_process_infobox(infobox):
    cooked_infobox = copy.deepcopy(infobox)
    for infobox_stat, xml_value in infobox.items():
        #  exceptions
        #if infobox_stat == 'eggs_unfertilized':
        #    if 'eggsmin' in cooked_infobox.keys():
        #        xml_value = 'false'
        if xml_value == '-' or xml_value == None:
            del cooked_infobox[infobox_stat]
            continue
        elif infobox_stat == 'name':
            xml_value = xml_value.replace(' dryad', '').capitalize()
        elif infobox_stat[-4:] == 'part':
            if not type(xml_value) is str:  # if not already cooked
                label = xml_value[0]
                part = xml_value[1]
                if label != '-':
                    xml_value = label
                elif part != '-':
                    xml_value = part.casefold()
                else:
                    del cooked_infobox[infobox_stat]
                    continue
        elif infobox_stat == 'description':
            xml_value = xml_value.replace('\\n', '<br>').replace('<br><br>', '<br>')
        elif infobox_stat == 'diet':
            if sum([split_xml_value not in diet_dict.values() for split_xml_value in xml_value.split(' and ')]) and xml_value not in diet_dict.values():  # if it's not already been cooked
                diet_list = [diet_dict[raw_diet.strip()] for raw_diet in xml_value.split(',')]
                xml_value = ' and '.join([diet for diet in diet_list if diet != '-'])
                if xml_value == '':
                    del cooked_infobox[infobox_stat]
                    continue
        elif infobox_stat in ['type2', 'type3']:
            if xml_value not in type_dict.values():  # if it's not already been cooked
                type_rank = []
                for trade_tag in xml_value: # makes the more important type as type2
                    type_rank.append((type_dict[trade_tag], list(type_dict.keys()).index(trade_tag)))
                type_rank = sorted(type_rank, key=lambda row: row[1])
                if infobox_stat == 'type2':
                    xml_value = type_rank[0][0]
                elif infobox_stat == 'type3':
                    if len(type_rank) > 1:
                        xml_value = type_rank[1][0]
                    else:
                        del cooked_infobox[infobox_stat]
                        continue
        elif infobox_stat == 'leathername':
            if xml_value not in leather_dict.values():  # if it's not already been cooked
                xml_value = leather_dict[xml_value]
        elif infobox_stat == 'woolname':
            if xml_value not in wool_dict.values():  # if it's not already been cooked
                xml_value = wool_dict[xml_value]
        elif infobox_stat == 'gestation':
            if 'eggsmin' in cooked_infobox.keys():
                del cooked_infobox[infobox_stat]
                continue
        elif infobox_stat == 'meatname':
            if xml_value[1] != '-':  # useMeatFrom
                if xml_value[1] in known_infoboxes.keys():
                    if 'meatname' in known_infoboxes[xml_value[1]].keys():
                        xml_value = known_infoboxes[xml_value[1]]['meatname']
                    else:
                        del cooked_infobox[infobox_stat]
                        continue
                        
            elif xml_value[0] != '-':  # meatLabel
                xml_value = xml_value[0]
            else:
                del cooked_infobox[infobox_stat]
                continue
        elif infobox_stat == 'eggsmin':
            xml_value = xml_value.split('~')[0]
        elif infobox_stat == 'eggsmax':
            xml_value = xml_value.split('~')[-1]
        elif infobox_stat == 'eggs_avg':
            if '~' in xml_value:
                xml_value = str((int(xml_value.split('~')[0]) + int(xml_value.split('~')[-1]))/2)
        elif infobox_stat == 'eggs_unfertilized':
            if xml_value != 'false':
                xml_value = 'true'
        elif infobox_stat == 'trainable':
            xml_value = xml_value.casefold()
        elif infobox_stat == 'milkname':
            xml_value = xml_value.casefold()
            if xml_value == 'milk':
                del cooked_infobox[infobox_stat]
                continue
        elif infobox_stat in ['armorblunt', 'armorsharp', 'armorheat']:
            if float(xml_value) <= 2:
                xml_value = str(round(float(xml_value)*100))
        elif infobox_stat == 'babyscale':
            if '.' not in xml_value:
                if 'bodySizeFactor' in lifestage_dict[xml_value]:
                    xml_value = lifestage_dict[xml_value]['bodySizeFactor']
                    if xml_value == '0.2':
                        del cooked_infobox[infobox_stat]
                        continue
                else:
                    del cooked_infobox[infobox_stat]
                    continue
        elif infobox_stat == 'baseleatheramount':
            if xml_value == '40':
                del cooked_infobox[infobox_stat]
                continue
        elif infobox_stat == 'basemeatamount':
            if xml_value == '140':
                del cooked_infobox[infobox_stat]
                continue
        elif infobox_stat in ['offspring', 'avg offspring']:
            if 'eggsmin' in cooked_infobox.keys():
                del cooked_infobox[infobox_stat]
                continue
            if type(xml_value) is list: # if it's not already been cooked
                if xml_value[0] != '-':
                    x = [float(pair.lstrip('(').rstrip(')').split(',')[0]) for pair in xml_value[0]]
                    y = [float(pair.lstrip('(').rstrip(')').split(',')[1]) for pair in xml_value[0]]
                    if infobox_stat == 'offspring':
                        xml_value = f'{round(min(x)+0.001)}-{round(max(x)-0.001)}'
                    else:
                        xml_value = str(round(curve.expected_from_discrete_curve(x, y), 3))
                        if round(float(xml_value)) == float(xml_value):
                            xml_value = str(round(float(xml_value)))
                elif xml_value[1] != '-':
                    if 'reproductive' in lifestage_dict[xml_value[1]].keys():
                        if infobox_stat == 'offspring':
                            xml_value = '1'
                        else:
                            del cooked_infobox[infobox_stat]
                            continue
                else:
                    del cooked_infobox[infobox_stat]
                    continue

        elif infobox_stat[:7] == 'livesin':
            try:
                if not xml_value.replace('.', '').isdecimal():  # if not already cooked
                    xml_value = biome_dict[infobox_stat[8:]][xml_value]
            except KeyError:
                del cooked_infobox[infobox_stat]
                continue
        elif '.' in xml_value:
            try:
                if int(float(xml_value)) == float(xml_value):
                    xml_value = str(int(float(xml_value)))
                else:
                    xml_value = str(float(xml_value))  # removes trailing 0's
            except TypeError:
                pass
        cooked_infobox[infobox_stat] = xml_value
    return cooked_infobox


input_infobox = OrderedDict()
with open(input_file, 'r') as f:
    for line in f.readlines():
        if line.lstrip()[0] != '|':
            continue
        stat = line.split('=')[0].lstrip().lstrip('|').rstrip().lstrip()
        value = line.split('=')[1].strip()
        input_infobox[stat] = value

for stat in list(input_infobox.keys()):
    if stat not in infobox_to_xml.keys():
        print(f'\"{stat}\" unrecognised and removed')
        del input_infobox[stat]

leather_dict = generate_leather_dict(base_dir)
wool_dict = generate_wool_dict(base_dir)
biome_dict = generate_biome_dict(base_dir)
lifestage_dict = generate_lifestage_dict(base_dir)
print()
known_infoboxes = {}  # dictionary of form {defName: infobox} or {base_name: infobox} for parents


def look_at_xml(filename):
    tree = ET.parse(base_dir + filename)
    root = tree.getroot()
    for thing_def in root.findall('ThingDef'):
        if 'ParentName' in thing_def.attrib.keys():
            parent_name = thing_def.attrib['ParentName']
            working_infobox = known_infoboxes[thing_def.attrib['ParentName']]
        else:
            working_infobox = {}
        if 'Name' in thing_def.attrib.keys():
            base_name = thing_def.attrib['Name'] # this is a base thing that we should the base_name of
            if base_name == 'AnimalThingBase':
                working_infobox['min comfortable temperature'] = '0'
                working_infobox['max comfortable temperature'] = '40'
                working_infobox['manhuntertame'] = '0'
                working_infobox['manhunter'] = '0'
                working_infobox['type'] = 'Animal'
            elif base_name == 'BaseMechanoid':
                del working_infobox['filth']
                del working_infobox['manhuntertame'] 
                del working_infobox['manhunter']
                working_infobox['type'] = 'Mechanoid'
            elif base_name == 'DryadBase':
                del working_infobox['manhuntertame']
                working_infobox['meatname'] = 'immature dryad meat'
            elif 'filth' not in working_infobox.keys():
                working_infobox['filth'] = '1'
            known_infoboxes[base_name] = add_to_infobox(working_infobox, thing_def)
        else:
            known_infoboxes[stat_finder(thing_def, 'defName')] = add_to_infobox(working_infobox, thing_def)


def compare_infoboxes(infobox_1, infobox_2):
    for infobox_stat, xml_stat in infobox_to_xml.items():
        try:
            value_1 = infobox_1[infobox_stat]
        except KeyError:
            value_1 = '-'
        try:
            value_2 = infobox_2[infobox_stat]
        except KeyError:
            value_2 = '-'
        
        if xml_stat == 'keep':
            continue
        elif xml_stat == 'ver':
            with open(base_dir + 'Version.txt') as g:
                value_2 = g.readline().split()[0]
        
        if value_1 != value_2:
            print(f'{infobox_stat}: {value_1} -> {value_2};')


folders_to_look_at = ['Data/Core/Defs/ThingDefs_Races/', 'Data/Ideology/Defs/ThingDefs_Races/']

for folder in folders_to_look_at:
    for filename in sorted(list(os.listdir(base_dir + folder))):
        look_at_xml(folder + filename)


cooked_infoboxes = {}
for def_name, raw_infobox in known_infoboxes.items():
    cooked_infoboxes[def_name] = post_process_infobox(raw_infobox)

name = input_infobox['name']
for cooked_infobox in cooked_infoboxes.values():
    if 'name' in cooked_infobox.keys() and cooked_infobox['name'] == name:
        correct_infobox = cooked_infobox
        break
else:
    print(f'ThingDef with label \"{name.casefold()}\" not found in {folders_to_look_at}')
    exit(1)


compare_infoboxes(input_infobox, correct_infobox)
print()


def print_and_output(f, text):
    f.write(f'{text}\n')
    print(text)

with open(output_file, 'w') as f:
    print_and_output(f, '{{infobox main|animal|')
    for infobox_stat, xml_stat in infobox_to_xml.items():
        if xml_stat == 'keep':
            print_and_output(f, f'|{infobox_stat} = {input_infobox[infobox_stat]}')
        elif xml_stat == 'ver':
            with open(base_dir + 'Version.txt') as g:
                print_and_output(f, f'|{infobox_stat} = {g.readline().split()[0]}')
        elif infobox_stat == 'tameable':
            continue
        elif infobox_stat in correct_infobox.keys():
            print_and_output(f, f'|{infobox_stat} = {correct_infobox[infobox_stat]}')
    print_and_output(f, '}}')


