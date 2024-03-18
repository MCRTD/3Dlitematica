import gzip
import io


def BigEndiannessForInt(source: bytes, index: int) -> int:
    return (
        (source[index] << 24)
        + (source[index + 1] << 16)
        + (source[index + 2] << 8)
        + source[index + 3]
    )


def BigEndiannessForLong(source: bytes, index: int) -> int:
    return (BigEndiannessForInt(source, index) << 32) + BigEndiannessForInt(source, index + 4)


def SmallEndiannessForInt(source: bytes, index: int) -> int:
    return (
        source[index]
        + (source[index + 1] << 8)
        + (source[index + 2] << 16)
        + (source[index + 3] << 24)
    )


def GZipUnzip(source:bytes) -> bytes:
    return gzip.GzipFile(fileobj=io.BytesIO(source)).read()
