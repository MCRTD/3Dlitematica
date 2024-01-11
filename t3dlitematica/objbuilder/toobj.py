import json
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
                            self.addEnity(Enity(i,j,k,data[count]))
                        except:
                            self.addblock(i,j,k,data[count]["Name"])
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
                [x+1,y,z],
                [x+1,y,z+1],
                [x,y,z+1],
                [x,y+1,z],
                [x+1,y+1,z],
                [x+1,y+1,z+1],
                [x,y+1,z+1]
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
        _v = ""
        _vt = ""
        _f = ""
        # load texture and generate mtl file
        temp = ""
        for i in self.tmpdata:
            if "textures" in self.tmpdata[i]:
                for j in set(self.tmpdata[i]["textures"]):
                    if j not in self.textures:
                        self.textures.append(j)
                        temp += "newmtl "+j.split("/")[-1]+"\n"
                        temp += "Ka 1.000 1.000 1.000\n"
                        temp += os.path.join("temp","textures",j,".png")+"\n"
                        temp += "\n"
        with open(self.name+".mtl","w") as f:
            f.write(temp)

        for blocks in self.tmpdata:
            for v in self.tmpdata[blocks]["v"]:
                if self.vtof.get((v[0],v[1],v[2])) == None:
                    _v += "v "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n"
                    self.vtof[(v[0],v[1],v[2])] = len(self.vtof)+1
            # for vt in self.tmpdata[blocks]["vt"]:
            #     _vt += "vt "+str(vt[0])+" "+str(vt[1])+"\n"
            for f in self.tmpdata[blocks]["f"]:
                if "textures" in self.tmpdata[blocks]:
                    _f += "usemtl "+self.tmpdata[blocks]["textures"][0].split("/")[-1]+"\n"
                _f += "f "
                for i in f:
                    _f += str(self.vtof[(self.tmpdata[blocks]["v"][i-1][0],self.tmpdata[blocks]["v"][i-1][1],self.tmpdata[blocks]["v"][i-1][2])])+" "
                _f += "\n"
            _f += "#DEBUG \n"
        pprint(self.vtof)
        self.output += "mtllib "+self.name+".mtl"+"\n"
        self.output += _v+_vt+_f
        self.objfile.write(self.output)


if __name__ == "__main__":
    with open("./test.json", "r",encoding="utf8") as f:
        data = json.load(f)
    size = (int(data["Regions"][" 1"]["Size"]["x"]),int(data["Regions"][" 1"]["Size"]["y"]),int(data["Regions"][" 1"]["Size"]["z"]))
    data = data["Regions"][" 1"]["decode_BlockStates"]
    objhandel("test",data,size)