import json
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

    def __init__(self, x,y,z,blockdata):
        self.blockdata = blockdata
        self.name = blockdata["Name"].replace("minecraft:","")
        self.x = x
        self.y = y
        self.z = z
        self.parents = {}
        self.thisdata = None
        self.textures = {}
        self.element = {}
        self.objdata = {
            "blockname": self.name,
            "v": [],
            "vt": [],
            "f": [],
            "textures": []
        }
        self.start()
    def __getstate__(self):
            return "custom debug info: exponent is " + self.parents

    def start(self):
        with open(r"C:\Users\phill\Documents\code\3Dlitematica\temp\output.json","r",encoding="utf8") as f:
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
                        self.load_model(self.thisdata["variants"][i]["model"])
                else:
                    self.load_model(self.thisdata["variants"][i]["model"])
        elif "multipart" in self.thisdata:
            ...
        for i in self.element:
            self.build_element(i)
        print("-"*50)
        if self.objdata['blockname'] == "sticky_piston":
            pprint(self.objdata)
            pprint(self.textures)

    def load_model(self,modelname,isparent=False):
        with open(r"C:\Users\phill\Documents\code\3Dlitematica\temp\output.json","r",encoding="utf8") as f:
            model = json.load(f)["models"][modelname]
            if "parent" in model:
                self.load_model(model["parent"].split("/")[-1],True)
            if isparent:
                self.parents[modelname] = model
            if "textures" in model:
                self.textures.update(model["textures"])
            if "elements" in model:
                self.element = model["elements"]

    def append_pos(self,thelist,item):
        """
        append 到 list並回傳index
        """
        if item not in thelist:
            thelist.append(item)
            return len(thelist)
        else:
            return thelist.index(item)+1

    def add_texture(self,texturename):
        print(texturename)
        if texturename in self.textures:
            if "#" in self.textures[texturename]:
                temp = self.textures[texturename]
                temp = temp.replace("#","")
                print(temp)
                self.add_texture(temp)
            else:
                self.objdata["textures"].append(self.textures[texturename])
                return


    def add_F(self,listV,rotate=0):
        f = []
        if rotate == 90:
            listV = [listV[3],listV[0],listV[1],listV[2]]
        if rotate == 180:
            listV = [listV[2],listV[3],listV[0],listV[1]]
        elif rotate == 270:
            listV = [listV[1],listV[2],listV[3],listV[0]]
        for i in listV:
            f.append(self.append_pos(self.objdata["v"],i))
        self.objdata["f"].append(f)


    def build_element(self,element):
        # 一個方塊 = 1*1*1
        # 數據給的方塊 = 16*16*16
        # 轉換為 1*1*1
        pos1 = element["from"]
        pos2 = element["to"]

        for i in range(3):
            pos1[i] /= (16*10)
            pos2[i] /= (16*10)

        # 六個面 = down up north south west east
        for i in element["faces"]:
            if "rotation" in element["faces"][i]:
                rotate = element["faces"][i]["rotation"]
            else:
                rotate = 0
            if i == "up":
                self.add_F(
                    [
                        [pos1[0]+self.x,pos2[1]+self.y,pos1[2]+self.z],
                        [pos2[0]+self.x,pos2[1]+self.y,pos1[2]+self.z],
                        [pos2[0]+self.x,pos2[1]+self.y,pos2[2]+self.z],
                        [pos1[0]+self.x,pos2[1]+self.y,pos2[2]+self.z]
                    ],
                    rotate
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#",""))
                else:
                    self.add_texture(i)
            elif i == "down":
                self.add_F(
                    [
                        [pos1[0]+self.x,pos1[1]+self.y,pos1[2]+self.z],
                        [pos2[0]+self.x,pos1[1]+self.y,pos1[2]+self.z],
                        [pos2[0]+self.x,pos1[1]+self.y,pos2[2]+self.z],
                        [pos1[0]+self.x,pos1[1]+self.y,pos2[2]+self.z]
                    ],
                    rotate
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#",""))
                else:
                    self.add_texture(i)
            elif i == "north":
                self.add_F(
                    [
                        [pos1[0]+self.x,pos1[1]+self.y,pos1[2]+self.z],
                        [pos2[0]+self.x,pos1[1]+self.y,pos1[2]+self.z],
                        [pos2[0]+self.x,pos2[1]+self.y,pos1[2]+self.z],
                        [pos1[0]+self.x,pos2[1]+self.y,pos1[2]+self.z]
                    ],
                    rotate
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#",""))
                else:
                    self.add_texture(i)
            elif i == "south":
                self.add_F(
                    [
                        [pos1[0]+self.x,pos1[1]+self.y,pos2[2]+self.z],
                        [pos2[0]+self.x,pos1[1]+self.y,pos2[2]+self.z],
                        [pos2[0]+self.x,pos2[1]+self.y,pos2[2]+self.z],
                        [pos1[0]+self.x,pos2[1]+self.y,pos2[2]+self.z]
                    ],
                    rotate
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#",""))
                else:
                    self.add_texture(i)
            elif i == "west":
                self.add_F(
                    [
                        [pos1[0]+self.x,pos1[1]+self.y,pos1[2]+self.z],
                        [pos1[0]+self.x,pos1[1]+self.y,pos2[2]+self.z],
                        [pos1[0]+self.x,pos2[1]+self.y,pos2[2]+self.z],
                        [pos1[0]+self.x,pos2[1]+self.y,pos1[2]+self.z]
                    ],
                    rotate
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#",""))
                else:
                    self.add_texture(i)
            elif i == "east":
                self.add_F(
                    [
                        [pos2[0]+self.x,pos1[1]+self.y,pos1[2]+self.z],
                        [pos2[0]+self.x,pos1[1]+self.y,pos2[2]+self.z],
                        [pos2[0]+self.x,pos2[1]+self.y,pos2[2]+self.z],
                        [pos2[0]+self.x,pos2[1]+self.y,pos1[2]+self.z]
                    ],
                    rotate
                )
                if "texture" in element["faces"][i]:
                    self.add_texture(element["faces"][i]["texture"].replace("#",""))
                else:
                    self.add_texture(i)
        self.objdata["vt"].append([0,0])
        self.objdata["vt"].append([1,0])
        self.objdata["vt"].append([1,1])
        self.objdata["vt"].append([0,1])





if __name__ == "__main__":
    Enity(0,0,0,{"Name":"minecraft:redstone_block"}).start()