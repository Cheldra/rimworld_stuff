from collections import OrderedDict
import os
import infobox_checker_core as core
import xml.etree.ElementTree as ET

def define_rules(): 
    return {
        'name': (core.keep, ['label']),
        'image': (core.image_keep, ['label']),
        'imagesize': (core.keep, []),
        'description': (core.para, ['description']),
        'type': 'category',
        'type2': (categorise, ['designationCategory', 'label', 'building.isNaturalRock', 'building.isResourceRock', 'building.buildingTags.list']),
        'placeable': (placeable_default, ['designationCategory']),  # should maybe be hidden
        'path cost': 'pathCost',
        'passability': (core.breakup, ['passability']),  # new
        'blockswind': 'blockWind',  # new
        'cover': 'fillPercent',
        'minifiable': (minifiable_default, ['minifiedDef', 'designationCategory', 'stealable']),  # new        
        'size': (by_default, ['size']),
        'rotatable': (core.keep, []),
        'mass base':(core.depend, ['statBases.Mass', 'minifiedDef']),
        'flammability': (flammability_default, ['statBases.Flammability']),
        'hp': 'statBases.MaxHitPoints',
        'sell price multiplier': (core.depend, ['statBases.SellPriceFactor', 'minifiedDef']),
        'beauty': 'statBases.Beauty',
        'beauty outdoors': 'statBases.BeautyOutdoors',  # not actually present on any buildings currently
        'cleanliness': 'statBases.Cleanliness',
        'rest effectiveness': 'statBases.BedRestEffectiveness',
        'power': (power, ['comps.li-CompProperties_Power.basePowerConsumption']),
        'efficiency': (efficiency, ['statBases.ResearchSpeedFactor', 'statBases.WorkTableWorkSpeedFactor', 'comps.li-CompProperties_Battery.efficiency']),
        'immunity gain speed factor': 'statBases.ImmunityGainSpeedFactor',
        'medical qualty offset': 'statBases.MedicalTendQualityOffset',
        'surgery success chance factor': 'statBases.SurgerySuccessChanceFactor',
        'comfort': 'statBases.Comfort',
        'glowradius': 'comps.li-CompProperties_Glower.glowRadius',
        'glowcolor': (glowcol, ['comps.li-CompProperties_Glower.glowColor']),
        'heatpersecond': 'comps.li-CompProperties_HeatPusher.heatPerSecond',
        'maxheattemperature': 'comps.li-CompProperties_HeatPusher.heatPushMaxTemperature',
        'mincooltemperature': 'comps.li-CompProperties_HeatPusher.heatPushMinTemperature',
        'recreation power': 'statBases.JoyGainFactor',
        'recreation type': (joy_lookup, ['building.joyKind']),
        #'edifice': 'building.isEdifice',  # new
        'terrain affordance': (terrain_affordance, ['terrainAffordanceNeeded', 'useStuffTerrainAffordance', 'stuffCategories.list']),
        'facility': (facilities_thing, ['comps.li-CompProperties_AffectedByFacilities.linkableFacilities.list']),
        'research': (research_lookup, ['researchPrerequisites.list']),
        'style': 'dominantStyleCategory',  # new
        'styledominance': 'statBases.StyleDominance',  # new
        'tradeTags': (core.cat, ['tradeTag.list'], ['sort-reverse']),
        'tradeability': 'tradeability',  # new
        'thingCategories': (core.cat, ['thingCategories.list']),
        'skill 1': (construction_needed, ['constructionSkillPrerequisite']), 
        'skill 1 level': 'constructionSkillPrerequisite',
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
        'deconstructable': (deconstructable, ['building.deconstructible', 'stealable']),  # new
        'deconstruct yield': (deconstruct_yield_thing, ['designationCategory', 'building.deconstructible', 'resourcesFractionWhenDeconstructed', 'costStuffCount', 'costList.tuples']),
        #'deconstructyieldfraction': 'resourcesFractionWhenDeconstructed',  # new
        #'leavesresourceswhendestroyed': (kill_resource, ['leaveResourcesWhenKilled', 'costList.tuples']),  # new
        'destroyyield': (destroy_yield_thing, ['designationCategory', 'leaveResourcesWhenKilled', 'costStuffCount', 'costList.tuples', 'killedLeavings.tuples']),
        #'bonusdestroyleavings': (destroy_thing, ['killedLeavings.tuples']),  # new
        'mineyield': (mineyield_thing, ['building.mineableYield', 'building.mineableThing', 'building.mineableDropChance']),  # new
        'veinsize': (core.span, ['building.mineableScatterLumpSizeRange']),  # new
        'veincommanility': 'building.mineableScatterCommonality',  # new
        'damage': (turret_thing, ['building.turretGunDef'], [['verbs.1.defaultProjectile', 'projectile.damageAmountBase']]),
        'armorPenetration': (core.keep, []),
        'range': (turret_thing, ['building.turretGunDef'], [['verbs.1.range']]),
        'minrange': (turret_thing, ['building.turretGunDef'], [['verbs.1.minRange']]),
        'accuracyTouch': (turret_thing, ['building.turretGunDef'], [['statBases.AccuracyTouch']]),
        'accuracyShort': (turret_thing, ['building.turretGunDef'], [['statBases.AccuracyShort']]),
        'accuracyMedium': (turret_thing, ['building.turretGunDef'], [['statBases.AccuracyMedium']]),
        'accuracyLong': (turret_thing, ['building.turretGunDef'], [['statBases.AccuracyLong']]),
        'accuracyAvg': (core.keep, []),
        'mode': (core.keep, []),
        'burst': (turret_thing, ['building.turretGunDef'], [['verbs.1.burstShotCount']]),
        'burstTicks': (turret_thing, ['building.turretGunDef'], [['verbs.1.ticksBetweenBurstShots']]),
        'cooldown': (turret_thing, ['building.turretGunDef'], [['statBases.RangedWeapon_Cooldown']]),
        'warmup': (turret_thing, ['building.turretGunDef'], [['verbs.1.warmupTime']]),
        'velocity': (turret_thing, ['building.turretGunDef'], [['verbs.1.defaultProjectile', 'projectile.speed']]),
        'stoppingPower': (core.keep, []),
        'DPS': (core.keep, []),
        'info': (core.keep, []),
        'page verified for version': (core.keep, [])
        }

def categorise(designation, label, natural_rock, resource_rock, *building_tags):
    if designation != None:
        if designation == 'Joy':
            return 'Recreation'
        return designation.rstrip('s')
    if 'ancient' in label:
        return 'Ruin'
    if resource_rock != None:
        return 'Ore'
    if natural_rock != None:
        return 'Stone'
    if 'MechClusterMember' in building_tags:
        return 'Mechanoid cluster'

def placeable_default(designation):
    if designation != None:
        return 'true'
    return 'false'

def by_default(in_brackets):
    if in_brackets == None:
        return '1 ˣ 1'
    n_1 = in_brackets.split(',')[0].strip('(').strip()
    n_2 = in_brackets.split(',')[1].strip(')').strip()
    return f'{n_1} ˣ {n_2}'

def minifiable_default(minified_def, designation_category, stealable):
    if designation_category != None or (stealable != None and stealable.lower() == 'true'):
        if minified_def != None:
            return 'true'
        else:
            return 'false'

def terrain_affordance(actual, use_from_stuff, *stuff_tags):
    if use_from_stuff is None or use_from_stuff.lower() != 'true':
        return actual
    heavy_stuff = ['Metallic', 'Stony']
    light_stuff = ['Woody', 'Fabric', 'Leathery']
    heavy = False
    light = False
    for stuff in stuff_tags:
        if stuff in heavy_stuff:
            heavy = True
        elif stuff in light_stuff:
            light = True
    if light and heavy:
        return 'Light-Heavy'
    elif heavy:
        return 'Heavy'
    elif light:
        return 'Light'
    raise RuntimeError(f'bad stuff tags: {stuff_tags}')

def glowcol(cols):
    return ', '.join(c.strip() for c in cols.split(',')[:-1]) + ')'

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

def flammability_default(actual):
    if actual != None:
        return actual
    return '0'
    print(deconstruct_fraction)
    exit()
def joy_lookup(base_dir, joy_defname):
    root = ET.parse(base_dir + 'Core/Defs/Joy/JoyKinds.xml').getroot()
    for joy_def in root.findall('JoyKindDef'):
        if joy_def.find('defName').text == joy_defname:
            return joy_def.find('label').text
    raise RuntimeError(f'joy kind not found: \"{joy_defname}\"')

def facilities_thing(all_propagated_dicts, *facility_defnames):
    facility_labels = [core.label_thing(all_propagated_dicts, f) for f in facility_defnames]
    return core.cat(*facility_labels)

def efficiency(research_speed, worktable_speed, battery_eff):
    if research_speed != None:
        return research_speed
    if worktable_speed != None:
        return worktable_speed
    if battery_eff != None:
        return battery_eff

def deconstructable(deconst, stealable):
    if deconst != None and deconst.lower() == 'false':
        return 'false'

def deconstruct_yield_thing(all_propagated_dicts, designation_category, deconstructable, deconstruct_fraction, stuff_amount, *cost_tuples):
    if deconstructable is not None and deconstructable.lower() != 'true':
        return  # can't be deconstructed, which we pass to the wiki to deal with through another stat
    if (deconstruct_fraction is None or float(deconstruct_fraction) == 0.5) and designation_category is not None:
        return  # is a constructed thing that is deconstructed normally - leave it to the wiki
    if deconstruct_fraction is not None and float(deconstruct_fraction) == 0:
        return 'nothing'
    if deconstruct_fraction is None:
        deconstruct_fraction = 0.5
    else:
        deconstruct_fraction = float(deconstruct_fraction)
    resources_and_amounts = []
    if stuff_amount != None:
        resources_and_amounts.append(('Stuff', stuff_amount))
    for location_string, amount in cost_tuples:
            resources_and_amounts.append((core.label_thing(all_propagated_dicts, location_string.split('.')[-1]).capitalize(), core.tidy(str(float(amount)*deconstruct_fraction))))
    return ' + '.join(['{{' + f'Icon small|{res}' + '}}' + f' {amount}' for res, amount in resources_and_amounts]) 


def destroy_yield_thing(all_propagated_dicts, designation_category, leaves_resources, stuff_amount, *resource_and_leavings_tuples):
    resources_and_amounts = []
    leavings_and_amounts = []
    if stuff_amount != None:
        resources_and_amounts.append(('Stuff', stuff_amount))
    for location_string, amount in resource_and_leavings_tuples:
        if 'costList' in location_string:
            resources_and_amounts.append((core.label_thing(all_propagated_dicts, location_string.split('.')[-1]).capitalize(), core.tidy(str(float(amount)*0.25))))
        elif 'killedLeavings' in location_string:
            leavings_and_amounts.append((core.label_thing(all_propagated_dicts, location_string.split('.')[-1]).capitalize(), amount))
    if (leaves_resources is None or leaves_resources.lower() == 'true') and len(leavings_and_amounts) < 1:
        if designation_category is not None:
            return  # pure cost - leave it to the wiki
        return ' + '.join(['{{' + f'Icon small|{res}' + '}}' + f' {amount}' for res, amount in resources_and_amounts])  # pure cost, but can't be constructed to we list it out
    if leaves_resources.lower() == 'false' and len(resources_and_amounts) > 0 and len(leavings_and_amounts) < 1:
        return 'nothing'  # would normally leave resources, but doesn't so we need to override the wiki
    if leaves_resources.lower() == 'false':
        return ' + '.join(['{{' + f'Icon small|{res}' + '}}' + f' {amount}' for res, amount in leavings_and_amounts])  # pure leavings
    if len(resources_and_amounts) < 0:
        return
    return ' + '.join(['{{' + f'Icon small|{res}' + '}}' + f' {amount}' for res, amount in resources_and_amounts + leavings_and_amounts]) # cost and leavings


def destroy_thing(all_propagated_dicts, *kill_leavings):
    if len(kill_leavings) < 1:
        return
    strings = []
    for location_string, kill_leaving in kill_leavings:
        resource_defname = location_string.split('.')[-1]
        resource_label = core.label_thing(all_propagated_dicts, resource_defname).capitalize()
        strings.append('{{' + f'Icon small|{resource_label}' + '}}' + f' {kill_leaving}')
    return ' + '.join(strings)

def kill_resource(leavesresources, *cost_tuples):
    if len(cost_tuples) > 0:
        if leavesresources.lower() != 'true':
            return leavesresources.lower()

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
    return core.cat(*research_labels).lower()
        
def construction_needed(constructionSkillPrerequisite):
    return 'Construction'

def mineyield_thing(all_propagated_dicts, myield, mthing, mchance):
    if mchance is None:
        mchance = 1
    if myield is None:
        myield = 1
    mthing = core.label_thing(all_propagated_dicts, mthing).capitalize()
    myield = core.tidy(str(round(float(myield)*float(mchance), 2)))
    return '{{' + f'Icon small|{mthing}' + '}}' + f' {myield}'

    

def turret_thing(location_strings, all_propagated_dicts, turret_defname):
    turret = all_propagated_dicts[turret_defname]
    if location_strings[0] not in turret:
        return
    if len(location_strings) == 1:
        if 'accuracy' in location_strings[0].lower():
            return str(100*float(turret[location_strings[0]]))
        if 'cool' in location_strings[0].lower():
            return str(60*float(turret[location_strings[0]]))
        return turret[location_strings[0]]
    if location_strings[0] in turret.keys():
        bullet = all_propagated_dicts[turret[location_strings[0]]]
        return bullet[location_strings[1]]
