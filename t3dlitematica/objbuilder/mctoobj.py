import json
import math
from pprint import pprint
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
    def __init__(self, x, y, z, blockdata):
        self.blockdata = blockdata
        self.name = blockdata["Name"].replace("minecraft:", "")
        self.x = x
        self.y = y
        self.z = z
        self.center = [sum([x, x + 0.1]) / 2, sum([y, y + 0.1]) / 2, sum([z, z + 0.1]) / 2]
        self.thisdata = None
        self.textures = {}
        self.enitys = []
        self.rotatemode = None
        self.rotate = 0
        self.element = None
        self.objdata = {"blockname": self.name, "v": [], "vt": [], "f": [], "textures": []}
        self.parse()
        self.merge()

    def merge(self):
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

    def parse(self):
        with open(
            r"C:\Users\phill\OneDrive\Documents\coed_thing\3Dlitematica\temp\output.json",
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
                        if "y" in self.thisdata["variants"][i]:
                            self.rotatemode = "y"
                            self.rotate = self.thisdata["variants"][i]["y"]
                        elif "x" in self.thisdata["variants"][i]:
                            self.rotatemode = "x"
                            self.rotate = self.thisdata["variants"][i]["x"]
                        self.load_model(self.thisdata["variants"][i]["model"])
                else:
                    self.load_model(self.thisdata["variants"][i]["model"])
        elif "multipart" in self.thisdata:
            for i in self.thisdata["multipart"]:
                if "when" in i:
                    if "OR" in i["when"]:
                        for j in i["when"]["OR"]:
                            if (
                                self.blockdata["Properties"][list(j.keys())[0]]
                                == list(j.values())[0]
                            ):
                                if "y" in i["apply"]:
                                    self.rotatemode = "y"
                                    self.rotate = i["apply"]["y"]
                                elif "x" in i["apply"]:
                                    self.rotatemode = "x"
                                    self.rotate = i["apply"]["x"]
                                self.load_model(i["apply"]["model"].split("/")[-1])
                                break
                    else:
                        if (
                            self.blockdata["Properties"][list(i["when"].keys())[0]]
                            == list(i["when"].values())[0]
                        ):
                            if "y" in i["apply"]:
                                self.rotatemode = "y"
                                self.rotate = i["apply"]["y"]
                            elif "x" in i["apply"]:
                                self.rotatemode = "x"
                                self.rotate = i["apply"]["x"]
                            self.load_model(i["apply"]["model"].split("/")[-1])
                else:
                    self.load_model(i["apply"]["model"].split("/")[-1])

    def load_model(self, modelname, isparent=False):
        with open(
            r"C:\Users\phill\OneDrive\Documents\coed_thing\3Dlitematica\temp\output.json",
            "r",
            encoding="utf8",
        ) as f:
            model = json.load(f)["models"][modelname]
            if "parent" in model:
                self.load_model(model["parent"].split("/")[-1], True)
            # if isparent:
            #     self.parents[modelname] = model
            if "textures" in model:
                self.textures.update(model["textures"])
            if "elements" in model:
                self.element = model["elements"]
        if not isparent:
            self.enitys.append(Build_enity(self, self.element))


class Build_enity:
    def __init__(self, mother: Enity, elements):
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
        if self.rotatemode == "y":
            for i in range(len(self.objdata["v"])):
                self.objdata["v"][i] = self.rotate_y(self.objdata["v"][i], self.rotate, self.center)
        elif self.rotatemode == "x":
            for i in range(len(self.objdata["v"])):
                self.objdata["v"][i] = self.rotate_x(self.objdata["v"][i], self.rotate, self.center)
        print("-" * 50)

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

    def add_F(self, listV, rotate=0):
        f = []
        if rotate == 90:
            listV = [listV[3], listV[0], listV[1], listV[2]]
        if rotate == 180:
            listV = [listV[2], listV[3], listV[0], listV[1]]
        elif rotate == 270:
            listV = [listV[1], listV[2], listV[3], listV[0]]
        for i in listV:
            f.append(self.append_pos(self.objdata["v"], i))
        self.objdata["f"].append(f)

    def build_element(self, element):
        # 一個方塊 = 1*1*1
        # 數據給的方塊 = 16*16*16
        # 轉換為 1*1*1
        pos1 = element["from"]
        pos2 = element["to"]

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
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#", ""))
                else:
                    self.add_texture(i)
                self.add_vt(element["faces"][i])

    def rotate_y(self, point, angle, center):
        angle = math.radians(angle)
        x = point[0] - center[0]
        z = point[2] - center[2]
        point[0] = x * math.cos(angle) - z * math.sin(angle) + center[0]
        point[2] = x * math.sin(angle) + z * math.cos(angle) + center[2]
        return point

    def rotate_x(self, point, angle, center):
        angle = math.radians(angle)
        y = point[1] - center[1]
        z = point[2] - center[2]
        point[1] = y * math.cos(angle) + z * math.sin(angle) + center[1]
        point[2] = -y * math.sin(angle) + z * math.cos(angle) + center[2]
        return point

    def add_vt(self, face):
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
