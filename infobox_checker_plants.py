from collections import OrderedDict
import os
import infobox_checker_core as core
import xml.etree.ElementTree as ET

def define_rules():
    return {
        'page verified for version': (core.keep, []),
        'name': (core.keep, ['label']),
        'image': (core.keep, ['graphicData.texPath']),
        'description': (core.para, ['description']),
        'type': 'category',
        'type2': (plant_subtype, ['plant.treeCategory', 'plant.sowTags.1', 'plant.purpose', 'category']),
        'path cost': 'pathCost',
        'passability': (core.breakup, ['passability']),  # new
        'blockswind': 'blockWind',  # new
        'cover': 'fillPercent',
        'minifiable': (core.notnone, ['minifiedDef']),  # new
        'hp': 'statBases.MaxHitPoints',
        'flammability': 'statBases.Flammability',
        'mass base': (core.depend, ['statBases.Mass', 'minifiable']),
        'beauty': 'statBases.Beauty',
        'beauty outdoors': 'statBases.BeautyOutdoors',
        'grow days': 'plant.growDays',
        'lifespanDaysPerGrowDays': 'plant.lifespanDaysPerGrowDays',
        'sow work': (core.depend, ['plant.sowWork', 'plant.sowTags.1']),
        'harvest work': 'plant.harvestWork',
        'product': (core.def_to_label, ['plant.harvestedThingDef']),
        'yield': 'plant.harvestYield',
        'min sowing skill': (core.depend, ['plant.sowMinSkill', 'plant.sowTags.1']),
        'min fertility': 'plant.fertilityMin',
        'fertility sensitivity': 'plant.fertilitySensitivity',
        'nutrition': 'statBases.Nutrition',
        'sowTags': (core.cat, ['plant.sowTags.list']),
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


def plant_subtype(tree_category, sow_tag_1, purpose, *args):
    if tree_category != None:
        return 'Tree'
    if sow_tag_1 != None:
        if purpose == 'Beauty':
            return 'Decorative'
        return 'Domesticated'
    return 'Wild'

def biome_lookup(biome_defname, base_dir, plant_defname):
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
    wild = biome_def.find('wildPlants')
    if wild == None:
        return
    for tag in wild:
        if tag.tag == plant_defname:
                return tag.text           

rules = define_rules()
