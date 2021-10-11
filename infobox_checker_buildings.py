from collections import OrderedDict
import os
import infobox_checker_core as core
import xml.etree.ElementTree as ET

def define_rules(): 
    return {
        'page verified for version': (core.keep, []),
        'name': (core.keep, ['label']),
        'image': (core.keep, ['graphicData.texPath']),
        'imagesize': (core.keep, []),
        'description': (core.para, ['description']),
        'type': 'category',
        'type2': (categorise, ['designationCategory', 'label', 'building.isNaturalRock', 'building.isResourceRock']),
        'placeable': (core.notnone, ['designationCategory']),  # should maybe be hidden
        'path cost': 'pathCost',
        'passability': (core.breakup, ['passability']),  # new
        'blockswind': 'blockWind',  # new
        'cover': 'fillPercent',
        'minifiable': (core.notnone, ['minifiedDef']),  # new        
        'size': (by, ['size']),
        'mass base': 'statBases.Mass',
        'flammability': 'statBases.Flammability',
        'hp': 'statBases.MaxHitPoints',
        'sell price multiplier': (core.depend, ['statBases.SellPriceFactor', 'minifiedDef']),
        'beauty': 'statBases.Beauty',
        'beauty outdoors': 'statBases.BeautyOutdoors',  # not actually present on any buildings currently
        'cleanliness': 'statBases.Cleanliness',
        'rest effectiveness': 'statBases.BedRestEffectiveness',
        'power': (power, ['comps.li-CompProperties_Power.basePowerConsumption']),
        'immunity gain speed factor': 'statBases.ImmunityGainSpeedFactor',
        'medical qualty offset': 'statBases.MedicalTendQualityOffset',
        'surgery success chance factor': 'statBases.SurgerySuccessChanceFactor',
        'comfort': 'statBases.Comfort',
        'recreation power': 'statBases.JoyGainFactor',
        'recreation type ': (joy_lookup, ['building.joyKind']),
        'terrain affordance': (core.lc, ['terrainAffordanceNeeded']),
        'facility': (facilities_thing, ['comps.li-CompProperties_AffectedByFacilities.linkableFacilities.list']),
        'research': (research_lookup, ['researchPrerequisites.list']),
        'tradeTags': (core.cat, ['tradeTag.list'], ['sort-reverse']),
        'tradeability': 'tradeability',  # new
        'skill 1': (construction_needed, ['constructionSkillPrerequisite']), 
        'skill 1 level': 'constructionSkillPrerequisite',
        'work to uninstall': 'building.uninstallWork',
        'work to make': (core.depend, ['statBases.WorkToBuild', 'designationCategory']),
        'stuff tags': (core.cat, ['stuffCategories.list']),  # need to make these only print if placeable
        'resource 1': (cost_thing, ['costStuffCount', 'costList.tuples', ], [1, 'resource']),
        'resource 1 amount': (cost_thing, ['costStuffCount', 'costList.tuples'], [1, 'amount']),
        'resource 2': (cost_thing, ['costStuffCount', 'costList.tuples'], [2, 'resource']),
        'resource 2 amount': (cost_thing, ['costStuffCount', 'costList.tuples'], [2, 'amount']),
        'resource 3': (cost_thing, ['costStuffCount', 'costList.tuples'], [3, 'resource']),
        'resource 3 amount': (cost_thing, ['costStuffCount', 'costList.tuples'], [3, 'amount']),
        'resource 4': (cost_thing, ['costStuffCount', 'costList.tuples'], [4, 'resource']),
        'resource 4 amount': (cost_thing, ['costStuffCount', 'costList.tuples'], [4, 'amount']),
        'deconstructible': (deconstructible, ['building.deconstructible', 'stealable']),  # new
        #'deconstruct yield': (core.keep, []),  # should be removed
        'deconstructyieldfraction': 'resourcesFractionWhenDeconstructed',  # new
        'leavesresourceswhendestroyed': (kill_resource, ['leaveResourcesWhenKilled', 'costList.tuples']),  # new
        'bonusdestroyleavings': (destroy_thing, ['killedLeavings.tuples']),  # new
        'mineyield': 'building.mineableYield',  # new
        'mineproduct': (core.label_thing, ['building.mineableThing']),  # new
        'veinsize': (core.span, ['building.mineableScatterLumpSizeRange']),  # new
        'veincommanility': 'building.mineableScatterCommonality',  # new
        'minedropchance': 'building.mineableDropChance'  # new
        }

def categorise(designation, label, natural_rock, resource_rock):
    if designation != None:
        return designation
    if 'ancient' in label:
        return 'Ruin'
    if resource_rock != None:
        return 'Ore'
    if natural_rock != None:
        return 'Stone'

def by(in_brackets):
    n_1 = in_brackets.split(',')[0].strip('(').strip()
    n_2 = in_brackets.split(',')[1].strip(')').strip()
    return f'{n_1} ˣ {n_2}'

def cost_thing(resource_index, resource_or_amount, all_propagated_dicts, stuff_amount, *resource_amounts):
    if resource_index == 1 and stuff_amount != None:
        if resource_or_amount == 'resource':
            return 'Stuff'
        return stuff_amount
    if stuff_amount != None:
        not_resources = 1
    else:
        not_resources = 0
    for i, resource_pair in enumerate(resource_amounts):
        if not resource_pair[1].isnumeric():
            not_resources += 1
            continue
        if resource_index == i + not_resources + 1:
            intrested_res = resource_pair
            break
    else:
        return
    if resource_or_amount == 'amount':
        return intrested_res[1]
    res_defname = intrested_res[0].split('.')[-1]
    return core.label_thing(all_propagated_dicts, res_defname).capitalize()


def joy_lookup(base_dir, joy_defname):
    root = ET.parse(base_dir + 'Core/Defs/Joy/JoyKinds.xml').getroot()
    for joy_def in root.findall('JoyKindDef'):
        if joy_def.find('defName').text == joy_defname:
            return joy_def.find('label').text
    raise RuntimeError(f'joy kind not found: \"{joy_defname}\"')

def facilities_thing(all_propagated_dicts, *facility_defnames):
    facility_labels = [core.label_thing(all_propagated_dicts, f) for f in facility_defnames]
    return core.cat(*facility_labels)

def deconstructible(deconst, stealable):
    if (deconst != None and deconst.lower() == 'false') or (stealable != None and stealable.lower() == 'false'):
        return 'false'


def destroy_thing(all_propagated_dicts, *kill_leavings):
    if len(kill_leavings) < 1:
        return
    strings = []
    for location_string, kill_leaving in kill_leavings:
        resource_defname = location_string.split('.')[-1]
        resource_label = core.label_thing(all_propagated_dicts, resource_defname).capitalize()
        strings.append(f'{kill_leaving} ' + '{{' + f'Icon small|{resource_label}' + '}}')
    return ' + '.join(strings)

def kill_resource(leavesresources, *cost_tuples):
    if len(cost_tuples) > 1:
        return leavesresources

def power(base_consumption):
    return str(int(base_consumption)*-1)  # doesn't work for solar generator

def research_lookup(base_dir, *research_defnames):
    folders = ['Core/Defs/ResearchProjectDefs/', 'Ideology/Defs/ResearchProjectDefs/', 'Royalty/Defs/ResearchProjectDefs/']
    research_labels = []
    for folder in folders:
        for filename in os.listdir(base_dir + folder):
            root = ET.parse(base_dir + folder + filename).getroot()
            for research_def in root.findall('ResearchProjectDef'):
                if research_def.find('defName') != None and research_def.find('defName').text in research_defnames:
                    research_labels.append(research_def.find('label').text)
    if len(research_labels) < len(research_defnames):
        raise RuntimeError(f'researches not found: \"{research_defnames}\"')
    return core.cat(*research_labels).capitalize()
        
def construction_needed(constructionSkillPrerequisite):
    return 'Construction'
