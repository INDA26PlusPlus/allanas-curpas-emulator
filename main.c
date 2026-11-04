#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

__attribute__((constructor))
void setup() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

/*

4 bit opcode

| opcode (4 bits) |          rest (4 bits)           |
|      ADD        |  dest (2 bits) | source (2 bits) |
|      ADDi       |  dest (2 bits) |  imm (2 bits)   |

opcodes:
    0 TRAP
    1 ADD
    2 AND
    3 XOR
    4 LD
    5 ST
    6 NOP

traps:
    TRAP 0 = print stuff in r0 to stdout

*/


enum {
    TRAP, // kinda done
    ADD, // done
    ADDi, // done
    XOR,
    XORi,
    LD,
    ST,
    NOP // done
};

typedef struct {
    uint8_t reg[4];
    uint8_t pc;
    uint8_t rsp;
} CPU;

uint8_t get_bits(uint8_t value, int high, int low) {
    uint8_t a = (value << (7-high));
    a = (a >> ((7-high)+low));

    return a;
}

uint8_t program[] = {
    0xe0, // NOP
    0xe0, // NOP
    0x4f, // ADDi r1, 8  01001111
    0x22, // ADD r0, r1
    0x00, // TRAP 0
};

int main() {
    CPU cpu = {0};
    uint8_t *memory = malloc(256);

    memcpy(memory, program, sizeof(program));
    uint8_t pc = 0;

    while (1) {
        uint8_t instruction = memory[pc];
        //printf("%b\n", instruction);
        pc += 1;

        uint8_t opcode = instruction >> 4;
        //printf("%b\n", opcode);

        switch (opcode) {
            case NOP:
                break;
            case ADD:
                uint8_t dest = get_bits(instruction, 3, 2);
                uint8_t src = get_bits(instruction, 1, 0);
                //printf("%d %d\n", cpu.reg[dest], cpu.reg[src]);
                cpu.reg[dest] = cpu.reg[dest] + cpu.reg[src];
                //printf("%d %d\n", cpu.reg[dest], cpu.reg[src]);

                break;
            case ADDi:
                dest = get_bits(instruction, 3, 2);
                src = get_bits(instruction, 1, 0);
                cpu.reg[dest] = cpu.reg[dest] + src;
                
                break;
            case XOR:
                dest = get_bits(instruction, 3, 2);
                src = get_bits(instruction, 1, 0);
                //printf("%d %d\n", cpu.reg[dest], cpu.reg[src]);
                cpu.reg[dest] = cpu.reg[dest] ^ cpu.reg[src];
                //printf("%d %d\n", cpu.reg[dest], cpu.reg[src]);

                break;
            case TRAP:
                uint8_t number = get_bits(instruction, 3, 0);
                switch (number) {
                    case 0:
                        putchar((char)cpu.reg[0]);
                        break;
                    default:
                        printf("not implemented trap %d\n", number);
                        break;
                }
            default:
                printf("weird opcode %x %04x\n", opcode, pc - 1);
                exit(0);

        }
    }
}