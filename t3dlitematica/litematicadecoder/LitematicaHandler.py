from . import NBTHandler
from . import Utilities


def Resolve(fPath):
    litematic = open(fPath , "rb")
    binSource = Utilities.GZipUnzip(litematic.read())
    return decode_BlockStates(to_human(NBTHandler.Resolve(binSource)))

def to_human(Resolve_data):
    for i in Resolve_data["Regions"]:
        for y in Resolve_data["Regions"][i]["Size"]:
            Resolve_data["Regions"][i]["Size"][y] = str(int(int(Resolve_data["Regions"][i]["Size"][y])/16777216))
        for y,z in enumerate(Resolve_data["Regions"][i]["TileEntities"]):
            # for z in Resolve_data["Regions"][i]["TileEntities"][y]:
            #     if z == "x" or z == "y" or z == "z":
            #         Resolve_data["Regions"][i]["TileEntities"][y][z] = str(int(Resolve_data["Regions"][i]["TileEntities"][y][z])/16777216)
            for hh in Resolve_data["Regions"][i]["TileEntities"][y]:
                if hh == "x" or hh == "y" or hh == "z":
                    Resolve_data["Regions"][i]["TileEntities"][y][hh] = str(int(int(Resolve_data["Regions"][i]["TileEntities"][y][hh])/16777216))

    return Resolve_data
            

def decode_BlockStates(Resolve_data):

    #   "BlockStates":[
    #      "360323773641625836",
    #      "977288815838265344"
    #   ]    
    #     (palette entries 0x00 through 0x1d are valid):

    # 0x00 - air
    # 0x01 - iron_block
    # 0x02 - white_concrete
    # (first couple of words of BlockState, spaces added for clarity):

    # 0x 1084 4201 8410 8400
    # 0x 4210 8420 8400 0842

    # Grouping the first word's binary data little-endian:
    # (last) (0001) 00001 00001 00010 00010 00010 00010 00010 00001 00001 00001 00000 00000 (first)

    for i in Resolve_data["Regions"]:
        Resolve_data["Regions"][i]["decode_BlockStates"] = []
        for y in Resolve_data["Regions"][i]["BlockStates"]:
            # 將Y轉換long array
            y = int(y)
            y = bin(y)[2:]
            y = y.zfill(64)
            print(y)
            # 去除頭0000
            y = y[4:]
            # 每六格一組
            y = [y[i:i+3] for i in range(0, len(y), 3)]
            # 將每組轉換成int
            y = [int(i, 2) for i in y]
            print(y)
            for z in y:
                Resolve_data["Regions"][i]["decode_BlockStates"].append(Resolve_data["Regions"][i]["BlockStatePalette"][z])

    return Resolve_data



            

            



            







    return Resolve_data

