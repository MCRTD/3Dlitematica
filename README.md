# 3Dlitematica

> [!WARNING]
> This project is a pre-release, and we do not guarantee that all functions will be available.

# Install 
```bash
pip install --upgrade 3dLitematica
```

# CLI

```
3dLitematica [OPTION] command
```

# Option

```

Options:
  --help           Show this message and exit.

Commands:
  decode   Decode a litematica file to json file
  obj      Convert a litematica file to obj file
  texture  Convert texture pack for 3d litematica

```

# Decode

```
Usage: 3dlitematica decode [OPTIONS] LITEMATICA
Example: 3dlitematica decode -o ./ -f output.json fss.litematica

  Decode a litematica file to json file

Options:
  -o, --output TEXT    Output file path
  -f, --filename TEXT  Output file name
```

# Obj
```
Usage: 3dlitematica obj [OPTIONS] JSON_OR_LITEMATICA TEXTUREFOLDER
Example: 3dlitematica obj -o ./ fss.litematica ./temp

  Convert a litematica file to obj file

Options:
  -o, --output TEXT  Output file path
  --help             Show this message and exit.
```

# texture
```
Usage: 3dlitematica texture [OPTIONS] TEXTUREPACK
Example: 3dlitematica texture -o ./temp ./minecraft_pack
  Convert texture pack for 3dlitematica

Options:
  -o, --output TEXT  Output file path
  --help             Show this message and exit.
```

