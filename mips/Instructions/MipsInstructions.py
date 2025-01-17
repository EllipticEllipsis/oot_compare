#!/usr/bin/python3

from __future__ import annotations

from ..Utils import *

from .MipsInstructionBase import InstructionBase
from .MipsInstructionNormal import InstructionNormal
from .MipsInstructionSpecial import InstructionSpecial
from .MipsInstructionRegimm import InstructionRegimm
from .MipsInstructionCoprocessor1 import InstructionCoprocessor1


def wordToInstruction(word: int) -> InstructionBase:
    if ((word >> 26) & 0x3F) == 0x00:
        return InstructionSpecial(word)
    if ((word >> 26) & 0x3F) == 0x01:
        return InstructionRegimm(word)
    if ((word >> 26) & 0x3F) == 0x10:
        # COP0
        pass
    if ((word >> 26) & 0x3F) == 0x11:
        return InstructionCoprocessor1(word)
    if ((word >> 26) & 0x3F) == 0x12:
        # COP2
        pass
    return InstructionNormal(word)
