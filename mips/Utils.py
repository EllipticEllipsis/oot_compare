#!/usr/bin/python3

from __future__ import annotations

import csv
import os
import hashlib
import json
import struct
from typing import List, Dict, Tuple
import subprocess
import sys
import shutil

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Returns the md5 hash of a bytearray
def getStrHash(byte_array: bytearray) -> str:
    return str(hashlib.md5(byte_array).hexdigest())

def writeBytearrayToFile(filepath: str, array_of_bytes: bytearray):
    with open(filepath, mode="wb") as f:
       f.write(array_of_bytes)

def readFileAsBytearray(filepath: str) -> bytearray:
    if not os.path.exists(filepath):
        return bytearray(0)
    with open(filepath, mode="rb") as f:
        return bytearray(f.read())

def readFile(filepath: str) -> List[str]:
    with open(filepath) as f:
        return [x.strip() for x in f.readlines()]

def readJson(filepath):
    with open(filepath) as f:
        return json.load(f)

def removeExtraWhitespace(line: str) -> str:
    return" ".join(line.split())

def bytesToBEWords(array_of_bytes: bytearray) -> List[int]:
    words = len(array_of_bytes)//4
    big_endian_format = f">{words}I"
    return list(struct.unpack_from(big_endian_format, array_of_bytes, 0))

def beWordsToBytes(words_list: List[int], buffer: bytearray) -> bytearray:
    words = len(words_list)
    big_endian_format = f">{words}I"
    struct.pack_into(big_endian_format, buffer, 0, *words_list)
    return buffer

def runCommandGetOutput(command: str, args: List[str]) -> List[str] | None:
    try:
        output = subprocess.check_output([command, *args]).decode("utf-8")
        return output.strip().split("\n")
    except:
        return None

def toHex(number: int, digits: int) -> str:
    return "0x" + hex(number)[2:].zfill(digits).upper()

def from2Complement(number: int, bits: int) -> int:
    isNegative = number & (1 << (bits - 1))
    if isNegative:
        return -((~number + 1) & ((1 << bits) - 1))
    return number

def readVersionedFileAsBytearrray(file: str, version: str) -> bytearray:
    filename = f"baserom_{version}/{file}"
    return readFileAsBytearray(filename)

def readCsv(filepath: str) -> List[List[str]]:
    data: List[List[str]] = []
    with open(filepath) as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            data.append(list(row))

    return data
