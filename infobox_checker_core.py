import os
from pathlib import Path
import xml.etree.ElementTree as ET
from pprint import pprint as pp
import argparse

import infobox_checker_plants
import infobox_checker_buildings
import infobox_checker_pawns


base_dir = str(Path.home()) + '/games/rimworld/RimWorld1-3-3117Linux/Data/'
input_file = 'input.txt'


def list_xmls(base_dir):
    for path, subdirs, files in os.walk(base_dir):
        if 'Defs' not in path:
            continue
        for filename in files:
            if filename[-4:] != '.xml':
                continue
            yield path[len(base_dir):] + '/' + filename


def parse_xml(base_dir, xml_file):
    new_thing_defs = {}
    root = ET.parse(base_dir + xml_file).getroot()
    for thing_def in root.findall('ThingDef'):
        if 'Name' in thing_def.attrib.keys():
            thing_name = thing_def.attrib['Name']
        else:
            thing_name = thing_def.find('defName').text
        new_thing_defs[thing_name] = thing_def
    return new_thing_defs


def list_location_strings_and_values(current_tag, current_location = '', li_num=0):
    joiner = '.'
    #print(current_tag, current_location)
    if 'Class' in current_tag.attrib.keys():
        current_location += 'li-' + current_tag.attrib['Class']
    elif 'Inherit' in current_tag.attrib.keys() and current_tag.attrib['Inherit'] == 'False':
        current_location += current_tag.tag + '!'
    elif li_num != 0:
        current_location += str(li_num)
    elif current_tag.tag != 'ThingDef':
        current_location += current_tag.tag
    else:
        joiner = ''
    any_sub_tags = False
    l = 0
    for sub_tag in current_tag:
        any_sub_tags = True
        if sub_tag.tag == 'li' and 'Class' not in sub_tag.attrib.keys():
            l += 1
        yield from list_location_strings_and_values(sub_tag, current_location + joiner, l)
    if not any_sub_tags:
        yield current_location, current_tag.text


def dictify_thing(thing_def):
    return {location_string: value for location_string, value in list_location_strings_and_values(thing_def)}


def propagate_parents(thing_dict, parent_name, all_thing_defs_dict):
    parent_def = all_thing_defs_dict[parent_name]
    parent_dict = dictify_thing(parent_def)
    parent_dict.update(thing_dict)
    if 'ParentName' in parent_def.attrib.keys():
        grandparent_name = parent_def.attrib['ParentName']
        return propagate_parents(parent_dict, grandparent_name, all_thing_defs_dict)
    return parent_dict


def cleanse_uninherited(thing_dict):
    removed_dict = thing_dict.copy()
    for key in thing_dict.keys():
        if '!' in key:
            uninherit = key.split('!')[0]
            for key2 in thing_dict.keys():
                if '!' not in key2 and key2 in removed_dict and key2[:len(uninherit)] == uninherit:
                    del removed_dict[key2]
    replaced_dict = {}
    for key, val in removed_dict.items():
        replaced_dict[key.replace('!', '')] = val 
    return replaced_dict


def get_all_propagated_dicts(base_dir):
    all_thing_defs_dict = {}  # dictionary of form base_name or thing_def.defName: thing_def
    for xml_filename in list_xmls(base_dir):
        all_thing_defs_dict.update(parse_xml(base_dir, xml_filename))
    all_things_propagated_dict = {}
    for name, thing_def in all_thing_defs_dict.items():
        if 'Abstract' not in thing_def.attrib.keys() or thing_def.attrib['Abstract'] == 'False':
            if 'ParentName' not in thing_def.attrib.keys():
                all_things_propagated_dict[name] = dictify_thing(thing_def)  # for the few things that have no parent
                continue
            all_things_propagated_dict[name] = cleanse_uninherited(propagate_parents(dictify_thing(thing_def),
                                                                 thing_def.attrib['ParentName'],
                                                                 all_thing_defs_dict))
    return all_things_propagated_dict        

def filter_dicts(all_propagated_dicts, filters):
    any_found = False
    for propagated_dict in all_propagated_dicts.values():
        for filter_key, filter_value in filters.items():
            if filter_key not in propagated_dict.keys() or lc(propagated_dict[filter_key]) != lc(filter_value):
                break
        else:
            any_found = True
            yield propagated_dict
    if not any_found:
        raise RuntimeError(f'could not find thing_def that has {filters}')


def analyse_key(all_propagated_dicts, filters, key):
    value_label_dict = {}
    for propagated_dict in all_propagated_dicts.values():
        for filter_key, filter_value in filters.items():
            if filter_key not in propagated_dict.keys() or propagated_dict[filter_key] != filter_value:
                break
        else:
            if key in propagated_dict.keys():
                value = propagated_dict[key]
                if value not in value_label_dict.keys():
                    value_label_dict[value] = []
                if 'label' in propagated_dict.keys():
                    value_label_dict[value].append(propagated_dict['label'])
                else:
                    value_label_dict[value].append(propagated_dict['defName'])
    for k, v in value_label_dict.copy().items():
        value_label_dict[k] = sorted(v)
    counts = [{k: len(v) for k, v in value_label_dict.items()}]
    return value_label_dict, counts, sum([len(v) for v in value_label_dict.values()])

def tidy(string):
    if string == None or string.lower() == 'none' or len(string) == 0:
        return
    if string[0] == '!':
        return string[1:]
    if len(string.split('.')) > 2:
        return string
    if '.' in string and string.replace('.', '').isnumeric() and float(string) == round(float(string)):
        string = str(round(float(string)))
    elif '.' in string and string.replace('.', '').isnumeric():
        string = string.rstrip('0')
    return string

def keep(infobox_stat, input_dict, *args):
    if input_dict == None:
        if len(args) == 0: # no default given
            return
        else:
            return args[0].capitalize()
    if infobox_stat in input_dict:
        return input_dict[infobox_stat]

def default(d, actual):
    if actual != None:
        return actual
    return d

def para(string):
    return string.replace('\\n', '<br>').replace('<br><br>', '<br>')

def lc(string):
    if string == None:
        string = 'None'
    return string.lower()

def cat(*args):
    if args[0] == 'sort':
        args = sorted(args[1:])
    elif args[0] == 'sort-reverse':
        args = sorted(args[1:], reverse=True)
    ret = ', '.join([a for a in args if a != None])
    if ret != '':
        return ret

def depend(actual, *dependancies):
    if len(dependancies) == 0:
        return
    for dependancy in dependancies:
        if dependancy == None or dependancy.lower() == 'none':
            return
    return actual

def notnone(*args):
    for arg in args:
        if arg == None or arg.lower() == 'none':
            return 'false'
    return 'true'

def notfalse(*args):
    for arg in args:
        if arg != None and arg.lower() != 'false':
            return 'true'

def breakup(string):
    output_string = ''
    j = 0
    for i, char in enumerate(string):
        if char.isupper():
            output_string += string[j:i] + ' ' 
            j = i
    output_string += string[j:]
    return output_string.strip().lower()

def label_thing(all_propagated_dicts, *def_names):
    labels = []
    for def_name in def_names:
        try:
            labels.append(all_propagated_dicts[def_name]['label'])
        except KeyError:
            print(f'WARNING: could not find label of defname \"{def_name}\", using as-is')
            labels.append(def_name)
    return cat(*labels)

def span(string):
    return string.split('~')[0] + '-' + string.split('~')[1]

def remove_default(default, string):
    if string != default:
        return string

def apply_rule(xml_dict, input_dict, all_propagated_dicts, infobox_stat, rule):
    if type(rule) == str:
        if rule in xml_dict:
            return tidy(xml_dict[rule])
        return
    if type(rule) != tuple:
        print(f'warning: rule {rule} not given as string or tuple, skipping')
        return
    function = rule[0]
    location_strings = rule[1]
    args = []
    if len(rule) > 2:
        args = rule[2]  # hard arguments
    any_found = False
    if function.__name__ == 'keep':
        args += [infobox_stat, input_dict]
        any_found = True
    elif '_thing' in function.__name__:
        args += [all_propagated_dicts]
    elif 'lookup' in function.__name__:
        args += [base_dir]
    elif 'default' in function.__name__:
        any_found = True
    for location_string in location_strings:
        if location_string[-5:] == '.list': # gives [list of values]
            for present_location_string in xml_dict.keys():
                if location_string[:-5] == present_location_string[:len(location_string) - 5] and xml_dict[present_location_string] != None:
                    args.append(xml_dict[present_location_string])
                    any_found = True
        elif location_string[-7:] == '.tuples':  #gives everything as [(location_string, value), ...]
            for present_location_string in xml_dict.keys():
                if location_string[:-7] == present_location_string[:len(location_string) - 7] and xml_dict[present_location_string] != None:
                    args.append((present_location_string, xml_dict[present_location_string]))
                    any_found = True
        else:
            if location_string in xml_dict.keys() and xml_dict[location_string] != None:
                args.append(xml_dict[location_string])
                any_found = True
            else:
                args.append(None)
    if not any_found:
        return
    try:
        value = tidy(function(*args))
    except:
        raise RuntimeError(xml_dict['label'], infobox_stat, rule)
    if value != None:
        return value
    


def xml_to_infobox(xml_dict, input_dict, all_propagated_dicts):
    category = xml_dict['category']
    if category == 'Plant':
        source = infobox_checker_plants
    elif category == 'Building':
        source = infobox_checker_buildings
    elif category == 'Pawn':
        source = infobox_checker_pawns
    else:
        print(f'WARNING: no rules to handle def with category \"{category}\" defined yet, continuing')
        return
    infobox = {}
    for infobox_stat, rule in source.define_rules().items():
        val = apply_rule(xml_dict, input_dict, all_propagated_dicts, infobox_stat, rule)
        if val != None:
            infobox[infobox_stat] = val
    return infobox


def parse_infobox(input_file):
    input_infobox = {}
    with open(input_file, 'r') as f:
        for line in f.readlines():
            if line.strip()[0] != '|':
                continue
            stat = line.split('=')[0].replace('|', '').strip()
            value = line.split('=')[1].strip()
            input_infobox[stat] = value
    return input_infobox
            

def write_infobox(infobox):
    if 'type2' in infobox.keys() and infobox['type2'].lower() in ['production']:
        col = infobox['type2'].lower()
    elif infobox['type'].lower() in ['animal', 'plant', 'weapon', 'area', 'building', 'resource']:
        col = infobox['type'].lower()
    else:
        col = 'none'
    
    print('{{' + f'infobox main|{col}|')
    for stat, val in infobox.items():
        print(f'|{stat} = {val}')
    print('}}')
        

def compare_infoboxes(infobox_1, infobox_2):
    for stat_1, val_1 in infobox_1.items():
        if stat_1 not in infobox_2.keys():
            if val_1 != '':
                print(f'{stat_1}: {val_1} -> -;')
            continue
        val_2 = infobox_2[stat_1]
        if val_1.strip('\"') != infobox_2[stat_1]:
            print(f'{stat_1}: {val_1} -> {val_2};')
    for stat_2, val_2 in infobox_2.items():
        if stat_2 not in infobox_1.keys():
            print(f'{stat_2}: - -> {val_2};')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', type=str)  # label to filter for
    parser.add_argument('-c', type=str)  # category to filter for
    parser.add_argument('-f', type=str)  # other filters ("location_string: value")
    parser.add_argument('-k', type=str)  # key to analyse (works with filters)
    parser.add_argument('-a', action='store_true')  # print all location strings (works with filters)
    args = parser.parse_args()
    filters = {}       
    if args.l != None:
        filters['label'] = args.l
    if args.c != None:
        filters['category'] = args.c
    if args.f != None and len(args.f) > 0:
        for filter in args.f.split(','):
            filters.update({filter.split(':')[0].strip(): filter.split(':')[1].strip()})
    all_propagated_dicts = get_all_propagated_dicts(base_dir)
    if args.k != None:
       pp(analyse_key(all_propagated_dicts, filters, args.k))
    elif args.a:
        for target_dict in filter_dicts(all_propagated_dicts, filters):
            pp(target_dict)
    else:  # processes based on -l, -c and -f if given, input_file if not
        if args.l != None or args.c != None or args.f != None:
            input_infobox = None
            filtered_dicts = filter_dicts(all_propagated_dicts, filters)
        else:
            input_infobox = parse_infobox(input_file)
            filtered_dicts = filter_dicts(all_propagated_dicts, {'label': input_infobox['name']})
        for filtered_dict in filtered_dicts:
            print()
            pp(filtered_dict)
            output_infobox = xml_to_infobox(filtered_dict, input_infobox, all_propagated_dicts)
            if output_infobox == None:
                continue
            write_infobox(output_infobox)
            if input_infobox != None:
                compare_infoboxes(input_infobox, output_infobox)
