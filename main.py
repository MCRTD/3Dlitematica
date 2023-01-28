from t3dlitematica.litematicadecoder import Resolve
import json
data = Resolve(r"C:\Users\phill\Desktop\codes\3Dlitematica\8020sc.litematic")
with open("./test.json", "w",encoding="utf8") as f:
    json.dump(data, f, indent=4)
print(data)