from json import loads
from os import remove
from nose.tools import assert_equal

from parser import make_json, get_value, forbid

make_json("texforscavvies509.tex", "test.txt")
with open("test.txt", "r") as f:
    strlst = f.read()
lst = [loads(s) for s in strlst.split("\n\n")]
items, scavlympics = (lst[0], lst[1])

def test_list_length():
    assert_equal(len(items), 314)
    assert_equal(len(scavlympics), 10)


def test_get_value():
    assert_equal(get_value("1 point"), 1)
    assert_equal(get_value("2 points"), 2)
    assert_equal(get_value("3.5 points"), 3.5)
    assert_equal(get_value("5+3 points"), 8)
    assert_equal(get_value("3 points. 10 if condition met."), -1)
    assert_equal(get_value("\delta points"), -1)
    assert_equal(get_value("\frac{120}{2} points"), -1)


def test_item_232():
    obs = [item for item in items if item["number"] == 232][0]
    assert_equal(obs["min"], 26.2)
    assert_equal(obs["max"], 26.2)


def test_forbid():
    assert_equal(forbid(112, 13), 114)
    assert_equal(forbid(100, 0), 102)
    assert_equal(forbid(112, None), 112)
