import litematicadecoder.NBTHandler as NBTHandler
import litematicadecoder.Utilities as Utilities


def Resolve(fPath):
    litematic = open(fPath , "rb")
    binSource = Utilities.GZipUnzip(litematic.read())
    return NBTHandler.Resolve(binSource)