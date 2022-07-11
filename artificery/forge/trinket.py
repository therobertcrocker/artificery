
from typing import Any


# --------------------------------------- Constants ----------------------------------------------------------

CATEGORY = "category"
DESCRIPTION = "description"
IS_NESTED = "is_nested"
GROUP = "nested_group"
PROPERTIES = "properties"

DATA = "loot_data"


# --------------------------------------- Functions ----------------------------------------------------------


def get_properties(description: str):
    properties = {}
    if "<" in description:
        properties[IS_NESTED] = True
        properties[GROUP] = description.split("<")[1].split(">")[0]

    return properties


def make_trinket(raw_trinket: dict[str, Any]):
    trinket = {}
    trinket[CATEGORY] = raw_trinket[CATEGORY]
    trinket[DESCRIPTION] = raw_trinket[DESCRIPTION]
    trinket[PROPERTIES] = get_properties(raw_trinket[DESCRIPTION])
    trinket[DATA] = raw_trinket[DATA]
    return trinket


def make_trinkets(trinket_list: list[dict[str, Any]]):
    trinkets = []
    for raw_trinket in trinket_list:
        trinkets.append(make_trinket(raw_trinket))
    return trinkets

