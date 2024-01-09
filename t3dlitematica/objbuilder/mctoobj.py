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

    def __init__(self, x,y,z,name):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.parent = None
        self.objdata = {
            "blockname": self.name,
            "v": [],
            "vt": [],
            "f": []
        }

    def convert_to_obj():
        ...