import typer

from artificery import gemstones

app = typer.Typer()
app.add_typer(gemstones.app, name="gemstones")



