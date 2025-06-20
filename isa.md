# Viso-Fox Architecture and Instruction Set

## Overview

Viso-Fox is a hypothetical ISA designed to be simple. It uses 64 bit addressing only using little-endian format. IO uses data ports and are polled.Instructions range from 64 to 256 bits wide based on the number of operands. This document describes the architecture, instruction set, and other details of the Viso-Fox ISA.

## I/O

In total, there are 16 data ports from `0x00` to `0x0F` and each port is 64 bits wide. Each port is both readable and writeable using the `IN` and `OUT` respectively. They are not stored in memory but are directly accessible via the CPU.

### Data Ports

| **Data Port** | **Description**                      | **Direction** |
| -------------- | ----------------------------------- | ------------- |
| `0x00`         | Controller 1 (Fox-Pad)              | Read only     |
| `0x01`         | Controller 2 (Fox-Pad)              | Read only     |
| `0x02`         | Controller 3 (Fox-Pad)              | Read only     |
| `0x03`         | Controller 4 (Fox-Pad)              | Read only     |
| `0x04`         | Send character to IO                | Write only    |
| `0x05`         | Read character to IO                | Read only     |
| `0x06`         | Reserved                            | N/A           |
| `0x07`         | Reserved                            | N/A           |
| `0x08`         | Reserved                            | N/A           |
| `0x09`         | Reserved                            | N/A           |
| `0x0A`         | Reserved                            | N/A           |
| `0x0B`         | Reserved                            | N/A           |
| `0x0C`         | Reserved                            | N/A           |
| `0x0D`         | Reserved                            | N/A           |
| `0x0E`         | Reserved                            | N/A           |
| `0x0F`         | Programmable time-based interrupt   | Read only     |

### Fox-Pad Controllers

Viso-Fox offers support for the Fox-Pad controller which has the following buttons with the following mappings:

Four controllers are supported, mapping for each controller is as follows:

| **Controller ID** | **Data Port** | **Description** |
| ----------------- | ------------- | ----------------|
| 0                 | `0x00`        | Controller 1    |
| 1                 | `0x01`        | Controller 2    |
| 2                 | `0x02`        | Controller 3    |
| 3                 | `0x03`        | Controller 4    |

To read the state of a controller, you can use the `IN` instruction with the corresponding data port. Each bit represents whether that button is pressed (1) or not pressed (0).

| **Bit** | **Button** | **Description**                    |
| ------: | ---------- | ---------------------------------- |
|       0 | D\_LEFT    | D-pad left                         |
|       1 | D\_RIGHT   | D-pad right                        |
|       2 | D\_UP      | D-pad up                           |
|       3 | D\_DOWN    | D-pad down                         |
|       4 | SELECT     | Select / back button               |
|       5 | START      | Start / pause                      |
|       6 | A          | Primary action button (e.g., jump) |
|       7 | B          | Secondary action button            |
|       8 | X          | Tertiary action button             |
|       9 | Y          | Quaternary action button           |
|      10 | SH\_L      | Left shoulder                      |
|      11 | SH\_R      | Right shoulder                     |

### Console output

Data can be sent to the console output using the `OUT` over data port `0x04`. The data sent is a single character which is encoded in ASCII (four characters at a time). The console output is a simple text output that displays the characters sent to it. Keyboard input can be read using the `IN` instruction over data port `0x05`. The input is a single character which is encoded in ASCII (supports up to four characters at a time).

## ROM Disk format

Viso-Fox automatically loads the ROM Disk into memory during the boot process. This is loaded by the MBS which copies the data and code segments into their respective regions in memory.

ROM disks are broken up into two three sections:

- **Header**: Contains metadata about the ROM disk.
- **Data Section**: Contains the raw data segment.
- **Code Section**: Contains the raw code segment.

| **Field**       | **Size** | **Description**                                     |
| --------------- | -------- | --------------------------------------------------- |
| `VFOX`          | 4 bytes  | Magic number identifying the file format            |
| Version         | 4 bytes  | 32-bit version number                               |
| Future Data     | Any size | Reserved for future use, use data to know ROM start |
| Data Start Addr | 8 bytes  | 64-bit address where the data section begins        |
| Code Start Addr | 8 bytes  | 64-bit address where the code section begins        |
| Data Section    | Variable | Raw data segment                                    |
| Code Section    | Variable | Raw code segment                                    |

## Minimum Boot Sequence

The minimum boot sequence (MBS) is a low level sequence of instructions that copies the data segment and code segments from the ROM disk into RAM during machine initialisation. MBS is only present during the initial boot process and terminates once it is complete.

MBS copies the data section into the data segment of RAM and copies the code section into the code segment of RAM (start location is lined up with where the CPU starts executing code).

MBS maybe implemented in hardware or microcode, but it is not part of the Viso-Fox ISA so implementation details may differ.

## Display

The display is a 640x480 resolution with 64 colors but has an effective resolution 320x240 as it uses 2x2 pixel blocks to represent each color. The display is memory mapped and uses a 16 bit color depth. Each pixel takes 16 bits which corresponds to a colour in the palette. In total 19200 ulongs are used for the display memory (640 * 480 / 4). Note this memory region is locked while the display is being drawn by draw flag in the `FLAGS` register.

Colours are defined as follows (starting from index 0 to 63):

```text
#000000, #fabbaf, #eb758f, #d94c8e, #b32d7d, #fa9891, #ff7070, #f53141, #c40c2e, #852264, #faa032, #f58122, #f2621f, #db4b16, #9e4c4c, #fad937, #ffb938, #e69b22, #cc8029, #ad6a45, #ccc73d, #b3b02d, #989c27, #8c8024, #7a5e37, #94bf30, #55b33b, #179c43, #068051, #116061, #a0eba8, #7ccf9a, #5cb888, #3da17e, #20806c, #49c2f2, #25acf5, #1793e6, #1c75bd, #195ba6, #ae88e3, #7e7ef2, #586ac4, #3553a6, #243966, #e29bfa, #ca7ef2, #a35dd9, #773bbf, #4e278c, #b58c7f, #9e7767, #875d58, #6e4250, #472e3e, #a69a9c, #807980, #696570, #495169, #0d2140, #050e1a, #d9a798, #c4bbb3, #f2f2da
```

Colour palette is [Jehkoba64 Palette](https://lospec.com/palette-list/jehkoba64).

## Registers

| **Register** | **Description**                                   | **Access**        |
| ------------ | ------------------------------------------------- | ----------------- |
| `R0`–`R7`    | General-purpose registers                         | Read/Write        |
| `FLAGS`      | CPU status flags (Zero, Carry, Overflow, etc.)    | Read-only         |
| `PC`         | Program Counter – address of the next instruction | Write (via JMP)   |
| `SP`         | Stack Pointer – points to the top of the stack    | Write (limited)   |
| `BP`         | Base Pointer – used for stack frame management    | Read/Write        |
| `IO`         | I/O register – interface with ports               | Read/Write        |
| `IVT`        | Interrupt Table – address of the interrupt table  | Read-only         |

## Flags

| **Bit** | **Flag** | **Purpose**                          |
| ------- | -------- | ------------------------------------ |
| 0       | `Z`      | Zero — result was zero               |
| 1       | `S`      | Sign — result was negative (MSB = 1) |
| 2       | `O`      | Overflow — signed overflow occurred  |
| 3       | `C`      | Carry — unsigned overflow (optional) |
| 4       | `DR`     | Display draw - lock graphics region  |
| 5–63    | —        | Reserved for future use or cleared   |

## Memory regions

There are five main memory regions in Viso-Fox:

| Region               | Shorthand | Size          | Description                                                           |
| -------------------- | --------- | -----------   | --------------------------------------------------------------------- |
| **Interrupt Table**  | `IT`      | 2 KB          | 256 interrupt entries × 8 bytes (64 bits) each                        |
| **Graphics Segment** | `GS`      | 76.8 KB       | Memory-mapped display buffer (640×480 / 4 pixels × 2 bytes = 76.8 KB) |
| **Code Segment**     | `CS`      | Remaining 1/2 | Half of the remaining memory (after IT, GS, and SS)                   |
| **Data Segment**     | `DS`      | Remaining 1/2 | Other half of remaining memory (mirrored with code)                   |
| **Stack Segment**    | `SS`      | 256 KB        | Stack memory (default size, grows downwards)                          |
| **Total Memory**     | `MEM`     | 1 GB          | Total memory available for the system                                 |

Note: Default configuration is 1GB of memory in total so values here use that as a basis.

## Interrupts and Syscalls

Viso-Fox supports interrupts/syscalls two kinds of interrupts:

- **Time based interrupts**: Triggered by the system clock for scheduling and timing operations.
- **Software interrupts**: Invoked by the program to request services from the operating system - Syscalls.

### Invocation

Interrupts are invoked using the `int` instruction with a specific interrupt number. The CPU uses an Interrupt Vector Table (IVT) to map interrupt numbers to their corresponding handlers. The IVT is located at the start of memory and contains 256 entries, each 8 bytes long, for a total size of 2 KB.

`0x00` - is reserved for the timer interrupt configured via programmable time-based interrupt port `0x0F`.
Interrupts run until completion and give control back to the CPU with the `iret` instruction.

Each interrupt has a specific number which corresponds to directly to the entry in the table e.g. `0x00` corresponds to the first entry in the interrupt table. The table does not contain the interrupt number itself but an address to the interrupt handler.

Interrupts can interrupt each other, each subsequent interrupt will push to the stack so user programs should not use their own interrupts but rely on ones provided by the operating environment where possible.

NOTE: Long running interrupts can cause the system to become unresponsive so should be avoided. In such cases, the time based interrupt will still run to prevent the system from hanging.

NOTE: The time based interrupt will only occur after it finishes by the time specified in the programmable time-based interrupt port `0x0F`. So if it runs twice as long as the time specified, it will not run again until the next time it is scheduled from it completing to prevent the system from hanging.

### Behaviours

If an interrupt entry is defined as `0x00`, it is considered an invalid interrupt and perform a `nop` (No Operation) instead of invoking an interrupt handler. This allows the CPU to skip over unused or unimplemented interrupts without causing an error.

When an interrupt is invoked, the CPU saves the current state of the program (registers and flags) onto the stack before transferring control to the interrupt handler. This ensures that when the interrupt handler completes, it can restore the program state and continue execution seamlessly.

When `int` is invoked, the CPU performs the following steps:

1. Pushes R0-R7
2. Pushes FLAGS
3. Pushes PC (Program Counter)
4. Updates the stack pointer (SP) to point to the new top of the stack.
5. Sets the PC to the address of the interrupt handler from the IVT.

When the interrupt handler completes, it uses the `iret` instruction to return control back to the program. The CPU performs the following steps:

1. Pops the PC (Program Counter) from the stack.
2. Pops FLAGS from the stack.
3. Pops R0-R7 from the stack.
4. Restores the stack pointer (SP) to its previous value.
5. Resumes execution from the address stored in the PC.

### Invoking interrupts via assembly

- **INT** INTERRUPT_NUMBER: Invoke a specific interrupt by number.
- **IRET**: Return from the last invoked interrupt.

## Instruction

Each instruction must be at least 1 ulong in length with an optional three ulongs as operands.

### Breakdown

Instruction must have 0x0F (F0X0 backwards) to denote it as a valid instruction else the CPU will perform a NOP with operand count of 0.

Each each instruction increments the program counter by one plus the number of operands specified in the instruction.

The instruction format is as follows:

| Bits  | Field      | Description                       |
| ----- | ---------- | --------------------------------- |
| 0–3   | `Code`     | Instruction prefix (`0xF`)        |
| 4–19  | `Opcode`   | Operation code (16 bits)          |
| 20–23 | `Operand`  | Operand count (0–3)               |
| 24–27 | `Mode1`    | Addressing mode for operand 1     |
| 28–31 | `Mode2`    | Addressing mode for operand 2     |
| 32–35 | `Mode3`    | Addressing mode for operand 3     |
| 36–63 | `Reserved` | Reserved for future use (28 bits) |

### Instruction opcodes

All instructions are encoded as 16-bit opcodes and require a denotation (`0xF`) to indicate that it is a valid instruction. The opcode is followed by an operand count and up to three operands, each of which can be in one of five addressing modes.

If a destination operand is not specified, the result is stored in the first source operand. The destination operand must be a register or memory location.

For an exhaustive list of supported operands and their addressing modes for each instruction, see the [instruction-table.md](instruction-table.md).

#### Common instructions

| Mnemonic | Operands           | Opcode   | Description                           |
| -------- | ------------------ | -------- | ------------------------------------- |
| `nop`    | —                  | `0x0000` | No operation                          |
| `mov`    | `source, dest`     | `0x0001` | Move value from source to destination |
| `cmp`    | `source1, source2` | `0x0002` | Compare two values                    |
| `hlt`    | —                  | `0xFFFF` | Halt execution                        |

#### Control flow instructions

| Mnemonic | Operands  | Opcode   | Description                   |
| -------- | --------- | -------- | ----------------------------- |
| `jmp`    | `address` | `0x0003` | Jump to address               |
| `jz`     | `address` | `0x0004` | Jump if zero                  |
| `jnz`    | `address` | `0x0005` | Jump if not zero              |
| `jl`     | `address` | `0x0006` | Jump if less than             |
| `jle`    | `address` | `0x0007` | Jump if less than or equal    |
| `jg`     | `address` | `0x0008` | Jump if greater than          |
| `jge`    | `address` | `0x0009` | Jump if greater than or equal |

#### Arithmetic instructions

Instructions such as `add`, `sub`, `mul` and `div` operate on two source operands and a destination operand but if this destination operand is not specified, the result is stored in the first source operand. The destination operand must be a register or memory location.

| Mnemonic | Operands                 | Opcode   | Description         |
| -------- | ------------------------ | -------- | ------------------- |
| `add`    | `source1, source2, dest` | `0x000A` | Add two values      |
| `sub`    | `source1, source2, dest` | `0x000B` | Subtract two values |
| `mul`    | `source1, source2, dest` | `0x000C` | Multiply two values |
| `div`    | `source1, source2, dest` | `0x000D` | Divide two values   |
| `inc`    | `value`                  | `0x000E` | Increment value     |
| `dec`    | `value`                  | `0x000F` | Decrement value     |
| `neg`    | `value`                  | `0x0010` | Negate value        |

#### Bitwise instructions

If no destination operand is specified, the result is stored in the first source operand. The destination operand must be a register or memory location.

| Mnemonic | Operands                 | Opcode   | Description |
| -------- | ------------------------ | -------- | ----------- |
| `and`    | `source1, source2, dest` | `0x0011` | Bitwise AND |
| `or`     | `source1, source2, dest` | `0x0012` | Bitwise OR  |
| `xor`    | `source1, source2, dest` | `0x0013` | Bitwise XOR |
| `not`    | `value`                  | `0x0014` | Bitwise NOT |

#### Shift and rotate instructions

| Mnemonic | Operands      | Opcode   | Description     |
| -------- | ------------- | -------- | --------------- |
| `shl`    | `value, dest` | `0x0015` | Shift left      |
| `shr`    | `value, dest` | `0x0016` | Shift right     |
| `rol`    | `value, dest` | `0x0017` | Rotate left     |
| `ror`    | `value, dest` | `0x0018` | Rotate right    |
| `bswap`  | `value`       | `0x0019` | Byte-swap value |

### Interrupt instructions

| Mnemonic | Operands | Opcode   | Description           |
| -------- | -------- | -------- | --------------------- |
| `int`    | `number` | `0x001A` | Invoke an interrupt   |
| `iret`   | —        | `0x001B` | Return from interrupt |

#### Stack instructions

| Mnemonic | Operands  | Opcode   | Description                                  |
| -------- | --------- | -------- | -------------------------------------------- |
| `push`   | `value`   | `0x001C` | Push value onto stack                        |
| `pop`    | `dest`    | `0x001D` | Pop value from stack                         |
| `call`   | `address` | `0x001E` | Call subroutine (jump + push return address) |
| `ret`    | —         | `0x001F` | Return from subroutine                       |

#### I/O instructions

| Mnemonic | Operands      | Opcode   | Description        |
| -------- | ------------- | -------- | ------------------ |
| `in`     | `port, dest`  | `0x0020` | Read from I/O port |
| `out`    | `value, port` | `0x0021` | Write to I/O port  |

## Addressing modes

There are five addressing modes for instructions such as `mov`. `PORT` is only used for I/O instructions such as `in` and `out`. The addressing modes are as follows:

| Code | Mnemonic  | Name                   | Example            | Description                                                                   |
| ---- | --------- | ---------------------- | ------------------ | ----------------------------------------------------------------------------- |
| 0x0  | `NULL`    | Zero addressing        | NOP                | Used for instructions which do not require addressing (no use, for debugging) |
| 0x1  | `IMM`     | Immediate              | `MOV 42, RX`       | Move constant value 42 into register `RX` (value is encoded in instruction)   |
| 0x2  | `REG`     | Register               | `MOV RY, RX`       | Move value from `RY` into `RX`                                                |
| 0x3  | `MEM`     | Direct Memory          | `MOV [0x1000], RX` | Move value from memory at address `0x1000` into `RX`                          |
| 0x4  | `IND`     | Indirect Memory        | `MOV [RY], RX`     | Move value from memory address stored in register `RY` into `RX`              |
| 0x5  | `PORT`    | I/O Port               | `IN 0x04, RX`      | Read value from I/O port `0x04` into `RX`                                     |

Note: Use `NULL` for instructions which require no addressing mode e.g. `hlt`, `nop` as these take no operands.

## Assembly syntax

See [assembly.md](assembly.md) for the assembly syntax and how to write programs in Viso-Fox assembly language.
