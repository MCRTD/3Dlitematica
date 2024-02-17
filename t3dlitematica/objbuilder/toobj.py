import json
import sys
import traceback
from mctoobj import Enity
from pprint import pprint
import os
class objhandel:

    def __init__(self,name,data,size) -> None:
        self.name = name
        self.objfile = open(name+".obj","w")
        self.output = "# generate by 3dlitematica"+"\n"+"g "+name+"\n"
        self.tmpdata = {}
        self.vtof = {} # 對應表
        self.vtovt = {}
        self.textures = []
        self.main(data,size)

    def main(self,data,size):
        data = list(reversed(data))
        x = size[0]
        y = size[1]
        z = size[2]
        count = 0
        for j in range(1,y+1):
            for k in range(1,z+1):
                for i in range(1,x+1):
                    if data[count]["Name"] == "minecraft:air":
                        pass
                    else:
                        try:
                            self.addEnity(Enity(i/10,j/10,k/10,data[count]))
                        except Exception as e:
                            error_class = e.__class__.__name__
                            detail = e.args[0]
                            cl, exc, tb = sys.exc_info()
                            lastCallStack = traceback.extract_tb(tb)[-1]
                            fileName = lastCallStack[0]
                            lineNum = lastCallStack[1]
                            funcName = lastCallStack[2]
                            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
                            print(f"[UserData] | {errMsg}")
                            self.addblock(i/10,j/10,k/10,data[count]["Name"])
                            print(e)
                    print(count)
                    count += 1


        # self.objfile.write(self.output)
        self.writeobj()
        self.objfile.close()
        print(self.tmpdata)

    """
    # List of geometric vertices, with (x, y, z, [w]) coordinates, w is optional and defaults to 1.0.
    v 0.123 0.234 0.345 1.0
    v ...

    # List of texture coordinates, in (u, [v, w]) coordinates, these will vary between 0 and 1. v, w are optional and default to 0.
    vt 0.500 1 [0]
    vt ...

    # Polygonal face element
    f 1 2 3
    f 3/1 4/2 5/3
    f 6/4/1 3/5/3 7/6/5
    f 7//1 8//2 9//3
    f ...
    """

    def addEnity(self,Enity:Enity):
        if Enity.objdata["v"] == []:
            raise Exception("Enity.objdata[\"v\"] is empty")
        self.tmpdata[(Enity.x,Enity.y,Enity.z)] = Enity.objdata


    def addblock(self,x,y,z,blockname):
        self.tmpdata[(x,y,z)] = {
            "blockname":blockname,
            "v":[
                [x,y,z],
                [x+0.1,y,z],
                [x+0.1,y,z+0.1],
                [x,y,z+0.1],
                [x,y+0.1,z],
                [x+0.1,y+0.1,z],
                [x+0.1,y+0.1,z+0.1],
                [x,y+0.1,z+0.1]
            ],
            "vt":[
                [0,0],
                [1,0],
                [1,1],
                [0,1]
            ],
            "f":[
                [1,2,3,4],
                [8,7,6,5],
                [5,6,2,1],
                [6,7,3,2],
                [7,8,4,3],
                [8,5,1,4]
            ]
        }

    def writeobj(self):
        # TODO: 將方塊加入到group裡面
        # https://blog.csdn.net/xyh930929/article/details/82260581
        # 格式 ：f v/vt/vn v/vt/vn v/vt/vn（f 顶点索引 / 纹理坐标索引 / 顶点法向量索引）
        temp = ""
        for i in self.tmpdata:
            if "textures" in self.tmpdata[i]:
                for j in set(self.tmpdata[i]["textures"]):
                    if j not in self.textures:
                        self.textures.append(j)
                        temp += "newmtl "+j.split("/")[-1]+"\n"
                        temp += "Ka 1.000 1.000 1.000\n"
                        temp += "map_Kd "+os.path.join("temp","textures",j+".png")+"\n"
                        temp += "\n"
        temp += "newmtl "+"missing"+"\n"
        temp += "Ka 1.000 1.000 1.000\n"
        temp += "map_Kd "+os.path.join("resource","Minecraft_missing_texture_block.svg.png")+"\n"
        temp += "\n"
        with open(self.name+".mtl","w") as f:
            f.write(temp)

        oneblock = ""
        for blocks in self.tmpdata:
            for v in self.tmpdata[blocks]["v"]:
                if self.vtof.get((v[0],v[1],v[2])) == None:
                    oneblock += "v "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n"
                    self.vtof[(v[0],v[1],v[2])] = len(self.vtof)+1
            for vt in self.tmpdata[blocks]["vt"]:
                if self.vtovt.get((vt[0],vt[1])) == None:
                    self.vtovt[(vt[0],vt[1])] = len(self.vtovt)+1
                    oneblock += "vt "+str(vt[0])+" "+str(vt[1])+"\n"
            ct1 = 0
            for f in self.tmpdata[blocks]["f"]:
                if "textures" in self.tmpdata[blocks]:
                    try:
                        oneblock += "usemtl "+self.tmpdata[blocks]["textures"][ct1].split("/")[-1]+"\n"
                    except:
                        oneblock += "usemtl "+"missing"+"\n"
                else:
                    oneblock += "usemtl "+"missing"+"\n"
                oneblock += "f "
                ct = 0
                for i in f:
                    oneblock += str(self.vtof[(self.tmpdata[blocks]["v"][i-1][0],self.tmpdata[blocks]["v"][i-1][1],self.tmpdata[blocks]["v"][i-1][2])])+ \
                        "/"+str(self.vtovt[(self.tmpdata[blocks]["vt"][ct][0],self.tmpdata[blocks]["vt"][ct][1])])+" "
                    ct += 1
                oneblock += "\n"
                ct1 += 1
            oneblock += "#DEBUG \n"
        # pprint(self.vtof)
        self.output += "mtllib "+self.name+".mtl"+"\n"
        self.output += oneblock
        self.objfile.write(self.output)


if __name__ == "__main__":
    with open("./test.json", "r",encoding="utf8") as f:
        data = json.load(f)
    size = (int(data["Regions"]["Unnamed"]["Size"]["x"]),int(data["Regions"]["Unnamed"]["Size"]["y"]),int(data["Regions"]["Unnamed"]["Size"]["z"]))
    data = data["Regions"]["Unnamed"]["decode_BlockStates"]
    objhandel("test",data,size)