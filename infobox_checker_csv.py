import infobox_checker_core as core
import infobox_checker_pawns as pawns
from pprint import pprint as pp
import argparse
import math
import curve


def get_all_prop_dicts(base_dirs):
    all_thing_defs_dict = {}  # dictionary of form base_name or thing_def.defName: thing_def
    for source, base_dir in base_dirs.items():
        for xml_filename in core.list_xmls(base_dir):
            all_thing_defs_dict.update(core.parse_xml(base_dir, xml_filename))
    all_things_propagated_dict = {}
    for name, thing_def in all_thing_defs_dict.items():
        if 'Abstract' not in thing_def.attrib.keys() or thing_def.attrib['Abstract'] == 'False':
            if 'ParentName' not in thing_def.attrib.keys():
                all_things_propagated_dict[name] = core.dictify_thing(thing_def)  # for the few things that have no parent
                continue
            try:
                all_things_propagated_dict[name] = core.cleanse_uninherited(core.propagate_parents(core.dictify_thing(thing_def),
                                                                 thing_def.attrib['ParentName'],
                                                                 all_thing_defs_dict))
            except KeyError:
                print(f'error with {name}, continuing')
                continue
    return all_things_propagated_dict
    

if __name__ == '__main__':
    base_dirs = {'Core': core.base_dir + 'Core/',
                 'Royalty': core.base_dir + 'Royalty/',
                 'Ideology': core.base_dir + 'Ideology/',
                 'Alpha Animals': 'alpha_biomes/AlphaAnimals-3.8/1.3',
                 'Vanilla Expanded': 'vanilla_expanded'}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', type=str)  # label to filter for
    parser.add_argument('-c', type=str)  # category to filter for
    parser.add_argument('-f', type=str)  # other filters ("location_string: value")
    args = parser.parse_args()
    filters = {}       
    if args.l != None:
        filters['label'] = args.l
    if args.c != None:
        filters['category'] = args.c
    if args.f != None and len(args.f) > 0:
        for filter in args.f.split(','):
            filters.update({filter.split(':')[0].strip(): filter.split(':')[1].strip()})
    
    all_prop_dicts = get_all_prop_dicts(base_dirs)
    #pp(all_prop_dicts['AA_OcularJelly'])
    filtered_dict_gen = core.filter_dicts(all_prop_dicts, filters)
    all_location_strings = set()
    filtered_dicts = []
    for filtered_dict in filtered_dict_gen:
        filtered_dicts.append(filtered_dict)
        for location_string in filtered_dict.keys():
            if filtered_dict[location_string] is not None and filtered_dict[location_string].strip() != '':
                all_location_strings.add(location_string)
    print(len(filtered_dicts))
    all_location_strings = list(all_location_strings)
    all_location_strings.remove('defName')
    all_location_strings = ['defName'] + all_location_strings
    with open('unprocessed.tsv', 'w') as f:
        f.write('\t'.join(all_location_strings) + '\n')
        for filtered_dict in filtered_dicts:
            spaced_loc_values = []
            for loc_str in all_location_strings:
                if loc_str not in filtered_dict or filtered_dict[loc_str] is None:
                    spaced_loc_values.append('')
                else:
                    spaced_loc_values.append(filtered_dict[loc_str].replace('\n', '\\n').replace('\t', '\\t'))
            f.write('\t'.join(spaced_loc_values) + '\n')
    for filtered_dict in filtered_dicts:
        print(filtered_dict['defName'])

    total_key_list = []
    
    output_infoboxes = []
    for filtered_dict in filtered_dicts:
        output_infobox, key_list = core.xml_to_infobox(filtered_dict, None, all_prop_dicts)
        output_infoboxes.append(output_infobox)
        for key in key_list:
            if key in output_infobox and output_infobox[key] != '' and key not in total_key_list:
                total_key_list.append(key)
    print(total_key_list)
    
    for i, infobox in enumerate(output_infoboxes):
        def_name = filtered_dicts[i]['defName']
        if def_name[:2] == 'AA':
            source = 'AA'
        elif def_name[:4] == 'AEXP':
            source = 'AEXP'
        else:
            source = ''
            
        if 'juvenileage' in infobox and 'maturityage' in infobox:
            raw_juv = float(infobox['juvenileage'])
            raw_mat = float(infobox['maturityage'])
            infobox['actual maturity age'] = str((1-1/math.e)*raw_mat)
            infobox['actual juvenile age'] = str((1-1/math.e**(raw_juv/raw_mat))*raw_mat)
        if 'hungerrate' in infobox:
            infobox['actual adult hunger'] = str(float(infobox['hungerrate'])*1.6)
            
        if 'basemeatamount' in infobox:
            base_meat_amount = float(infobox['basemeatamount'])
        else:
            base_meat_amount = 140
        if 'baseleatheramount' in infobox:
            base_leather_amount = float(infobox['baseleatheramount'])
        else:
            base_leather_amount = 40
        if 'babyscale' in infobox:
            baby_scale = float(infobox['babyscale'])
        else:
            baby_scale = 0.2
        if 'bodysize' in infobox:
            body_size = float(infobox['bodysize'])
        else:
            baby_scale = 1
        
        infobox['adult meat yield'] = str(curve.post_process_curve(body_size*base_meat_amount))
        infobox['baby meat yield'] = str(curve.post_process_curve(body_size*base_meat_amount*baby_scale))
        infobox['adult leather yield'] = str(curve.post_process_curve(body_size*base_leather_amount))
        infobox['baby leather yield'] = str(curve.post_process_curve(body_size*base_leather_amount*baby_scale))
        infobox['source'] = source
    
    total_key_list += ['actual maturity age', 'actual juvenile age', 'actual adult hunger',
                       'adult meat yield', 'baby meat yield', 'adult leather yield', 'baby leather yield', 'source']     
            
    
    with open('infobox_processed.tsv', 'w') as f:
        f.write('\t'.join(total_key_list) + '\n')
        for i, output_infobox in enumerate(output_infoboxes):
            spaced_infobox_values = []
            for key in total_key_list:
                if key not in output_infobox or output_infobox[key] is None:
                    spaced_infobox_values.append('')
                else:
                    spaced_infobox_values.append(output_infobox[key].replace('\n', '\\n').replace('\t', '\\t'))
            f.write('\t'.join(spaced_infobox_values) + '\n')
