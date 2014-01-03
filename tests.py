from json import loads
from os import remove

from parser import make_json, get_values, forbid

make_json("texforscavvies509.tex", "test.txt")
with open("test.txt", "r") as f:
    strlst = f.read()
lst = [loads(s) for s in strlst.split("\n\n")]
items, scavlympics = (lst[0], lst[1])

def test_list_length():
    assert(len(items)==314)
    assert(len(scavlympics)==10)


def test_get_values():
    assert(get_values("1 point") == (1,1))
    assert(get_values("2 points") == (2,2))
    assert(get_values("3.5 points") == (3.5, 3.5))
    assert(get_values("5+3 points") == (8, 8))
    assert(get_values("3 points. 10 if condition met.") == (None, None))
    assert(get_values("\delta points") == (None, None))
    assert(get_values("\frac{120}{2} points") == (None, None))


def test_item_232():
    obs = filter(lambda x: x['number']==232, items)[0]
    assert(obs["min"] == 26.2)
    assert(obs["max"] == 26.2)

def test_forbid():
    # print forbid(99, -1)
    print forbid(112, 13)
    assert(False)
