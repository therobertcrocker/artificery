from curses import raw
from sre_constants import CATEGORY
import typer
from artificery.database import Database
from artificery import artificer 

# --------------------------------------- Constants ----------------------------------------------------------

TRINKETS = "trinkets"
TRINKET = "trinket"
CATEGORY = "category"
DESCRIPTION = "description"
IS_NESTED = "is_nested"
GROUP = "nested_group"
PROPERTIES = "properties"

DATA = "loot_data"


# --------------------------------------- Pymongo Setup ------------------------------------------------------

db = Database()

# --------------------------------------- Typer Setup --------------------------------------------------------

app = typer.Typer()


# --------------------------------------- Functions ----------------------------------------------------------


def get_properties(description):
    properties = {}
    if "<" in description:
        properties[IS_NESTED] = True
        properties[GROUP] = description.split('<')[1].split('>')[0]

    return properties

def make_trinket(raw_trinket):
    trinket = {}
    trinket[CATEGORY] = raw_trinket[CATEGORY]
    trinket[DESCRIPTION] = raw_trinket[DESCRIPTION]
    trinket[PROPERTIES] = get_properties(raw_trinket[DESCRIPTION])
    trinket[DATA] = raw_trinket[DATA]
    return trinket


def make_trinkets(trinket_list):
    trinkets = []
    for raw_trinket in trinket_list:
        trinkets.append(make_trinket(raw_trinket))
    return trinkets


# --------------------------------------- Typer Commands -----------------------------------------------------

@app.command("add")
def add_trinkets(file: str, debug: bool = typer.Option(False, help="print the results to test if working")):
    """
    Add trinkets to database from csv file
    """
    try:
        trinket_list = artificer.make_items(file, TRINKET)
        trinkets = make_trinkets(trinket_list)
        if debug:
            for trinket in trinkets:
                typer.echo(trinket)
        else:
            db.trinkets.insert_many(trinkets)
    except Exception as e:
        typer.echo("an exception occured", e)
    else:
        typer.echo(f"added trinkets to database from {file}")


@app.command("add_one")
def add_trinket(category: str, description: str, debug: bool = typer.Option(False, help="print the results to test if working")):
    """
    add single trinket to database from command line
    """
    try:
        raw_trinket = artificer.make_item(TRINKET, category=category, description=description)
        trinket = make_trinket(raw_trinket)
        if debug:
            typer.echo(trinket)
        else:
            db.trinkets.insert_one(trinket)
    except Exception as e:
        typer.echo("an exception occured", e)
    else:
        typer.echo(f"added {category} trinket with description '{description}' to the database")


# --------------------------------------- Program Operations -------------------------------------------------
if __name__ == "__main__":
    # runs the app
    app()
