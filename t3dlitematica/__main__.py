from click import command, echo, option
from litematicadecoder import Resolve
from objbuilder import objhandel
from texturepackexport import convert_texturepack


@command
@option("--count", default=1, help="Number of greetings.")
@option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    for _ in range(count):
        echo(f"Hello, {name}!")