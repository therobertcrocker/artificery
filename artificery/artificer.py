import pandas

# data handling
DATA_DIR = "data_input/"

# mongoDB
DATA = "loot_data"
LOOT_TYPE = "loot_type"
TAGS = "tags"


# --------------------------------------- Data Handling ------------------------------------------------------

def parse_csv(file):
    file_path = DATA_DIR + file
    try:
        items = pandas.read_csv(file_path).to_dict(orient="records")
    except Exception as e:
        print("An exception occurred: ", e)
    else:
        return items


def make_item(loot_type, **fields):
    item = fields
    item[DATA] = {
        LOOT_TYPE: loot_type,
        TAGS: []
    }
    return item


def make_items(file, item_type):
    raw_items = parse_csv(file)
    items_list = []
    for item in raw_items:
        items_list.append(make_item(item_type, **item))
    return items_list

