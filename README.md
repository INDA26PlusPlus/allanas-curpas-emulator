# allanas-curpas-emulator
8 bit emulator xdxdxdlmao

```py

"""


4 bit opcode

| opcode (4 bits) |          rest (4 bits)           | next byte    | flags |
|      TRAP       |          number (4 bits)         |              |       |
|      ADD        |  dest (2 bits) | source (2 bits) |              |  zcn  |
|      ADDi       |  dest (2 bits) |  imm (2 bits)   |              |  zcn  |
|      XOR        |  dest (2 bits) | source (2 bits) |              |  zcn  |
|      XORi       |  dest (2 bits) |  imm (2 bits)   |              |  zcn  |
|      LD         |  dest (2 bits) |  addr (2 bits)  |              |       |
|      ST         |  addr (2 bits) | source (2 bits) |              |       |
|      NOPPY      |          unused (4 bits)         |              |       |
|      AND        |  dest (2 bits) | source (2 bits) |              |  zcn  |
|      ANDi       |  dest (2 bits) |  imm (2 bits)   |              |  zcn  |
|      JMP        |         cond (4 bits)            | target (8)   |       |
|      LIT        |  dest (2 bits) | unused (2 bits) | value (8)    |       |


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

```