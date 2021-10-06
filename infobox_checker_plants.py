from collections import OrderedDict
import infobox_checker_core as core

def define_rules():
    return {
        'page verified for version': (core.keep, []),
        'name': (core.keep, ['label']),
        'image': (core.keep, ['graphicData.texPath']),
        'description': 'description',
        'type': 'category',
        'type2': (plant_subtype, ['plant.treeCategory', 'plant.sowTags.1', 'plant.purpose']),
        'path cost': 'pathCost',
        'passability': (core.breakup, ['passability']),  # new
        'blockswind': 'blockWind',  # new
        'cover': 'fillPercent',
        'minifiable': (core.notnone, ['minifiedDef']),  # new
        'hp': 'statBases.MaxHitPoints',
        'flammability': 'statBases.Flammability',
        'mass base': 'statBases.Mass',
        'beauty': 'statBases.Beauty',
        'beautyoutdoors': 'statBases.BeautyOutdoors',
        'grow days': 'plant.growDays',
        'lifespanDaysPerGrowDays': 'plant.lifespanDaysPerGrowDays',
        'sow work': (core.depend, ['plant.sowWork', 'plant.sowTags.1']),
        'harvest work': (core.depend, ['plant.harvestWork', 'plant.harvestTag']),
        'product': (core.def_to_label, ['plant.harvestedThingDef']),
        'yield': 'plant.harvestYield',
        'min sowing skill': (core.depend, ['plant.sowMinSkill', 'plant.sowTags.1']),
        'min fertility': 'plant.fertilityMin',
        'fertility sensitivity': 'plant.fertilitySensitivity',
        'nutrition': (core.default_0, ['statBases.Nutrition']),
        'sowTags': (core.cat, ['plant.sowTags.list'])
        }


def plant_subtype(tree_category, sow_tag_1, purpose):
    if tree_category != None:
        return 'Tree'
    if sow_tag_1 != None:
        if purpose == 'Beauty':
            return 'Decorative'
        return 'Domesticated'
    return 'Wild'

rules = define_rules()
