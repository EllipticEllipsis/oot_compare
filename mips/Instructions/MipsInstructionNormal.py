#!/usr/bin/python3

from __future__ import annotations

from ..Utils import *

from .MipsInstructionBase import InstructionBase


class InstructionNormal(InstructionBase):
    NormalOpcodes = {
        0b000_000: "SPECIAL",
        0b000_001: "REGIMM",
        0b000_010: "J", # Jump
        0b000_011: "JAL", # Jump And Link
        0b000_100: "BEQ", # Branch on EQual
        0b000_101: "BNE", # Branch on Not Equal
        0b000_110: "BLEZ", # Branch on Less than or Equal to Zero
        0b000_111: "BGTZ", # Branch on Greater Than Zero

        0b001_000: "ADDI", # Add Immediate
        0b001_001: "ADDIU", # Add Immediate Unsigned Word
        0b001_010: "SLTI", # Set on Less Than Immediate
        0b001_011: "SLTIU", # Set on Less Than Immediate Unsigned
        0b001_100: "ANDI", # And Immediate
        0b001_101: "ORI", # Or Immediate
        0b001_110: "XORI", # eXclusive OR Immediate
        0b001_111: "LUI", # Load Upper Immediate

        0b010_000: "COP0", # Coprocessor OPeration z
        0b010_001: "COP1", # Coprocessor OPeration z
        0b010_010: "COP2", # Coprocessor OPeration z
        0b010_011: "COP3", # Coprocessor OPeration z
        0b010_100: "BEQL", # Branch on EQual Likely
        0b010_101: "BNEL", # Branch on Not Equal Likely
        0b010_110: "BLEZL", # Branch on Less than or Equal to Zero Likely
        0b010_111: "BGTZL", # Branch on Greater Than Zero Likely

        0b011_000: "DADDI", # Doubleword add Immediate
        0b011_001: "DADDIU", # Doubleword add Immediate Unsigned
        0b011_010: "LDL", # Load Doubleword Left
        0b011_011: "LDR", # Load Doubleword Right
        # 0b011_100: "",
        # 0b011_101: "",
        # 0b011_110: "",
        # 0b011_111: "",

        0b100_000: "LB", # Load Byte
        0b100_001: "LH", # Load Halfword
        0b100_010: "LWL", # Load Word Left
        0b100_011: "LW", # Load Word
        0b100_100: "LBU", # Load Byte Insigned
        0b100_101: "LHU", # Load Halfword Unsigned
        0b100_110: "LWR", # Load Word Right
        0b100_111: "LWU", # Load Word Unsigned

        0b101_000: "SB", # Store Byte
        0b101_001: "SH", # Store Halfword
        0b101_010: "SWL", # Store Word Left
        0b101_011: "SW", # Store Word
        0b101_100: "SDL", # Store Doubleword Left
        0b101_101: "SDR", # Store Doubleword Right
        0b101_110: "SWR", # Store Word Right
        # 0b101_111: "",

        0b110_000: "LL", # Load Linked word
        0b110_001: "LWC1", # Load Word to Coprocessor z
        0b110_010: "LWC2", # Load Word to Coprocessor z
        0b110_011: "PREF", # Prefetch
        0b110_100: "LLD", # Load Linked Doubleword
        0b110_101: "LDC1", # Load Doubleword to Coprocessor z
        0b110_110: "LDC2", # Load Doubleword to Coprocessor z
        0b110_111: "LD", # Load Doubleword

        0b111_000: "SC", # Store Conditional word
        0b111_001: "SWC1", # Store Word from Coprocessor z
        0b111_010: "SWC2", # Store Word from Coprocessor z
        # 0b111_011: "",
        0b111_100: "SCD", # Store Conditional Doubleword
        0b111_101: "SDC1", # Store Doubleword from Coprocessor z
        0b111_110: "SDC2", # Store Doubleword from Coprocessor z
        0b111_111: "SD", # Store Doubleword
    }

    def isImplemented(self) -> bool:
        if self.opcode not in InstructionNormal.NormalOpcodes:
            return False
        opcode = self.getOpcodeName()
        if opcode in ("SPECIAL", "REGIMM", "COP0", "COP1", "COP2", "COP3"):
            return False
        return True

    def isBranch(self) -> bool:
        opcode = self.getOpcodeName()
        if opcode in ("BEQ", "BEQL", "BLEZ", "BLEZL", "BNE", "BNEL", "BGTZ", "BGTZL"):
            return True
        return super().isBranch()

    def isJType(self) -> bool: # OP LABEL
        opcode = self.getOpcodeName()
        if opcode in ("J", "JAL"):
            return True
        return super().isJType()

    def isIType(self) -> bool: # OP rt, IMM(rs)
        if self.isJType():
            return False
        if self.isIType2():
            return False
        if self.isIType3():
            return False
        if self.isIType4():
            return False
        if self.isIType5():
            return False
        return True
    def isIType2(self) -> bool: # OP  rs, rt, IMM
        opcode = self.getOpcodeName()
        if opcode == "BEQ" or opcode == "BEQL":
            return True
        if opcode == "BNE" or opcode == "BNEL":
            return True
        return False
    def isIType3(self) -> bool: # OP  rt, rs, IMM
        opcode = self.getOpcodeName()
        if opcode == "ADDI" or opcode == "ADDIU":
            return True
        if opcode == "ANDI":
            return True
        if opcode == "DADDI" or opcode == "DADDIU":
            return True
        if opcode == "ORI" or opcode == "XORI":
            return True
        if opcode == "SLTI" or opcode == "SLTIU":
            return True
        return False
    def isIType4(self) -> bool: # OP  rs, IMM
        opcode = self.getOpcodeName()
        if opcode in ("BLEZ", "BGTZ", "BLEZL", "BGTZL"):
            return True
        return False
    def isIType5(self) -> bool: # OP  rt, IMM
        opcode = self.getOpcodeName()
        if opcode in ("LUI", ):
            return True
        return False


    def sameOpcode(self, other: InstructionBase) -> bool:
        if self.opcode != other.opcode:
            return False

        return self.isImplemented()


    def modifiesRt(self) -> bool:
        if self.isBranch():
            return False
        opcode = self.getOpcodeName()
        if opcode in ("SB", "SH", "SWL", "SW", "SDL", "SDR", "SWR"):
            return False
        if opcode in ("LWC1", "LWC2", "LDC1", "LDC2"): # Changes the value of the coprocessor's register
            return False
        if opcode in ("SWC1", "SWC2", "SDC1", "SDC2"):
            return False
        return super().modifiesRt()


    def getOpcodeName(self) -> str:
        if self.opcode in InstructionNormal.NormalOpcodes:
            return InstructionNormal.NormalOpcodes[self.opcode]
        return super().getOpcodeName()


    def disassemble(self) -> str:
        opcode = self.getOpcodeName().lower().ljust(7, ' ')
        rs = self.getRegisterName(self.rs)
        rt = self.getRegisterName(self.rt)
        immediate = toHex(self.immediate, 4)

        if "COP" in self.getOpcodeName(): # Hack until I implement COPz instructions
            instr_index = toHex(self.instr_index, 7)
            return f"{opcode} {instr_index}"

        if self.getOpcodeName() == "NOP":
            return "nop"
        if self.isIType5():
            result = f"{opcode} {rt},"
            result = result.ljust(14, ' ')
            return f"{result} {immediate}"
        elif self.isIType():
            # TODO: use float registers
            result = f"{opcode} {rt},"
            result = result.ljust(14, ' ')
            return f"{result} {immediate}({rs})"
        elif self.isIType2():
            result = f"{opcode} {rs},"
            result = result.ljust(14, ' ')
            result += f" {rt},"
            result = result.ljust(19, ' ')
            if self.getOpcodeName() == "BEQ":
                if self.rs == 0 and self.rt == 0:
                    result = "b".ljust(7, ' ')
            return f"{result} {immediate}"
        elif self.isIType3():
            result = f"{opcode} {rt},"
            result = result.ljust(14, ' ')
            result += f" {rs},"
            result = result.ljust(19, ' ')
            return f"{result} {immediate}"
        elif self.isIType4():
            result = f"{opcode} {rs},"
            result = result.ljust(14, ' ')
            return f"{result} {immediate}"
        elif self.isJType():
            # instr_index = toHex(self.instr_index, 7)
            # return f"{opcode} {instr_index}"
            instrIndexHex = toHex(self.instr_index<<2, 6)[2:]
            label = f"func_80{instrIndexHex}"
            #if (self.instr_index<<2) % 16 == 0 and (self.instr_index<<2) & 0x800000:
                #print(label)
            return f"{opcode} {label}"
        return super().disassemble()
