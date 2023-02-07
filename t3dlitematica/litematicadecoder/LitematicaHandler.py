from . import NBTHandler
from . import Utilities


def Resolve(fPath):
    litematic = open(fPath , "rb")
    binSource = Utilities.GZipUnzip(litematic.read())
    return to_human(NBTHandler.Resolve(binSource))
"""
"Regions": {
        " 1": {
            "BlockStates": [
                "4620693217682128896",
                "0",
                "0",
                "0",
                "933588451196928",
                "0",
                "0",
                "192",
                "-9140959233716518912",
                "3",
                "3504693313548",
                "12340",
                "-9222461641222782976",
                "4399120533504",
                "21392119709066581",
                "38771",
                "7010985591857086464",
                "317503775340232704",
                "105553116315654",
                "6316108",
                "-7998111435584438168",
                "5262174689605716992",
                "3592104500539404",
                "14031668569977",
                "957895196679",
                "9007200683426304",
                "3499900542361217282",
                "31619922895306752",
                "223",
                "504403160211652608",
                "0",
                "0"
            ],
            "PendingBlockTicks": [],
            "Position": {
                "x": "0",
                "y": "0",
                "z": "0"
            },
            "BlockStatePalette": [
                {
                    "Name": "minecraft:air"
                },
                {
                    "Properties": {
                        "facing": "west",
                        "open": "false"
                    },
                    "Name": "minecraft:barrel"
                },
                {
                    "Properties": {
                        "facing": "west",
                        "enabled": "false"
                    },
                    "Name": "minecraft:hopper"
                },
                {
                    "Name": "minecraft:redstone_block"
                },
                {
                    "Properties": {
                        "facing": "west",
                        "extended": "false"
                    },
                    "Name": "minecraft:sticky_piston"
                },
                {
                    "Properties": {
                        "powered": "false",
                        "facing": "east"
                    },
                    "Name": "minecraft:observer"
                },
                {
                    "Properties": {
                        "powered": "false",
                        "facing": "up"
                    },
                    "Name": "minecraft:observer"
                },
                {
                    "Properties": {
                        "triggered": "false",
                        "facing": "east"
                    },
                    "Name": "minecraft:dispenser"
                },
                {
                    "Name": "minecraft:glowstone"
                },
                {
                    "Properties": {
                        "facing": "west",
                        "enabled": "true"
                    },
                    "Name": "minecraft:hopper"
                },
                {
                    "Properties": {
                        "mode": "compare",
                        "powered": "true",
                        "facing": "west"
                    },
                    "Name": "minecraft:comparator"
                },
                {
                    "Properties": {
                        "east": "none",
                        "south": "none",
                        "north": "none",
                        "west": "side",
                        "power": "1"
                    },
                    "Name": "minecraft:redstone_wire"
                },
                {
                    "Properties": {
                        "waterlogged": "false",
                        "type": "top"
                    },
                    "Name": "minecraft:smooth_stone_slab"
                },
                {
                    "Properties": {
                        "facing": "down",
                        "enabled": "false"
                    },
                    "Name": "minecraft:hopper"
                },
                {
                    "Properties": {
                        "triggered": "false",
                        "facing": "north"
                    },
                    "Name": "minecraft:dropper"
                },
                {
                    "Properties": {
                        "powered": "false",
                        "facing": "down"
                    },
                    "Name": "minecraft:observer"
                },
                {
                    "Properties": {
                        "facing": "north",
                        "enabled": "true"
                    },
                    "Name": "minecraft:hopper"
                },
                {
                    "Properties": {
                        "facing": "up",
                        "extended": "false"
                    },
                    "Name": "minecraft:sticky_piston"
                },
                {
                    "Properties": {
                        "mode": "compare",
                        "powered": "false",
                        "facing": "north"
                    },
                    "Name": "minecraft:comparator"
                },
                {
                    "Properties": {
                        "delay": "2",
                        "powered": "false",
                        "facing": "south",
                        "locked": "false"
                    },
                    "Name": "minecraft:repeater"
                },
                {
                    "Properties": {
                        "delay": "4",
                        "powered": "false",
                        "facing": "north",
                        "locked": "false"
                    },
                    "Name": "minecraft:repeater"
                },
                {
                    "Properties": {
                        "waterlogged": "false",
                        "type": "double"
                    },
                    "Name": "minecraft:smooth_stone_slab"
                },
                {
                    "Properties": {
                        "delay": "2",
                        "powered": "false",
                        "facing": "east",
                        "locked": "false"
                    },
                    "Name": "minecraft:repeater"
                },
                {
                    "Properties": {
                        "facing": "down",
                        "extended": "false"
                    },
                    "Name": "minecraft:sticky_piston"
                },
                {
                    "Properties": {
                        "powered": "false",
                        "facing": "south"
                    },
                    "Name": "minecraft:observer"
                },
                {
                    "Properties": {
                        "powered": "false",
                        "shape": "ascending_west"
                    },
                    "Name": "minecraft:powered_rail"
                },
                {
                    "Properties": {
                        "triggered": "false",
                        "facing": "down"
                    },
                    "Name": "minecraft:dropper"
                },
                {
                    "Properties": {
                        "facing": "north",
                        "extended": "false"
                    },
                    "Name": "minecraft:sticky_piston"
                },
                {
                    "Properties": {
                        "waterlogged": "false",
                        "type": "bottom"
                    },
                    "Name": "minecraft:smooth_stone_slab"
                },
                {
                    "Properties": {
                        "facing": "down",
                        "enabled": "true"
                    },
                    "Name": "minecraft:hopper"
                },
                {
                    "Properties": {
                        "powered": "false",
                        "shape": "east_west"
                    },
                    "Name": "minecraft:powered_rail"
                },
                {
                    "Name": "minecraft:white_stained_glass"
                },
                {
                    "Properties": {
                        "facing": "west",
                        "extended": "false"
                    },
                    "Name": "minecraft:piston"
                },
                {
                    "Properties": {
                        "triggered": "false",
                        "facing": "north"
                    },
                    "Name": "minecraft:dispenser"
                },
                {
                    "Properties": {
                        "delay": "3",
                        "powered": "false",
                        "facing": "south",
                        "locked": "false"
                    },
                    "Name": "minecraft:repeater"
                },
                {
                    "Properties": {
                        "delay": "1",
                        "powered": "false",
                        "facing": "south",
                        "locked": "false"
                    },
                    "Name": "minecraft:repeater"
                },
                {
                    "Properties": {
                        "mode": "subtract",
                        "powered": "false",
                        "facing": "north"
                    },
                    "Name": "minecraft:comparator"
                },
                {
                    "Properties": {
                        "east": "none",
                        "south": "side",
                        "north": "side",
                        "west": "side",
                        "power": "0"
                    },
                    "Name": "minecraft:redstone_wire"
                },
                {
                    "Properties": {
                        "delay": "2",
                        "powered": "false",
                        "facing": "north",
                        "locked": "false"
                    },
                    "Name": "minecraft:repeater"
                },
                {
                    "Properties": {
                        "east": "none",
                        "south": "none",
                        "north": "side",
                        "west": "none",
                        "power": "0"
                    },
                    "Name": "minecraft:redstone_wire"
                }
            ],
            "Size": {
                "x": "100663296",
                "y": "134217728",
                "z": "117440512"
            },
            "PendingFluidTicks": [],
            "TileEntities": [
                {
                    "x": "50331648",
                    "y": "50331648",
                    "z": "0",
                    "Items": [],
                    "id": "minecraft:dropper"
                },
                {
                    "TransferCooldown": "0",
                    "x": "50331648",
                    "y": "83886080",
                    "z": "33554432",
                    "Items": [],
                    "id": "minecraft:hopper"
                },
                {
                    "x": "50331648",
                    "y": "100663296",
                    "z": "50331648",
                    "Items": [],
                    "id": "minecraft:dispenser"
                },
                {
                    "x": "16777216",
                    "y": "0",
                    "z": "0",
                    "Items": [
                        {
                            "Slot": 0,
                            "id": "minecraft:shulker_box",
                            "Count": 1,
                            "tag": {
                                "BlockEntityTag": {
                                    "Items": [
                                        {
                                            "Slot": 0,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 1,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 2,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 3,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 4,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 5,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 6,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 7,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 8,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 9,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 10,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 11,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 12,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 13,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 14,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 15,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 16,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 17,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 18,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 19,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 20,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 21,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 22,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 23,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 24,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 25,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        },
                                        {
                                            "Slot": 26,
                                            "id": "minecraft:sand",
                                            "Count": 64
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "id": "minecraft:barrel"
                },
                {
                    "TransferCooldown": "0",
                    "x": "50331648",
                    "y": "33554432",
                    "z": "0",
                    "Items": [
                        {
                            "Slot": 0,
                            "id": "minecraft:sand",
                            "Count": 18
                        },
                        {
                            "Slot": 1,
                            "id": "minecraft:bedrock",
                            "Count": 1
                        },
                        {
                            "Slot": 2,
                            "id": "minecraft:bedrock",
                            "Count": 1
                        },
                        {
                            "Slot": 3,
                            "id": "minecraft:bedrock",
                            "Count": 1
                        },
                        {
                            "Slot": 4,
                            "id": "minecraft:bedrock",
                            "Count": 1
                        }
                    ],
                    "id": "minecraft:hopper"
                },
                {
                    "TransferCooldown": "0",
                    "x": "50331648",
                    "y": "50331648",
                    "z": "16777216",
                    "Items": [],
                    "id": "minecraft:hopper"
                },
                {
                    "x": "50331648",
                    "y": "67108864",
                    "z": "33554432",
                    "Items": [],
                    "id": "minecraft:dropper"
                },
                {
                    "x": "50331648",
                    "y": "100663296",
                    "z": "67108864",
                    "id": "minecraft:comparator",
                    "OutputSignal": "0"
                },
                {
                    "TransferCooldown": "0",
                    "x": "33554432",
                    "y": "0",
                    "z": "0",
                    "Items": [],
                    "id": "minecraft:hopper"
                },
                {
                    "x": "67108864",
                    "y": "33554432",
                    "z": "0",
                    "id": "minecraft:comparator",
                    "OutputSignal": "16777216"
                },
                {
                    "TransferCooldown": "0",
                    "x": "50331648",
                    "y": "50331648",
                    "z": "33554432",
                    "Items": [],
                    "id": "minecraft:hopper"
                },
                {
                    "x": "50331648",
                    "y": "50331648",
                    "z": "50331648",
                    "id": "minecraft:comparator",
                    "OutputSignal": "0"
                },
                {
                    "x": "16777216",
                    "y": "67108864",
                    "z": "0",
                    "Items": [],
                    "id": "minecraft:dropper"
                },
                {
                    "TransferCooldown": "0",
                    "x": "16777216",
                    "y": "50331648",
                    "z": "0",
                    "Items": [],
                    "id": "minecraft:hopper"
                },
                {
                    "TransferCooldown": "0",
                    "x": "16777216",
                    "y": "67108864",
                    "z": "16777216",
                    "Items": [],
                    "id": "minecraft:hopper"
                },
                {
                    "x": "16777216",
                    "y": "83886080",
                    "z": "33554432",
                    "Items": [],
                    "id": "minecraft:dropper"
                },
                {
                    "x": "16777216",
                    "y": "33554432",
                    "z": "0",
                    "Items": [
                        {
                            "Slot": 3,
                            "id": "minecraft:shulker_box",
                            "Count": 1
                        },
                        {
                            "Slot": 4,
                            "id": "minecraft:shulker_box",
                            "Count": 1
                        },
                        {
                            "Slot": 5,
                            "id": "minecraft:shulker_box",
                            "Count": 1
                        },
                        {
                            "Slot": 6,
                            "id": "minecraft:shulker_box",
                            "Count": 1
                        },
                        {
                            "Slot": 7,
                            "id": "minecraft:shulker_box",
                            "Count": 1
                        },
                        {
                            "Slot": 8,
                            "id": "minecraft:shulker_box",
                            "Count": 1
                        }
                    ],
                    "id": "minecraft:dispenser"
                },
                {
                    "TransferCooldown": "0",
                    "x": "16777216",
                    "y": "67108864",
                    "z": "33554432",
                    "Items": [],
                    "id": "minecraft:hopper"
                },
                {
                    "TransferCooldown": "0",
                    "x": "33554432",
                    "y": "83886080",
                    "z": "33554432",
                    "Items": [],
                    "id": "minecraft:hopper"
                },
                {
                    "TransferCooldown": "0",
                    "x": "50331648",
                    "y": "117440512",
                    "z": "50331648",
                    "Items": [],
                    "id": "minecraft:hopper"
                }
            ],
            "Entities": []
        }
    }
"""
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
            


