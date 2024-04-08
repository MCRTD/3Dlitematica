from pathlib import Path
import json
import tempfile
import shutil
from typing import List

class multiload:

    def __init__(self, texturepacks: List[str]) -> None:
        """
        texturepacks: ./redstone,./beautiful,./default

        最先使用 | 第二 | 最後

        text1 -> text2 -> text3
        """
        self.texturepacks = texturepacks
        self.tempfolder = None

    def __enter__(self):
        with open(Path(self.texturepacks[-1],"output.json"), "r", encoding="utf8") as f:
            finaloutput = json.load(f)
        temp = self.texturepacks.pop()
        if not self.texturepacks:
            return temp
        self.tempfolder = tempfile.mkdtemp()
        shutil.copytree(Path(temp,"textures"), Path(self.tempfolder,"textures"))
        for texturepack in self.texturepacks.reverse():
            with open(Path(texturepack,"output.json"), "r", encoding="utf8") as f:
                texturedata = json.load(f)
            # merge
            for models in texturedata["models"]:
                finaloutput["models"][models] = texturedata["models"][models]
            for blockstates in texturedata:
                if blockstates == "models":
                    continue
                finaloutput[blockstates] = texturedata[blockstates]

            shutil.copytree(Path(texturepack,"textures"), Path(self.tempfolder,"textures"))
        with open(Path(self.tempfolder,"output.json"), "w", encoding="utf8") as f:
            json.dump(finaloutput, f, indent=4, ensure_ascii=False)

        return self.tempfolder

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tempfolder:
            shutil.rmtree(self.tempfolder)


