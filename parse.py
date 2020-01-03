import json
import os


OUTDIR = 'out'


def parse_people(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    count_keys = ['has_died', 'gender', 'company_id']
    count_dict = {k: {} for k in count_keys}
    list_keys = ['balance', 'email', 'phone', 'address', 'registered']
    list_dict = {k: [] for k in list_keys}
    nested_keys = ['tags']
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
                nested_dict[k].append("{}: {}".format(person['index'], v))
    
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
    people_filename = os.path.join('resources', 'people.json')
    parse_people(people_filename)
