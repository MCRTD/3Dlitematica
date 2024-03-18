from typing import List, Any
class bitstack:
    def __init__(self, bytelong:int, Resolve_data: List[Any]) -> None:
        self.bites = ""
        long = 1
        while bytelong > 2**long:
            long += 1
        self.bytelong = long
        self.Resolve_data = Resolve_data

    def add(self, bite: int) -> None:
        bite = int(bite)
        bite = bin(bite & 0xFFFFFFFFFFFFFFFF)[2:].zfill(64)
        bite = [j for j in [bite[i : i + 8] for i in range(0, len(bite), 8)][::-1]]
        bite = "".join(bite)
        self.bites += bite[::-1]

    def get(self, length: int) -> str:
        bite = self.bites[:length]
        self.bites = self.bites[length:]
        return bite

    def calc(self) -> List[Any]:
        stepbytes = self.bites
        stepbytes = [
            stepbytes[i : i + self.bytelong][::-1] for i in range(0, len(self.bites), self.bytelong)
        ]  # self.bytelong位一組
        stepbytes = stepbytes[::-1]
        stepbytes = [int(i, 2) for i in stepbytes]  # 二進位轉十進位
        decode_BlockStates = []
        for z in stepbytes:
            decode_BlockStates.append(self.Resolve_data[z])
        return decode_BlockStates
