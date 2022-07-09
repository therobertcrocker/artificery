import typer

from artificery import gemstones
from artificery import trinkets

app = typer.Typer()

app.add_typer(gemstones.app, name="gemstones")
app.add_typer(trinkets.app, name="trinkets")



