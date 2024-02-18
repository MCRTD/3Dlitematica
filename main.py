from t3dlitematica import Resolve
import json

# data = Resolve("./randomtest.litematic")
data = Resolve("./final_test.litematic")
with open("./test.json", "w", encoding="utf8") as f:
    json.dump(data, f, indent=4)
# print(data)
