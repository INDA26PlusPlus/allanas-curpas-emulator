import sys
from enum import IntEnum

"""

anton8 instruction set

4 bit opcode

| opcode (4 bits) |          rest (4 bits)           | next byte         | flags |
|      TRAP       |          number (4 bits)         |                   |       |
|      ADD        |  dest (2 bits) | source (2 bits) |                   |  zcn  |
|      ADDi       |  dest (2 bits) |  imm (2 bits)   |                   |  zcn  |
|      XOR        |  dest (2 bits) | source (2 bits) |                   |  zcn  |
|      XORi       |  dest (2 bits) |  imm (2 bits)   |                   |  zcn  |
|      LD         |  dest (2 bits) |  addr (2 bits)  |                   |       |
|      ST         |  addr (2 bits) | source (2 bits) |                   |       |
|      NOPPY      |          unused (4 bits)         |                   |       |
|      AND        |  dest (2 bits) | source (2 bits) |                   |  zcn  |
|      ANDi       |  dest (2 bits) |  imm (2 bits)   |                   |  zcn  |
|      JMP        |         cond (4 bits)            | target (8 bits)   |       |
|      LIT        |  dest (2 bits) | unused (2 bits) | value (8 bits)    |       |


opcodes:
    0 TRAP
    1 ADD
    2 ADDi
    3 XOR
    4 XORi
    5 LD
    6 ST
    7 NOPPY
    8 AND
    9 ANDi
    10 JMP
    11 LIT

traps:
    TRAP 0 = halt
    TRAP 1 = print stuff in r0 to stdout

"""

class Op(IntEnum):
    TRAP = 0 # done kinda
    ADD = 1 # done
    ADDi = 2 # done
    XOR = 3 # done
    XORi = 4 # done
    LD = 5 # done
    ST = 6 # done
    NOPPY = 7 # done
    AND = 8 # done
    ANDi = 9 # done
    JMP = 10 # done
    LIT = 11 # done



class CPU:
    def __init__(self):
        self.reg: list[int] = [0] * 4
        self.pc: int = 0
        self.rsp: int = 0

        self.z: bool = False
        self.c: bool = False
        self.n: bool = False



def get_bits(value, high, low):
    return (value >> low) & ((1 << (high - low + 1)) - 1)


def set_flags(cpu, dest):
    cpu.c = cpu.reg[dest] > 0xff
    cpu.reg[dest] = 0xff & cpu.reg[dest]
    if cpu.reg[dest] == 0:
        cpu.z = True
    else:
        cpu.z = False
    cpu.n = bool(cpu.reg[dest] & 0x80)

"""
program = bytes([
    0x70,  # NOP 01110000
    0x70,  # NOP
    0x27,  # ADDi r1, 3 00100111
    0x27,  # ADDi r1, 3
    0x00,  # TRAP 0
])
"""
program = bytes([
    0xb0, 0x0a,  # LIT r0, '0x0a'
    0x01,        # TRAP 1
    0xb0, 0x61,  # LIT r0, 'a' 10110000
    0x01,        # TRAP 1
    0xb0, 0x6e,  # LIT r0, 'n'
    0x01,        # TRAP 1
    0xb0, 0x74,  # LIT r0, 't'
    0x01,        # TRAP 1
    0xb0, 0x6f,  # LIT r0, 'o'
    0x01,        # TRAP 1
    0xb0, 0x6e,  # LIT r0, 'n'
    0x01,        # TRAP 1
    0xb0, 0x38,  # LIT r0, '8'
    0x01,        # TRAP 1
    0xb0, 0x0a,  # LIT r0, '0x0a'
    0x01,        # TRAP 1
    0xb0, 0x0a,  # LIT r0, '0x0a'
    0x01,        # TRAP 1
    0x00,        # TRAP 0
])



cpu = CPU()
memory = bytearray(256)

for address, byte in enumerate(program):
    memory[address] = byte

while True:
    instruction = memory[cpu.pc]
    cpu.pc = (cpu.pc + 1) & 0xff
    #print(cpu)

    opcode = instruction >> 4

    match opcode:
        case Op.NOPPY:
            pass
        case Op.ADD:
            dest = get_bits(instruction, 3, 2)
            src = get_bits(instruction, 1, 0)
            #print(f"{src:b} {dest:b}")
            cpu.reg[dest] = cpu.reg[dest] + cpu.reg[src]
            set_flags(cpu, dest)
        case Op.ADDi:
            dest = get_bits(instruction, 3, 2)
            src = get_bits(instruction, 1, 0)
            #print(f"{src:b} {dest:b}")
            cpu.reg[dest] = cpu.reg[dest] + src
            set_flags(cpu, dest)
        case Op.XOR:
            dest = get_bits(instruction, 3, 2)
            src = get_bits(instruction, 1, 0)
            cpu.reg[dest] = cpu.reg[src] ^ cpu.reg[dest]
            set_flags(cpu, dest)
        case Op.XORi:
            dest = get_bits(instruction, 3, 2)
            src = get_bits(instruction, 1, 0)
            cpu.reg[dest] = cpu.reg[dest] ^ src
            set_flags(cpu, dest)
        case Op.AND:
            dest = get_bits(instruction, 3, 2)
            src = get_bits(instruction, 1, 0)
            cpu.reg[dest] = cpu.reg[src] & cpu.reg[dest]
            set_flags(cpu, dest)
        case Op.ANDi:
            dest = get_bits(instruction, 3, 2)
            src = get_bits(instruction, 1, 0)
            cpu.reg[dest] = cpu.reg[dest] & src
            set_flags(cpu, dest)

        case Op.LD:
            dest = get_bits(instruction, 3, 2)
            src = get_bits(instruction, 1, 0)
            cpu.reg[dest] = memory[cpu.reg[src]]
        case Op.ST:
            dest = get_bits(instruction, 3, 2)
            src = get_bits(instruction, 1, 0)
            memory[cpu.reg[dest]] = cpu.reg[src]

        case Op.LIT:
            dest = get_bits(instruction, 3, 2)
            value = memory[cpu.pc]
            cpu.pc = (cpu.pc + 1) & 0xff
            cpu.reg[dest] = value
        case Op.JMP:
            # z = zero
            # c = carry
            # n = neg
            condition = get_bits(instruction, 3, 0)
            value = memory[cpu.pc]
            cpu.pc = (cpu.pc + 1) & 0xff
            match condition:
                case 0:
                    a = True
                case 1:
                    a = cpu.z
                case 2:
                    a = not cpu.z
                case 3:
                    a = cpu.c
                case 4:
                    a = not cpu.c
                case 5:
                    a = cpu.n
                case 6:
                    a = not cpu.n
            if a == True:
                cpu.pc = value

        case Op.TRAP:
            number = get_bits(instruction, 3, 0)
            if number == 0:
                break
            if number == 1:
                sys.stdout.write(chr(cpu.reg[0]))
                sys.stdout.flush()
            else:
                print(f"not implemented trap {number}")
        case _:
            print(f"weird opcode {hex(opcode)} {(cpu.pc - 1) & 0xff}")
            sys.exit(0)
