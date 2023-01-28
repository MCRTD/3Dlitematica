import struct
from . import Utilities


def Resolve(binSource , indentationWhiteSpace = 2):
    jsonLines , _ = ReadCompoundTag(binSource , indentationWhiteSpace)
    RemoveComma(jsonLines)
    json = ""
    for jsonLine in jsonLines:
        json += jsonLine + "\n"
        json += jsonLine
    return json

#TODO: 重寫這裡
def ReadCompoundTag(binSource , indentationWhiteSpace = 2 , pointer = 0 , defaultIndentation = 0 , readName = False):
    indentation = defaultIndentation
    name = ""
    jsonLines = []
    if readName:
        name , pointer = ReadTagName(binSource , pointer)
        jsonLines += [" " * indentation + f"\"{name}\": " + "{"]
    else:
        pointer += 3
        jsonLines += [" " * indentation + "{"]
    while True:
        if binSource[pointer] == 0:
            jsonLines = RemoveComma(jsonLines)
            jsonLine = " " * indentation + "},"
            jsonLines += [jsonLine]
            indentation -= indentationWhiteSpace
            pointer += 1
            if indentation < defaultIndentation:
                break

        if   binSource[pointer] == 1:  # TAG_Byte
            jsonLine , pointer = ReadByteTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += [jsonLine]
        elif binSource[pointer] == 2:  # TAG_Short
            jsonLine , pointer = ReadShortTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += [jsonLine]
        elif binSource[pointer] == 3:  # TAG_Int
            jsonLine , pointer = ReadIntTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += [jsonLine]
        elif binSource[pointer] == 4:  # TAG_Long
            jsonLine , pointer = ReadLongTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += [jsonLine]
        elif binSource[pointer] == 5:  # TAG_Float
            jsonLine , pointer = ReadFloatTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += [jsonLine]
        elif binSource[pointer] == 6:  # TAG_Double
            jsonLine , pointer = ReadDoubleTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += [jsonLine]
        elif binSource[pointer] == 7:  # TAG_Byte_Array
            jsonSubLines , pointer = ReadByteArrayTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += jsonSubLines
        elif binSource[pointer] == 8:  # TAG_String
            jsonLine , pointer = ReadStringTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += [jsonLine]
        elif binSource[pointer] == 9:  # TAG_List
            jsonSubLines , pointer = ReadListTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += jsonSubLines
        elif binSource[pointer] == 10: # TAG_Compound
            jsonSubLines , pointer = ReadCompoundTag(binSource , indentationWhiteSpace , pointer , indentation + 2 , True)
            jsonLines += jsonSubLines
        elif binSource[pointer] == 11: # TAG_Int_Array
            jsonSubLines , pointer = ReadIntArrayTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += jsonSubLines
        elif binSource[pointer] == 12: # TAG_Long_Array
            jsonSubLines , pointer = ReadLongArrayTag(binSource , indentationWhiteSpace , pointer , indentation + 2)
            jsonLines += jsonSubLines
        else:
            break
    return jsonLines , pointer


def ReadByteTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent , pointer = ReadByte(binSource , pointer)
    jsonLine = " " * defaultIndentation + f"\"{tagName}\": {tagContent},"
    return jsonLine , pointer


def ReadShortTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = str(struct.unpack("h" , binSource[pointer : pointer + 2]))[1 : -2]
    jsonLine = " " * defaultIndentation + f"\"{tagName}\": {tagContent},"
    return jsonLine , pointer + 2


def ReadIntTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = str(struct.unpack("i" , binSource[pointer : pointer + 4]))[1 : -2]
    jsonLine = " " * defaultIndentation + f"\"{tagName}\": {tagContent},"
    return jsonLine , pointer + 4


def ReadLongTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = str(struct.unpack("q" , binSource[pointer : pointer + 8]))[1 : -2]
    jsonLine = " " * defaultIndentation + f"\"{tagName}\": {tagContent},"
    return jsonLine , pointer + 8


def ReadFloatTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = ReadFloat(binSource , pointer)
    jsonLine = " " * defaultIndentation + f"\"{tagName}\": {tagContent},"
    return jsonLine , pointer + 4


def ReadDoubleTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent = ReadDouble(binSource , pointer)
    jsonLine = " " * defaultIndentation + f"\"{tagName}\": {tagContent}"
    return jsonLine , pointer + 8


def ReadByteArrayTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    length = Utilities.BigEndiannessForInt(binSource , pointer)
    jsonLines = [" " * (defaultIndentation - indentationWhiteSpace) + f"\"{tagName}\": ["]
    pointer += 4
    indentation = defaultIndentation + indentationWhiteSpace
    for i in range(0 , length):
        tagContent , pointer = ReadByte(binSource , pointer)
        jsonLines += [" " * indentation + f"{tagContent},"]
    jsonLines = RemoveComma(jsonLines)
    jsonLines += [" " * defaultIndentation + "],"]
    print(pointer)
    return jsonLines , pointer


def ReadStringTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    tagContent , pointer = ReadString(binSource , pointer + 1)
    jsonLine = " " * defaultIndentation+ f"\"{tagName}\": \"{tagContent}\","
    return jsonLine , pointer


def ReadListTag(binSource , indentationWhiteSpace , pointer , defaultIndentation , callByList = False):
    if callByList:
        tagName = "SubList"
    else:
        tagName , pointer = ReadTagName(binSource , pointer)
    jsonLines = [" " * defaultIndentation + f"\"{tagName}\": ["]
    contentType = binSource[pointer]
    contentCount = Utilities.BigEndiannessForInt(binSource , pointer + 1)
    pointer += 5
    indentation = defaultIndentation + indentationWhiteSpace
    if contentType != 0:
        if   contentType == 1:    # TAG_Bytes
            for i in range(0 , contentCount):
                tagContent , pointer = ReadByte(binSource , pointer)
                jsonLines += [" " * indentation + f"{tagContent},"]
        elif 1 < contentType < 5: #TAG_Short , TAG_Int , TAG_Long
            unpackFormat = None
            if   contentType == 2:
                unpackFormat = "h"
            elif contentType == 3:
                unpackFormat = "i"
            else:
                unpackFormat = "q"
            size = (1 << contentType) >> 1
            for i in range(0 , contentCount):
                tagContent = str(struct.unpack(unpackFormat , binSource[pointer : pointer + size]))[1 : -2]
                jsonLines = [" " * indentation + f"{tagContent},"]
        elif contentType == 5: # TAG_Float
            for i in range(0 , contentCount):
                tagContent , pointer = ReadFloat(binSource , pointer)
                jsonLines += [" " * indentation + f"{tagContent},"]
        elif contentType == 6: # TAG_Double
            for i in range(0 , contentCount):
                tagContent , pointer = ReadDouble(binSource , pointer)
                jsonLines += [" " * indentation + f"{tagContent},"]
        elif contentType == 8:    # TAG_String
            for i in range(0 , contentCount):
                tagContent , pointer = ReadString(binSource , pointer)
                jsonLines += [" " * indentation + f"{tagContent},"]
        elif contentType == 9:    # TAG_List
            for i in range(0 , contentCount):
                jsonSubLines , pointer = ReadListTag(binSource , indentationWhiteSpace , pointer , defaultIndentation + 2 , True)
                jsonLines += jsonSubLines
        elif contentType == 10:   # TAG_Compound
            for i in range(0 , contentCount):
                jsonSubLines , pointer = ReadCompoundTag(binSource , indentationWhiteSpace , pointer - 3 , defaultIndentation + 2 , False)
                jsonLines += jsonSubLines
        elif contentType == 7 or 10 < binSource[pointer] < 13:  # TAG_Byte_Array , TAG_Int_Array , TAG_Long_Array
            pass
        jsonLines = RemoveComma(jsonLines)
    jsonLines += [" " * defaultIndentation + "],"]
    return jsonLines , pointer


def ReadIntArrayTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    length = Utilities.BigEndiannessForInt(binSource , pointer)
    jsonLines = [" " * defaultIndentation + f"\"{tagName}\": ["]
    pointer += 4
    indentation = defaultIndentation + indentationWhiteSpace
    for i in range(0 , length):
        tagContent = str(struct.unpack("i" , binSource[pointer : pointer + 4]))[1 : -2]
        jsonLines += [" " * indentation + f"{tagContent},"]
        pointer += 4
    jsonLines = RemoveComma(jsonLines)
    jsonLines += [" " * defaultIndentation + "],"]
    return jsonLines , pointer


def ReadLongArrayTag(binSource , indentationWhiteSpace , pointer , defaultIndentation):
    tagName , pointer = ReadTagName(binSource , pointer)
    length = Utilities.BigEndiannessForInt(binSource , pointer)
    jsonLines = [" " * defaultIndentation + f"\"{tagName}\": ["]
    pointer += 4
    indentation = defaultIndentation + indentationWhiteSpace
    for i in range(0 , length):
        tagContent = str(struct.unpack("q" , binSource[pointer : pointer + 8]))[1 : -2]
        jsonLines += [" " * indentation + f"{tagContent},"]
        pointer += 8
    jsonLines = RemoveComma(jsonLines)
    jsonLines += [" " * defaultIndentation + "],"]
    return jsonLines , pointer


def ReadString(binSource , pointer):
    string = ""
    for i in range(0 , binSource[pointer]):
        pointer += 1
        string += chr(binSource[pointer])
    return string , pointer + 1


def ReadFloat(binSource , pointer):
    return float(str(struct.unpack(">f" , bytearray(binSource[pointer : pointer + 4])))[1:-2]) , pointer + 4


def ReadDouble(binSource , pointer):
    return float(str(struct.unpack(">d" , binSource[pointer : pointer + 8]))[1:-2]) , pointer + 8


def ReadByte(binSource , pointer):
    binary = binSource[pointer]
    if (binary & 0b1000_0000) > 0:
        binary = -((~binary + 1) & 0b1111_1111)
    return binary , pointer + 1


def ReadTagName(binSource , pointer):
    pointer += 2
    if binSource[pointer] == 0:
        return "Unknow Name" , pointer + 1
    return ReadString(binSource , pointer)


def RemoveComma(jsonLines):
    lastIndex = len(jsonLines) - 1
    length = len(jsonLines[lastIndex])
    jsonLines[lastIndex] = jsonLines[lastIndex][0 : length - 1]
    return jsonLines