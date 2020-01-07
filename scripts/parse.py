"""
Parse the contents of the people.json file to output each field
in different files. Used to run things like sort, uniq, grep, etc
to examine data.
"""
import json
import os
import sys


OUTDIR = 'out'


def parse_resources(resources_dir):
    filename = os.path.join(resources_dir, 'people.json')
    with open(filename, 'r') as f:
        data = json.load(f)
    count_keys = ['has_died', 'gender', 'company_id']
    count_dict = {k: {} for k in count_keys}
    list_keys = ['balance', 'email', 'phone', 'address', 'registered']
    list_dict = {k: [] for k in list_keys}
    nested_keys = ['tags', 'favouriteFood']
    nested_dict = {k: [] for k in nested_keys}
    for person in data:
        for k in count_keys:
            v = person.get(k)
            if v not in count_dict[k]:
                count_dict[k][v] = 1
            else:
                count_dict[k][v] += 1
            
        for k in list_keys:
            list_dict[k].append(person.get(k))
        
        for k in nested_keys:
            for v in person[k]:
                # nested_dict[k].append("{}: {}".format(person['index'], v))
                nested_dict[k].append(v)
    
    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)
    
    for k in count_keys:
        outfile = "{}.txt".format(k)
        outpath = os.path.join(OUTDIR, outfile)
        with open(outpath, 'w') as f:
            for value, count in count_dict[k].items():
                f.write("{}: {}\n".format(value, count))

    for k in list_keys:
        outfile = "{}.txt".format(k)
        outpath = os.path.join(OUTDIR, outfile)
        with open(outpath, 'w') as f:
            for value in list_dict[k]:
                f.write("{}\n".format(value))
    
    for k in nested_keys:
        outfile = "{}.txt".format(k)
        outpath = os.path.join(OUTDIR, outfile)
        with open(outpath, 'w') as f:
            for value in nested_dict[k]:
                f.write("{}\n".format(value))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python parse.py <resources_dir>')
        exit(1)
    parse_resources(sys.argv[1])
