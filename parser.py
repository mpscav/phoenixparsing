from re import search
from json import dumps

def split_into_sections(fh):
    "Split the file into two sections: scavlympics and items."
    with open(fh, 'r') as f:
        scavlist = f.read()
        scavlympics = get_section(scavlist, "Scav Olympics")
        items = get_section(scavlist, "Items")
    return scavlympics, items


def get_section(lst, name):
    "Grab a named section and split into pages and items."
    begin = lst.index("\\section*{{{}}}".format(name))
    item_start = begin+lst[begin:].index("\\item ")
    item_end = item_start+lst[item_start:].index("\\end{list}")
    section = lst[item_start:item_end]
    if "\\newpage" in section:
        pages = section.split("\\newpage")
        items = [page.split("\\item ")[1:] for page in pages]
    else:
        items = section.split("\\item ")[1:]
        items = [item.strip() for item in items]
    return items


def parse_item(item, pagenum):
    "Turn an item into a tuple."
    match = search(r'(.*)[([](.*)[])]', item)
    if match:
        text, value = match.groups()
    else:
        text = item
        value = None
    return (text.strip(), value, pagenum)


def make_json(infile, outfile):
    "Convert a Scav list in LaTeX into JSON."
    def thirteen(x):
        return int((x+86)/99 + x)
    scavlympics, items = split_into_sections(infile)
    items = [parse_item(item, pagenum + 1)
             for pagenum, page in enumerate(items[:-1]) for item in page]
    # add item numbers & dictify
    items = [{'number':thirteen(i+1), # 2014 scav
              'page':pagenum,
              'text':text,
              'value': value}
             for i, (text, value, pagenum) in enumerate(items)]
    items_json = (dumps(items, sort_keys=True, indent=4))
    scavlympics_json = (dumps(scavlympics, sort_keys=True, indent=4))
    if outfile:
        with open(outfile, 'w') as f:
            f.write(items_json)
            f.write('\n')
            f.write(scavlympics_json)
    else:
        print items_json
        print scavlympics_json


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Parse a Scav list to JSON.")
    parser.add_argument("infile", help="The list to parse.")
    parser.add_argument("-o", "--outfile", dest="outfile",
                        help="Output file to dump JSON to. Defaults to stdout.")
    args = parser.parse_args()
    make_json(args.infile, args.outfile)
