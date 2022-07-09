import typer
from artificery.database import Database
from artificery import artificer
from artificery import forge

# --------------------------------------- Constants ----------------------------------------------------------

GEMSTONE = "gemstone"

# --------------------------------------- Pymongo Setup ------------------------------------------------------

db = Database()

# --------------------------------------- Typer Setup --------------------------------------------------------

app = typer.Typer()

# --------------------------------------- Typer Commands -----------------------------------------------------


@app.command("add")
def add_gemstones(
    file: str,
    debug: bool = typer.Option(False, help="print the results to test if working"),
):
    """
    Add gemstones to database from csv file
    """
    try:
        gem_list = artificer.make_items(file, GEMSTONE)
        gems = forge.make_gemstones(gem_list)
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
def add_gemstone(
    value: str,
    name: str,
    debug: bool = typer.Option(False, help="print the results to test if working"),
):
    """
    add single gemstone to database from command line
    """
    value = int(value)
    try:
        uncut_gem = artificer.make_item(GEMSTONE, name=name, value=value)
        gem = forge.make_gemstone(uncut_gem)
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
