from . import NBTHandler
from . import Utilities


def Resolve(fPath):
    litematic = open(fPath , "rb")
    binSource = Utilities.GZipUnzip(litematic.read())
    return NBTHandler.Resolve(binSource)