import json
import math
import os
from typing import Callable, List, Union
# example:
#         "cube": {
#             "parent": "block",
#             "elements": [
#                 {
#                     "from": [
#                         0,
#                         0,
#                         0
#                     ],
#                     "to": [
#                         16,
#                         16,
#                         16
#                     ],
#                     "faces": {
#                         "down": {
#                             "texture": "#down",
#                             "cullface": "down"
#                         },
#                         "up": {
#                             "texture": "#up",
#                             "cullface": "up"
#                         },
#                         "north": {
#                             "texture": "#north",
#                             "cullface": "north"
#                         },
#                         "south": {
#                             "texture": "#south",
#                             "cullface": "south"
#                         },
#                         "west": {
#                             "texture": "#west",
#                             "cullface": "west"
#                         },
#                         "east": {
#                             "texture": "#east",
#                             "cullface": "east"
#                         }
#                     }
#                 }
#             ]
#         },


# element 裡面的 from , to 是指一個block的3維空間的座標


class Enity:
    def __init__(self, x:float, y:float, z:float, blockdata:dict,texturepath:str) -> None:
        self.blockdata = blockdata
        self.name = blockdata["Name"].replace("minecraft:", "")
        self.x = x
        self.y = y
        self.z = z
        self.center = [sum([x, x + 0.1]) / 2, sum([y, y + 0.1]) / 2, sum([z, z + 0.1]) / 2]
        self.thisdata = None
        self.textures = {}
        self.enitys = []
        self.rotatemode = []
        self.rotate = []
        self.element = None
        self.objdata = {"blockname": self.name, "v": [], "vt": [], "f": [], "textures": []}
        self.texturepath = os.path.join(texturepath, "output.json")
        self.parse()
        self.merge()

    def merge(self) -> None:
        # f要替換為全部v轉換的index
        for i in self.enitys:
            self.objdata["v"].extend(i.objdata["v"])

        for i in self.enitys:
            for j in i.objdata["f"]:
                temp = []
                for x in range(len(j)):
                    temp.append(self.objdata["v"].index(i.objdata["v"][j[x] - 1]) + 1)
                self.objdata["f"].append(temp)
            self.objdata["vt"].extend(i.objdata["vt"])
            self.objdata["textures"].extend(i.objdata["textures"])

    def parse(self) -> None:
        with open(
            self.texturepath,
            "r",
            encoding="utf8",
        ) as f:
            self.thisdata = json.load(f)[self.name]
        if "variants" in self.thisdata:
            for i in self.thisdata["variants"]:
                if i != "":
                    flag = False
                    values = i.split(",")
                    for value in values:
                        value = value.split("=")
                        if value[0] in self.blockdata["Properties"]:
                            if value[1] == self.blockdata["Properties"][value[0]]:
                                flag = True
                            else:
                                flag = False
                                break
                    if flag:
                        if "x" in self.thisdata["variants"][i]:
                            self.rotatemode.append("x")
                            self.rotate.append(self.thisdata["variants"][i]["x"])
                        if "y" in self.thisdata["variants"][i]:
                            self.rotatemode.append("y")
                            self.rotate.append(self.thisdata["variants"][i]["y"])
                        self.load_model(self.thisdata["variants"][i]["model"])
                else:
                    self.load_model(self.thisdata["variants"][i]["model"])
        elif "multipart" in self.thisdata:
            code = 0
            for i in self.thisdata["multipart"]:
                if "when" in i:
                    if "OR" in i["when"]:
                        flag = False
                        for j in i["when"]["OR"]:
                            flag2 = False
                            for x in j.keys():
                                if "|" in j[x]:
                                    if self.blockdata["Properties"][x] in j[x].split("|"):
                                        flag2 = True
                                    else:
                                        flag2 = False
                                        break
                                else:
                                    if self.blockdata["Properties"][x] == j[x]:
                                        flag2 = True
                                    else:
                                        flag2 = False
                                        break
                            if flag2:
                                flag = True
                        if flag:
                            if "x" in i["apply"]:
                                self.rotatemode.append({"code": code, "mode": "x"})
                                self.rotate.append(i["apply"]["x"])
                            if "y" in i["apply"]:
                                self.rotatemode.append({"code": code, "mode": "y"})
                                self.rotate.append(i["apply"]["y"])
                            self.load_model(i["apply"]["model"].split("/")[-1], code)
                    else:
                        if (
                            self.blockdata["Properties"][list(i["when"].keys())[0]]
                            in list(i["when"].values())[0].split("|")
                            if "|" in list(i["when"].values())[0]
                            else self.blockdata["Properties"][list(i["when"].keys())[0]]
                            == list(i["when"].values())[0]
                        ):
                            if "x" in i["apply"]:
                                self.rotatemode.append({"code": code, "mode": "x"})
                                self.rotate.append(i["apply"]["x"])
                            if "y" in i["apply"]:
                                self.rotatemode.append({"code": code, "mode": "y"})
                                self.rotate.append(i["apply"]["y"])
                            self.load_model(i["apply"]["model"].split("/")[-1], code)
                else:
                    self.load_model(i["apply"]["model"].split("/")[-1], code)
                code += 1

    def load_model(self, modelname:str, code=None,isparent=False) -> None:
        with open(
            self.texturepath,
            "r",
            encoding="utf8",
        ) as f:
            model = json.load(f)["models"][modelname]
            if "parent" in model:
                self.load_model(model["parent"].split("/")[-1], code,True)
            # if isparent:
            #     self.parents[modelname] = model
            if "textures" in model:
                self.textures.update(model["textures"])
            if "elements" in model:
                self.element = model["elements"]

        if not isparent:
            self.enitys.append(Build_enity(self, code,self.element))


class Build_enity:
    def __init__(self, mother: Enity, code:str,elements:List[dict]) -> None:
        self.name = code
        self.x = mother.x
        self.y = mother.y
        self.z = mother.z
        self.center = [
            sum([self.x, self.x + 0.1]) / 2,
            sum([self.y, self.y + 0.1]) / 2,
            sum([self.z, self.z + 0.1]) / 2,
        ]
        self.parents = {}
        self.textures = mother.textures
        self.element = elements
        self.objdata = {"v": [], "vt": [], "f": [], "textures": []}
        self.rotatemode = mother.rotatemode
        self.rotate = mother.rotate
        self.start()

    def start(self):
        for i in self.element:
            self.build_element(i)
        alrrote = []

        for i in range(len(self.rotatemode)):
            if isinstance(self.rotatemode[i],dict):
                if self.rotatemode[i]["mode"] == "y" and self.rotatemode[i] not in alrrote and self.rotatemode[i]["code"] == self.name:
                    alrrote.append(self.rotatemode[i])
                    for j in range(len(self.objdata["v"])):
                        self.objdata["v"][j] = self.rotate_y(
                            self.objdata["v"][j], self.rotate[i], self.center
                        )
                elif self.rotatemode[i]["mode"] == "x" and self.rotatemode[i] not in alrrote and self.rotatemode[i]["code"] == self.name:
                    alrrote.append(self.rotatemode[i])
                    for j in range(len(self.objdata["v"])):
                        self.objdata["v"][j] = self.rotate_x(
                            self.objdata["v"][j], self.rotate[i], self.center
                        )
            else:
                if self.rotatemode[i] == "y" and self.rotatemode[i] not in alrrote:
                    alrrote.append(self.rotatemode[i])
                    for j in range(len(self.objdata["v"])):
                        self.objdata["v"][j] = self.rotate_y(
                            self.objdata["v"][j], self.rotate[i], self.center
                        )
                elif self.rotatemode[i] == "x" and self.rotatemode[i] not in alrrote:
                    alrrote.append(self.rotatemode[i])
                    for j in range(len(self.objdata["v"])):
                        self.objdata["v"][j] = self.rotate_x(
                            self.objdata["v"][j], self.rotate[i], self.center
                        )

    def append_pos(self, thelist, item):
        """
        append 到 list並回傳index
        """
        if item not in thelist:
            thelist.append(item)
            return len(thelist)
        else:
            return thelist.index(item) + 1

    def add_texture(self, texturename):
        if texturename in self.textures:
            if "#" in self.textures[texturename]:
                temp = self.textures[texturename]
                temp = temp.replace("#", "")
                self.add_texture(temp)
            else:
                self.objdata["textures"].append(self.textures[texturename])
                return

    def add_F(self, listV:List[float], rotate:int=0, elerotate:Callable[[List[float]],List[float]]=None) -> None:
        f = []
        if rotate == 90:
            listV = [listV[3], listV[0], listV[1], listV[2]]
        if rotate == 180:
            listV = [listV[2], listV[3], listV[0], listV[1]]
        elif rotate == 270:
            listV = [listV[1], listV[2], listV[3], listV[0]]
        if elerotate != None:
            for i in range(len(listV)):
                listV[i] = elerotate(listV[i])
        for i in listV:
            f.append(self.append_pos(self.objdata["v"], i))
        self.objdata["f"].append(f)

    def build_element(self, element:dict) -> None:
        # 一個方塊 = 1*1*1
        # 數據給的方塊 = 16*16*16
        # 轉換為 1*1*1
        pos1 = element["from"]
        pos2 = element["to"]

        elerotate = None



        if "rotation" in element:
            center = []
            if element["rotation"]["angle"] > 0:
                element["rotation"]["angle"] = -element["rotation"]["angle"]
            else:
                element["rotation"]["angle"] = abs(element["rotation"]["angle"])
            if "origin" in element["rotation"]:
                center = [
                    element["rotation"]["origin"][i] / (16 * 10) + [self.x, self.y, self.z][i]
                    for i in range(3)
                ]
            if element["rotation"]["axis"] == "y":
                elerotate = lambda x: self.rotate_y(  # noqa: E731
                    x, element["rotation"]["angle"], center if center != [] else self.center
                )
            elif element["rotation"]["axis"] == "x":
                elerotate = lambda x: self.rotate_x(  # noqa: E731
                    x, element["rotation"]["angle"], center if center != [] else self.center
                )
            if "rescale" in element["rotation"] and element["rotation"]["rescale"] and "rail" in self.textures:
                pos1 = [0,9,-3]
                pos2 = [16,9,19]

        for i in range(3):
            pos1[i] /= 16 * 10
            pos2[i] /= 16 * 10



        # 六個面 = down up north south west east
        for i in element["faces"]:
            if "rotation" in element["faces"][i]:
                rotate = element["faces"][i]["rotation"]
            else:
                rotate = 0
            if i == "up":
                self.add_F(
                    [
                        [pos1[0] + self.x, pos2[1] + self.y, pos2[2] + self.z],
                        [pos2[0] + self.x, pos2[1] + self.y, pos2[2] + self.z],
                        [pos2[0] + self.x, pos2[1] + self.y, pos1[2] + self.z],
                        [pos1[0] + self.x, pos2[1] + self.y, pos1[2] + self.z],
                    ],
                    rotate,
                    elerotate,
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#", ""))
                else:
                    self.add_texture(i)
                self.add_vt(element["faces"][i])
            elif i == "down":
                self.add_F(
                    [
                        [pos1[0] + self.x, pos1[1] + self.y, pos1[2] + self.z],
                        [pos2[0] + self.x, pos1[1] + self.y, pos1[2] + self.z],
                        [pos2[0] + self.x, pos1[1] + self.y, pos2[2] + self.z],
                        [pos1[0] + self.x, pos1[1] + self.y, pos2[2] + self.z],
                    ],
                    rotate,
                    elerotate,
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#", ""))
                else:
                    self.add_texture(i)
                self.add_vt(element["faces"][i])
            elif i == "north":
                self.add_F(
                    [
                        [pos2[0] + self.x, pos1[1] + self.y, pos1[2] + self.z],
                        [pos1[0] + self.x, pos1[1] + self.y, pos1[2] + self.z],
                        [pos1[0] + self.x, pos2[1] + self.y, pos1[2] + self.z],
                        [pos2[0] + self.x, pos2[1] + self.y, pos1[2] + self.z],
                    ],
                    rotate,
                    elerotate,
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#", ""))
                else:
                    self.add_texture(i)
                self.add_vt(element["faces"][i])
            elif i == "south":
                self.add_F(
                    [
                        [pos1[0] + self.x, pos1[1] + self.y, pos2[2] + self.z],
                        [pos2[0] + self.x, pos1[1] + self.y, pos2[2] + self.z],
                        [pos2[0] + self.x, pos2[1] + self.y, pos2[2] + self.z],
                        [pos1[0] + self.x, pos2[1] + self.y, pos2[2] + self.z],
                    ],
                    rotate,
                    elerotate,
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#", ""))
                else:
                    self.add_texture(i)
                self.add_vt(element["faces"][i])
            elif i == "west":
                self.add_F(
                    [
                        [pos1[0] + self.x, pos1[1] + self.y, pos1[2] + self.z],
                        [pos1[0] + self.x, pos1[1] + self.y, pos2[2] + self.z],
                        [pos1[0] + self.x, pos2[1] + self.y, pos2[2] + self.z],
                        [pos1[0] + self.x, pos2[1] + self.y, pos1[2] + self.z],
                    ],
                    rotate,
                    elerotate,
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#", ""))
                else:
                    self.add_texture(i)
                self.add_vt(element["faces"][i])
            elif i == "east":
                self.add_F(
                    [
                        [pos2[0] + self.x, pos1[1] + self.y, pos2[2] + self.z],
                        [pos2[0] + self.x, pos1[1] + self.y, pos1[2] + self.z],
                        [pos2[0] + self.x, pos2[1] + self.y, pos1[2] + self.z],
                        [pos2[0] + self.x, pos2[1] + self.y, pos2[2] + self.z],
                    ],
                    rotate,
                    elerotate,
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#", ""))
                else:
                    self.add_texture(i)
                self.add_vt(element["faces"][i])

    def rotate_y(self, point:List[float], angle:Union[int,float], center:List[float]):
        angle = math.radians(angle)
        x = point[0] - center[0]
        z = point[2] - center[2]
        point[0] = x * math.cos(angle) - z * math.sin(angle) + center[0]
        point[2] = x * math.sin(angle) + z * math.cos(angle) + center[2]
        return point

    def rotate_x(self, point:List[float], angle:Union[int,float], center:List[float]):
        angle = math.radians(angle)
        y = point[1] - center[1]
        z = point[2] - center[2]
        point[1] = y * math.cos(angle) + z * math.sin(angle) + center[1]
        point[2] = -y * math.sin(angle) + z * math.cos(angle) + center[2]
        return point

    def add_vt(self, face:dict) -> None:
        if "uv" in face:
            self.objdata["vt"].append(
                [
                    [
                        face["uv"][0] / 16 if face["uv"][0] != 0 else 0,
                        face["uv"][1] / 16 if face["uv"][1] != 0 else 0,
                    ],
                    [
                        face["uv"][2] / 16 if face["uv"][2] != 0 else 0,
                        face["uv"][1] / 16 if face["uv"][1] != 0 else 0,
                    ],
                    [
                        face["uv"][2] / 16 if face["uv"][2] != 0 else 0,
                        face["uv"][3] / 16 if face["uv"][3] != 0 else 0,
                    ],
                    [
                        face["uv"][0] / 16 if face["uv"][0] != 0 else 0,
                        face["uv"][3] / 16 if face["uv"][3] != 0 else 0,
                    ],
                ]
            )
        else:
            self.objdata["vt"].append(
                [
                    [0, 0],
                    [1, 0],
                    [1, 1],
                    [0, 1],
                ]
            )


if __name__ == "__main__":
    # Enity(0, 0, 0, {"Name": "minecraft:redstone_block"}).start()
    print(Build_enity.rotate_y(..., [10, 0, 2], 180, [5, 5, 5]))
