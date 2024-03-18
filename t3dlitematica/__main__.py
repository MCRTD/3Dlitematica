import os
import click
from litematicadecoder import Resolve
from objbuilder import objhandel
from texturepackexport import convert_texturepack


class Litematica(click.ParamType):
    name = "litematica"

    def convert(self, value, param, ctx):
        if not os.path.exists(value):
            self.fail(f"{value} does not exist.")
        if not value.endswith(".litematic"):
            self.fail(f"{value} is not a litematica file.")
        return value


class LitematicaOrJson(click.ParamType):
    name = "LitematicaOrJson"

    def convert(self, value, param, ctx):
        if not os.path.exists(value):
            self.fail(f"{value} does not exist.")
        if not value.endswith(".litematic") or not value.endswith(".json"):
            self.fail(f"{value} is not a litematica or json file.")
        return value


@click.group()
@click.option("--debug", default=False)
def cli(debug):
    if debug:
        click.echo("Debug mode is 'on' ")


@cli.command()
@click.argument("litematica", type=Litematica())
@click.option("-o", "--output", "output", default="./", help="Output file path")
def Decode(litematica, output):
    """
    Decode a litematica file to json file
    """
    print(litematica)
    click.echo("Wait")


@cli.command()
@click.argument("json/litematica", type=LitematicaOrJson())
@click.argument("TextureFolder", type=click.Path(exists=True))
@click.option("-o", "--output", "output", default="./", help="Output file path")
def Obj(data,testure,output):
    """
    Convert a litematica file to obj file
    """
    click.echo("Wait")


@cli.command()
@click.argument("texturepack", type=click.Path(exists=True))
@click.option("-o", "--output", "output", default="./", help="Output file path")
def Texture(texturepack,output):
    """
    Convert texture pack for 3d litematica
    """
    click.echo("Wait")


if __name__ == "__main__":
    cli()
