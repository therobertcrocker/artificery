import typer
from artificery.database import Database
from artificery import artificer
from artificery import forge

# --------------------------------------- Constants ----------------------------------------------------------

TRINKET = "trinket"

# --------------------------------------- Pymongo Setup ------------------------------------------------------

db = Database()

# --------------------------------------- Typer Setup --------------------------------------------------------

app = typer.Typer()

# --------------------------------------- Typer Commands -----------------------------------------------------


@app.command("add")
def add_trinkets(
    filename: str,
    debug: bool = typer.Option(False, help="print the results to test if working"),
):
    """
    Add trinkets to database from csv file
    """
    try:
        trinket_list = artificer.make_items(filename, TRINKET)
        trinkets = forge.make_trinkets(trinket_list)
        if debug:
            for trinket in trinkets:
                typer.echo(trinket)
        else:
            db.trinkets.insert_many(trinkets)
    except Exception as e:
        typer.echo("an exception occured", e)
    else:
        typer.echo(f"added trinkets to database from {filename}")


@app.command("add_one")
def add_trinket(
    category: str,
    description: str,
    debug: bool = typer.Option(False, help="print the results to test if working"),
):
    """
    add single trinket to database from command line
    """
    try:
        raw_trinket = artificer.make_item(
            TRINKET, category=category, description=description
        )
        trinket = forge.make_trinket(raw_trinket)
        if debug:
            typer.echo(trinket)
        else:
            db.trinkets.insert_one(trinket)
    except Exception as e:
        typer.echo("an exception occured", e)
    else:
        typer.echo(
            f"added {category} trinket with description '{description}' to the database"
        )


# --------------------------------------- Program Operations -------------------------------------------------
if __name__ == "__main__":
    # runs the app
    app()
