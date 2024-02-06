import json
import os
import shutil

class convert_texturepack:

    def __init__(self, path: str , output: str):
        self.path = path
        self.mainpath = os.path.join(path, "assets", "minecraft")
        self.output = output
        self.noneedfind = ["armor_trims","mob_effects","shield_patterns","particles"]
        self.blocksdata = {"models":{}}
        self.start()


    def start(self):
        sources = []
        for i in os.listdir(os.path.join(self.mainpath, "atlases")):
            if i.split(".")[0] in self.noneedfind:
                continue
            with open(os.path.join(self.mainpath, "atlases", i), "r", encoding="utf8") as f:
                blocksdata = json.load(f)
            for j in blocksdata["sources"]:
                if j["type"] == "paletted_permutations":
                    continue
                sources.append(j)
        needcopy = set()
        for i in sources:
            if i['type'] == "directory":
                needcopy.add(i["source"].split("/")[0])
            elif i['type'] == "single":
                needcopy.add(i["resource"].split("/")[0])

        def load_model(path):
            with open(os.path.join(self.mainpath, "models", path), "r", encoding="utf8") as f:
                blockmodel = f.read()
                tempload = json.loads(blockmodel)
            blockmodel = blockmodel.replace("minecraft:", "")
            blockmodel = json.loads(blockmodel)
            if "parent" in blockmodel and blockmodel["parent"]  not in self.blocksdata["models"]:
                load_model(tempload["parent"].split(":")[-1]+".json")
            if path not in self.blocksdata["models"]:
                self.blocksdata["models"][path.split("/")[-1].split(".")[0]] = blockmodel

        for i in os.listdir(os.path.join(self.mainpath, "blockstates")):
            with open(os.path.join(self.mainpath, "blockstates", i), "r", encoding="utf8") as f:
                blockstates = json.load(f)
            if "variants" in blockstates:
                for variants in blockstates["variants"]:
                    if (type(blockstates["variants"][variants]) == dict):
                        load_model(blockstates["variants"][variants]["model"].split(":")[-1]+".json")
                        blockstates["variants"][variants]["model"] = blockstates["variants"][variants]["model"].split("/")[-1]
                    elif (type(blockstates["variants"][variants]) == list):
                        for j in blockstates["variants"][variants]:
                            load_model(j["model"].split(":")[-1]+".json")
                            j["model"] = j["model"].split("/")[-1]

            self.blocksdata[i.split(".")[0]] = blockstates

        with open(self.output+"\output.json", "w", encoding="utf8") as f:
            json.dump(self.blocksdata, f, indent=4, ensure_ascii=False)

        if os.path.exists(os.path.join(self.output,"textures")):
            shutil.rmtree(os.path.join(self.output,"textures"))
        for i in needcopy:
            shutil.copytree(os.path.join(self.mainpath, "textures", i), os.path.join(self.output, "textures", i))





if __name__ == "__main__":
    convert_texturepack(r"C:\Users\phill\Downloads\VanillaDefault 1.20.4", r"C:\Users\phill\Documents\code\3Dlitematica\temp")