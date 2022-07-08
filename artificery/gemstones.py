import typer
from artificery.database import Database
from artificery import artificer 
import random

# --------------------------------------- Constants ----------------------------------------------------------

GEMSTONES = "gemstones"
GEMSTONE = "gemstone"
VALUE = "value"
NAME = "name"
AMOUNT = "amount"
UNIT = "unit"
GOLD = 'gp'
CAPACITY = "magical_capacity"
SLOTS = "spell_slots"
MAX_LEVEL = "max_level"
IS_FRAGILE = "is_fragile"

DATA = "loot_data"


# --------------------------------------- Pymongo Setup ------------------------------------------------------

db = Database()

# --------------------------------------- Typer Setup --------------------------------------------------------

app = typer.Typer()


# --------------------------------------- Functions ----------------------------------------------------------

def set_capacity(fragility, tier):
    capacity = {}
    slot_ranges = [
        [3, 5], [4, 6], [5, 7],
        [7, 9], [9, 12], [12, 15],
        [14, 16], [16, 19], [18, 21]]

    low_bound = slot_ranges[tier][0]
    high_bound = slot_ranges[tier][1]

    capacity[SLOTS] = random.randint(low_bound, high_bound)
    capacity[MAX_LEVEL] = tier + 2
    if fragility > tier:
        capacity[IS_FRAGILE] = True
    else:
        capacity[IS_FRAGILE] = False

def get_capacity(value):
    capacity = {}
    fragility = random.randint(1, 10)

    if value <= 10:
        capacity = set_capacity(fragility, 0)
        
    elif value > 10 and value <= 25:
        capacity = set_capacity(fragility, 1)

    elif value > 25 and value <= 50:
        capacity = set_capacity(fragility, 2)

    elif value > 50 and value <= 100:
        capacity = set_capacity(fragility, 3)

    elif value > 100 and value <= 250:
        capacity = set_capacity(fragility, 4)

    elif value > 250 and value <= 500:
        capacity = set_capacity(fragility, 5)

    elif value > 500 and value <= 750:
        capacity = set_capacity(fragility, 6)

    elif value > 750 and value <= 1000:
        capacity = set_capacity(fragility, 7)

    elif value > 1000 and value <= 2500:
        capacity = set_capacity(fragility, 8)

    return capacity


def make_gemstone(uncut_gem):
    gem = {
        NAME: uncut_gem[NAME],
        VALUE: {
            AMOUNT: uncut_gem[VALUE],
            UNIT: GOLD
        },
        CAPACITY: get_capacity(uncut_gem[VALUE]),
        DATA: uncut_gem[DATA]
    }
    return gem


def make_gemstones(gem_list):
    gems = []
    for uncut_gem in gem_list:
        gems.append(make_gemstone(uncut_gem))
    return gems


# --------------------------------------- Typer Commands -----------------------------------------------------

@app.command("add")
def add_gemstones(file: str, debug: bool = typer.Option(False, help="print the results to test if working")):
    """
    Add gemstones to database from csv file
    """
    try:
        gem_list = artificer.make_items(file, GEMSTONE)
        gems = make_gemstones(gem_list)
        if debug:
            for gem in gems:
                typer.echo(gem)
        else:
            db.gemstones.insert_many(gems)
    except Exception as e:
        typer.echo("an exception occured", e)
    else:
        typer.echo(f"added gemstones to database from {file}")


@app.command("add_one")
def add_gemstone(value: str, name: str, debug: bool = typer.Option(False, help="print the results to test if working")):
    """
    add single gemstone to database from command line
    """
    value = int(value)
    try:
        uncut_gem = artificer.make_item(GEMSTONE, name=name, value=value)
        gem = make_gemstone(uncut_gem)
        if debug:
            typer.echo(gem)
        else:
            db.gemstones.insert_one(gem)
    except Exception as e:
        typer.echo("an exception occured", e)
    else:
        typer.echo(f"added {name} gemstone with value {value} to the database")


# --------------------------------------- Program Operations -------------------------------------------------
if __name__ == "__main__":
    # runs the app
    app()
