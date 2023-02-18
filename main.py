from t3dlitematica.litematicadecoder import Resolve
import json
# data = Resolve(r"C:\Users\0\Documents\coed_thing\3Dlitematica\20gt.litematic")
data = Resolve(r"C:\Users\phill\Desktop\codes\3Dlitematica\1.litematic")
with open("./test.json", "w",encoding="utf8") as f:
    json.dump(data, f, indent=4)
print(data)


