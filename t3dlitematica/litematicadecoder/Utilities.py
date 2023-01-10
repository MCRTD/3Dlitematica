import gzip
import io
import zipfile


def BigEndiannessForInt(source , index):
    return (source[index] << 24) + (source[index + 1] << 16) + (source[index + 2] << 8) + source[index + 3]



def BigEndiannessForLong(source , index):
    return (BigEndiannessForInt(source , index) << 32) + BigEndiannessForInt(source , index + 4)


def SmallEndiannessForInt(source , index):
    return source[index] + (source[index + 1] << 8) + (source[index + 2] << 16) + (source[index + 3] << 24)


def GZipUnzip(source):
    return gzip.GzipFile(fileobj=io.BytesIO(source)).read()


def ZipUnzip(source):
    return zipfile.ZipFile(io.BytesIO(source)).read()