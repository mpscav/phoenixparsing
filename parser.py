from re import search
from json import dumps

def split_into_sections(fh):
    with open(fh, 'r') as f:
        scavlist = f.read()
        scavlympics = get_section(scavlist, "Scav Olympics")
        items = get_section(scavlist, "Items")
    return scavlympics, items


def get_section(lst, name):
    begin = lst.index("\\section*{{{}}}".format(name))
    item_start = begin+lst[begin:].index("\\item ")
    item_end = item_start+lst[item_start:].index("\\end{list}")
    section = lst[item_start:item_end]
    if "\\newpage" in section:
        pages = section.split("\\newpage")
        items = [page.split("\\item ")[1:] for page in pages]
    else:
        items = section.split("\\item ")[1:]
    return items


def parse_item(item, pagenum):
    match = search(r'(.*)[([](.*)[])]', item)
    if match:
        text, value = match.groups()
    else:
        text = item
        value = None
    return (text, value, pagenum)


def twentythirteen(x):
    return int((x+87)/100 + x)


def make_json(infile, outfile):
    scavlympics, items = split_into_sections(infile)
    pages = [[parse_item(item, pagenum + 1) for item in page]
             for pagenum, page in enumerate(items[:-1])]
    del pages[12] # 2014 Scav
    items = [item for page in pages for item in page]
    items = [{'number':twentythirteen(i), # 2014 scav
              'page':pagenum,
              'text':text,
              'value': value}
             for i, (text, value, pagenum) in enumerate(items)]
    with open(outfile, 'w') as f:
        f.write(dumps(items, sort_keys=True, indent=4))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Parse a Scav list to JSON.")
    parser.add_argument("infile", help="The list to parse.")
    parser.add_argument("outfile", help="Output file to dump JSON to.")
    args = parser.parse_args()
    make_json(args.infile, args.outfile)
