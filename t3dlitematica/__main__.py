import os
from pathlib import Path
import click
import json
from alive_progress import alive_bar
from .litematicadecoder import Resolve
from .objbuilder import LitimaticaToObj
from .texturepackexport import convert_texturepack


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
        if not value.endswith(".litematic") and not value.endswith(".json"):
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
@click.option("-f", "--filename", "filename", default="output.json", help="Output file name")
def Decode(litematica, output, filename):
    """
    Decode a litematica file to json file
    """
    path = Path(output).absolute()
    with alive_bar(bar="bubbles", spinner="wait"):
        data = Resolve(litematica)
    with open(os.path.join(path,filename), "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)


@cli.command()
@click.argument("json_or_litematica", type=LitematicaOrJson())
@click.argument("texturefolder", type=click.Path(exists=True))
@click.option("-o", "--output", "output", default="./", help="Output file path")
def Obj(json_or_litematica, texturefolder, output):
    """
    Convert a litematica file to obj file
    """
    json_or_litematica = Path(json_or_litematica).absolute()
    TextureFolder = Path(texturefolder).absolute()
    output = Path(output).absolute()
    with alive_bar(bar="bubbles", spinner="wait"):
        if str(json_or_litematica).endswith(".litematic"):
            litematica = Resolve(json_or_litematica)
        else:
            print(json_or_litematica)
            with open(json_or_litematica, "r", encoding="utf8") as f:
                litematica = json.load(f)
        LitimaticaToObj(litematica, TextureFolder, output)


@cli.command()
@click.argument("texturepack", type=click.Path(exists=True))
@click.option("-o", "--output", "output", default="./temp", help="Output file path")
def Texture(texturepack, output):
    """
    Convert texture pack for 3d litematica
    """
    texturepack = Path(texturepack).absolute()
    output = Path(output).absolute()
    with alive_bar(bar="bubbles", spinner="wait"):
        convert_texturepack(texturepack, output)


if __name__ == "__main__":
    cli()
