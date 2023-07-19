from t3dlitematica.litematicadecoder import Resolve
import json
data = Resolve("./randomtest.litematic")
# data = Resolve("./20gt.litematic")
with open("./test.json", "w",encoding="utf8") as f:
    json.dump(data, f, indent=4)
print(data)


