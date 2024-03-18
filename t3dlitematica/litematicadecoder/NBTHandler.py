import struct
from . import Utilities
import copy
from typing import Union


def Resolve(binSource:bytes , indentationWhiteSpace:int = 2) -> dict:
    jsonLines , _ = ReadCompoundTag(binSource , indentationWhiteSpace)
    return jsonLines

def ReadCompoundTag(binSource:bytes , indentationWhiteSpace:int = 2 , pointer:int = 0 , defaultIndentation:int = 0 , readName:bool = False) -> tuple[Union[dict , str] , int]:
    indentation = defaultIndentation
    name = ""
    if readName:
        name , pointer = ReadTagName(binSource , pointer)
        litematicdata = {}
        returnlitematicdata = {"name": name, "value": ""}
    else:
        pointer += 3
        litematicdata = {}

    while True:
        if binSource[pointer] == 0:
            indentation -= indentationWhiteSpace
            pointer += 1
            if indentation < defaultIndentation:
                break
        if   binSource[pointer] == 1:  # TAG_Byte
            jsonLine , pointer = ReadByteTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonLine["name"]] = jsonLine["value"]
        elif binSource[pointer] == 2:  # TAG_Short
            jsonLine , pointer = ReadShortTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonLine["name"]] = jsonLine["value"]
        elif binSource[pointer] == 3:  # TAG_Int
            jsonLine , pointer = ReadIntTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonLine["name"]] = jsonLine["value"]
        elif binSource[pointer] == 4:  # TAG_Long
            jsonLine , pointer = ReadLongTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonLine["name"]] = jsonLine["value"]
        elif binSource[pointer] == 5:  # TAG_Float
            jsonLine , pointer = ReadFloatTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonLine["name"]] = jsonLine["value"]
        elif binSource[pointer] == 6:  # TAG_Double
            jsonLine , pointer = ReadDoubleTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonLine["name"]] = jsonLine["value"]
        elif binSource[pointer] == 7:  # TAG_Byte_Array
            jsonSubLines , pointer = ReadByteArrayTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonSubLines["name"]] = jsonSubLines["value"]
        elif binSource[pointer] == 8:  # TAG_String
            jsonLine , pointer = ReadStringTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonLine["name"]] = jsonLine["value"]
        elif binSource[pointer] == 9:  # TAG_List
            jsonSubLines , pointer = ReadListTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonSubLines["name"]] = jsonSubLines["value"]
        elif binSource[pointer] == 10: # TAG_Compound
            jsonSubLines , pointer = ReadCompoundTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2 , True)
            litematicdata[jsonSubLines["name"]] = jsonSubLines["value"]
        elif binSource[pointer] == 11: # TAG_Int_Array
            jsonSubLines , pointer = ReadIntArrayTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonSubLines["name"]] = jsonSubLines["value"]
        elif binSource[pointer] == 12: # TAG_Long_Array
            jsonSubLines , pointer = ReadLongArrayTag(copy.deepcopy(binSource) , indentationWhiteSpace , pointer , indentation + 2)
            litematicdata[jsonSubLines["name"]] = jsonSubLines["value"]
        else:
            break
    if readName:
        returnlitematicdata["value"] = litematicdata
        return returnlitematicdata , pointer
    else:
        return litematicdata , pointer


def ReadByteTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent , pointer = ReadByte(binSource , pointer)
    jsonLine = {"name": tagName, "value": tagContent}
    return jsonLine , pointer


def ReadShortTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = str(struct.unpack("h" , binSource[pointer : pointer + 2]))[1 : -2]
    jsonLine = {"name": tagName, "value": tagContent}
    return jsonLine , pointer + 2


def ReadIntTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = str(struct.unpack("i" , binSource[pointer : pointer + 4]))[1 : -2]
    jsonLine = {"name": tagName, "value": tagContent}
    return jsonLine , pointer + 4


def ReadLongTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = str(struct.unpack("q" , binSource[pointer : pointer + 8]))[1 : -2]
    jsonLine = {"name": tagName, "value": tagContent}
    return jsonLine , pointer + 8


def ReadFloatTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = ReadFloat(binSource , pointer)
    jsonLine = {"name": tagName, "value": tagContent}
    return jsonLine , pointer + 4


def ReadDoubleTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = ReadDouble(binSource , pointer)
    jsonLine = {"name": tagName, "value": tagContent}
    return jsonLine , pointer + 8


def ReadByteArrayTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    length = Utilities.BigEndiannessForInt(binSource , pointer)
    jsonLines = {"name": tagName, "value": []}
    pointer += 4
    for _ in range(length):
        tagContent , pointer = ReadByte(binSource , pointer)
        jsonLines["value"].append(tagContent)

    return jsonLines , pointer


def ReadStringTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent , pointer = ReadString(binSource , pointer + 1)
    jsonLine = {"name": tagName, "value": tagContent}
    return jsonLine , pointer


def ReadListTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation , callByList = False):
    if callByList:
        tagName = "SubList"
    else:
        tagName , pointer = ReadTagName(binSource , pointer)
    jsonLines = {"name": tagName, "value": []}
    contentType = binSource[pointer]
    contentCount = Utilities.BigEndiannessForInt(binSource , pointer + 1)
    pointer += 5
    if contentType != 0:
        if contentType == 1:    # TAG_Bytes
            for _ in range(contentCount):
                tagContent , pointer = ReadByte(binSource , pointer)
                jsonLines["value"].append(tagContent)
        elif 1 < contentType < 5: #TAG_Short , TAG_Int , TAG_Long
            unpackFormat = None
            if   contentType == 2:
                unpackFormat = "h"
            elif contentType == 3:
                unpackFormat = "i"
            else:
                unpackFormat = "q"
            size = (1 << contentType) >> 1
            for _ in range(contentCount):
                tagContent = str(struct.unpack(unpackFormat , binSource[pointer : pointer + size]))[1 : -2]
                jsonLines["value"].append(tagContent)
        elif contentType == 5: # TAG_Float
            for _ in range(contentCount):
                tagContent , pointer = ReadFloat(binSource , pointer)
                jsonLines["value"].append(tagContent)
        elif contentType == 6: # TAG_Double
            for _ in range(contentCount):
                tagContent , pointer = ReadDouble(binSource , pointer)
                jsonLines["value"].append(tagContent)
        elif contentType == 8:    # TAG_String
            for _ in range(contentCount):
                pointer += 1
                tagContent , pointer = ReadString(binSource , pointer)
                jsonLines["value"].append(tagContent)
        elif contentType == 9:    # TAG_List
            for _ in range(contentCount):
                jsonSubLines , pointer = ReadListTag(binSource , indentationWhiteSpace , pointer , defaultIndentation + 2 , True)
                jsonLines["value"].append(jsonSubLines)
        elif contentType == 10:   # TAG_Compound
            for _ in range(contentCount):
                jsonSubLines , pointer = ReadCompoundTag(binSource , indentationWhiteSpace , pointer - 3 , defaultIndentation + 2 , False)
                jsonLines["value"].append(jsonSubLines)
        elif contentType == 7 or 10 < binSource[pointer] < 13:  # TAG_Byte_Array , TAG_Int_Array , TAG_Long_Array
            pass
    return jsonLines , pointer


def ReadIntArrayTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    length = Utilities.BigEndiannessForInt(binSource , pointer)
    jsonLines = {"name": tagName, "value": []}
    pointer += 4
    for _ in range(length):
        binSource = binSource.ljust(pointer + 4 , b"\x00")
        tagContent = str(struct.unpack("i" , binSource[pointer : pointer + 4]))[1 : -2]
        jsonLines["value"].append(tagContent)
        pointer += 4
    return jsonLines , pointer


def ReadLongArrayTag(binSource:bytes , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    length = Utilities.BigEndiannessForInt(binSource , pointer)
    jsonLines = {"name": tagName, "value": []}
    pointer += 4
    for _ in range(length):
        tagContent = str(struct.unpack("q" , binSource[pointer : pointer + 8]))[1 : -2]
        jsonLines["value"].append(tagContent)
        pointer += 8

    return jsonLines , pointer


def ReadString(binSource:bytes , pointer):
    string = ""
    for _ in range(binSource[pointer]):
        pointer += 1
        string += chr(binSource[pointer])
    return string , pointer + 1


def ReadFloat(binSource:bytes , pointer):
    return float(str(struct.unpack(">f" , bytearray(binSource[pointer : pointer + 4])))[1:-2]) , pointer + 4


def ReadDouble(binSource:bytes , pointer):
    return float(str(struct.unpack(">d" , binSource[pointer : pointer + 8]))[1:-2]) , pointer + 8


def ReadByte(binSource:bytes , pointer):
    binary = binSource[pointer]
    if (binary & 0b1000_0000) > 0:
        binary = -((~binary + 1) & 0b1111_1111)
    return binary , pointer + 1


def ReadTagName(binSource:bytes , pointer):
    pointer += 2
    if binSource[pointer] == 0:
        return "Unknow Name" , pointer + 1
    return ReadString(binSource , pointer)