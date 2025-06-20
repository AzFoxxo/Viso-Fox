# Instruction Set Table

This table contains contains operand mnemonic, operands, opcode, description and operand types supported for each.

Note: Some instructions allow both `source, source, dest` and `source/dest, source`. In these cases, the operand on the left is valid as a source only, while the rightmost operand is permitted as a source and destination.

| Mnemonic | Operands               | Opcode | Description                                  | Operand Type #1 (source\|dest)   | Operand Type #2    | Operand Type #3     |
|----------|------------------------|--------|----------------------------------------------|----------------------------------|--------------------|---------------------|
| nop      | —                      | 0x0000 | No operation                                 | NULL                             | NULL               | NULL                |
| mov      | source, dest           | 0x0001 | Move value from source to destination        | IMM, REG, MEM, IND               | REG, MEM, IND      | NULL                |
| cmp      | source1, source2       | 0x0002 | Compare two values                           | IMM, REG, MEM, IND               | IMM, REG, MEM, IND | NULL                |
| hlt      | —                      | 0xFFFF | Halt execution                               | NULL                             | NULL               | NULL                |
| jmp      | address                | 0x0003 | Jump to address                              | IMM, REG, MEM, IND               | NULL               | NULL                |
| jz       | address                | 0x0004 | Jump if zero                                 | IMM, REG, MEM, IND               | NULL               | NULL                |
| jnz      | address                | 0x0005 | Jump if not zero                             | IMM, REG, MEM, IND               | NULL               | NULL                |
| jl       | address                | 0x0006 | Jump if less than                            | IMM, REG, MEM, IND               | NULL               | NULL                |
| jle      | address                | 0x0007 | Jump if less than or equal                   | IMM, REG, MEM, IND               | NULL               | NULL                |
| jg       | address                | 0x0008 | Jump if greater than                         | IMM, REG, MEM, IND               | NULL               | NULL                |
| jge      | address                | 0x0009 | Jump if greater than or equa                 | IMM, REG, MEM, IND               | NULL               | NULL                |
| add      | source1, source2, dest | 0x000A | Add two values                               | IMM, REG, MEM, IND\|REG          | IMM, REG, MEM, IND | REG, NULL           |
| sub      | source1, source2, dest | 0x000B | Subtract two values                          | IMM, REG, MEM, IND\|REG          | IMM, REG, MEM, IND | REG, NULL           |
| mul      | source1, source2, dest | 0x000C | Multiply two values                          | IMM, REG, MEM, IND\|REG          | IMM, REG, MEM, IND | REG, NULL           |
| div      | source1, source2, dest | 0x000D | Divide two values                            | IMM, REG, MEM, IND\|REG          | IMM, REG, MEM, IND | REG, NULL           |
| inc      | value                  | 0x000E | Increment value                              | REG, MEM, IND                    | NULL               | NULL                |
| dec      | value                  | 0x000F | Decrement value                              | REG, MEM, IND                    | NULL               | NULL                |
| neg      | value                  | 0x0010 | Negate value                                 | REG, MEM, IND                    | NULL               | NULL                |
| and      | source1, source2, dest | 0x0011 | Bitwise AND                                  | IMM,REG, MEM, IND\|REG, MEM, IND | IMM,REG, MEM, IND  | REG, MEM, IND, MULL |
| or       | source1, source2, dest | 0x0012 | Bitwise OR                                   | IMM,REG, MEM, IND\|REG, MEM, IND | IMM,REG, MEM, IND  | REG, MEM, IND, MULL |
| xor      | source1, source2, dest | 0x0013 | Bitwise XOR                                  | IMM,REG, MEM, IND\|REG, MEM, IND | IMM,REG, MEM, IND  | REG, MEM, IND, MULL |
| not      | value                  | 0x0014 | Bitwise NOT                                  | REG, MEM, IND                    | NULL               | NULL                |
| shl      | value, dest            | 0x0015 | Shift left                                   | IMM, REG                         | REG, MEM, IND      | NULL                |
| shr      | value, dest            | 0x0016 | Shift right                                  | IMM, REG                         | REG, MEM, IND      | NULL                |
| rol      | value, dest            | 0x0017 | Rotate left                                  | IMM, REG                         | REG, MEM, IND      | NULL                |
| ror      | value, dest            | 0x0018 | Rotate right                                 | IMM, REG                         | REG, MEM, IND      | NULL                |
| bswap    | value                  | 0x0019 | Byte-swap value                              | REG, MEM, IND                    | NULL               | NULL                |
| int      | number                 | 0x001A | Invoke an interrupt                          | IMM, REG, MEM, IND               | NULL               | NULL                |
| iret     | —                      | 0x001B | Return from interrupt                        | NULL                             | NULL               | NULL                |
| push     | value                  | 0x001C | Push value onto stack                        | IMM, REG, MEM, IND               | NULL               | NULL                |
| pop      | dest                   | 0x001D | Pop value from stack                         | REG, MEM, IND                    | NULL               | NULL                |
| call     | address                | 0x001E | Call subroutine (jump + push return address) | IMM, REG, MEM, IND               | NULL               | NULL                |
| ret      | —                      | 0x001F | Return from subroutine                       | NULL                             | NULL               | NULL                |
| in       | port, dest             | 0x0020 | Read from I/O port                           | PORT                             | REG, MEM, IND      | NULL                |
| out      | value, dest            | 0x0021 | Write to I/O port                            | IMM, REG, MEM, IND               | PORT               | NULL                |
