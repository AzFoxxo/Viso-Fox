# Viso-Fox Architecture and Instruction Set

## Overview

Viso-Fox is a hypothetical ISA designed to be simple. It uses 64 bit addressing only using little-endian format. IO uses interrupts.

## IO

Viso-Fox offers support for the Fox-Pad controller which has the following buttons with the following mappings:

| Button  | Mapping |
| ------- | ------- |
| JUMP    | 0x11    |
| LEFT    | 0x12    |
| RIGHT   | 0x13    |
| UP      | 0x14    |
| DOWN    | 0x15    |
| ESCAPE  | 0x16    |
| START   | 0x17    |
| SELECT  | 0x18    |
| A       | 0x19    |
| B       | 0x1A    |
| C       | 0x1B    |
| D       | 0x1C    |
| MENU    | 0x1D    |

There is a single debug output which uses the `0xF0` to `0xFF` range for debug output. Push a single character to shared register `RS` and then invoke the interrupt `0xF0` to output the character to the debug console.

| Debug Output       | Mapping | Description                                             |
| ------------------ | ------- | ------------------------------------------------------- |
| Character output   | 0xF0    | Send character to 'RS'                                  |
| Clear debug output | 0xF1    | Clear debug console called                              |
| Debug input        | 0xF2    | Invoked when called and ascii character is sent to 'RS' |
| Debug input clear  | 0xF3    | Clear debug input buffer                                |

### Assembly interrupt mapping

Say we want to run our own code when A is pressed, we can do this by defining a label we can set the value of the interrupt handler to the address of our code. For example:

```asm
section data

section code

    ; Set the interrupt handler for A button press
    main:
        MOV a_button_press, [0x11]

    ; Code to run when A is pressed - code executed here is using shadow registers and shadow stack
    a_button_press:
        ; Return to main program
        IRET ; Return from interrupt

```

## ROM Disk format

Head starts with the magic number `VFOX` followed by 64 bit version number, start of the data section in 64 bit, start of the code section in 64 bit, the data section, the code section.

## Minimum Boot Sequence

The minimum boot sequence (MBS) is a low level sequence of instructions that copies the data segment and code segments from the ROM disk into RAM during machine initialisation. MBS is only present during the initial boot process and terminates once it is complete.

## Display

The display is a 640x480 resolution with 54 colors but has an effective resolution 320x240 as it uses 2x2 pixel blocks to represent each color. The display is memory mapped and uses a 16 bit color depth. Each pixel takes 16 bits which corresponds to a colour in the palette. In total 19200 ulongs are used for the display memory (640 * 480 / 4).

Colours are defined as follows:

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 | 54 |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| #26232f | #314047 | #596d62 | #929c74 | #c8c5a3 | #fcfcfc | #1b377f | #147abf | #40afdd | #b2dbf4 | #181667 | #3b2c96 | #706ae1 | #8f95ee | #440a41 | #812593 | #cc4bb9 | #ec99db | #3f0011 | #b31c35 | #ef2064 | #f26282 | #960811 | #e81813 | #a75d69 | #ec9ea4 | #560d04 | #c43611 | #e26a12 | #f0af66 | #2a1a14 | #5d342a | #a66e46 | #df9c6e | #8e4e11 | #d89511 | #ead11e | #f5eb6b | #2f541c | #5a831b | #a2bb1e | #c6df6b | #0f450f | #008b12 | #0bcb12 | #3ef33f | #115153 | #0c8563 | #04bf79 | #6ae6aa | #262726 | #514f4c | #887e83 | #b3aac0 |

## Registers

| Register | Shadow | Purpose                                    | Read | Write | Notes                                  |
| -------- | ------ | ------------------------------------------ | ---- | ----- | -------------------------------------- |
| `RX`     | `RXS`  | General-purpose register                   | ✅    | ✅   | Used in normal and interrupt mode      |
| `RY`     | `RYS`  | General-purpose register                   | ✅    | ✅   | Used in normal and interrupt mode      |
| `RZ`     | `RZS`  | General-purpose register                   | ✅    | ✅   | Used in normal and interrupt mode      |
| `PC`     | —      | Program Counter — next instruction address | ❌    | ❌   | Jump writes to only or machine tick    |
| `SP`     | `SPS`  | Stack Pointer — top of the stack           | ✅    | ✅   | Machine-controlled during PUSH/POP     |
| `BP`     | `BPS`  | Base Pointer — stack frame management      | ✅    | ✅   | Software-managed                       |
| `RS`     |  `RS`  | Shared register for both main and shadow   | ✅    | ✅   | Used for passing data                  |

## Flags

| Flag | Name           | Set By                      | Read  | Write  | Description                                               |
| ---- | -------------- | --------------------------- | ----  | ------ | ---------------------------------------------------------- |
| `ZF` | Zero Flag      | ALU operations              | ✅    | ❌     | Set if the result of the last operation was **zero**       |
| `CF` | Carry Flag     | Arithmetic (add/sub)        | ✅    | ❌     | Set if the last operation resulted in a **carry**          |
| `SF` | Sign Flag      | Arithmetic/logic operations | ✅    | ❌     | Set if the result of the last operation was **negative**   |
| `OF` | Overflow Flag  | Arithmetic operations       | ✅    | ❌     | Set if the last operation resulted in an **overflow**      |
| `IF` | Interrupt Flag | `INT`/`IRET`, system state  | ✅    | ✅     | Set if **interrupts are enabled**; can be manually toggled |

## Memory regions

There are five main memory regions in Viso-Fox:

| Region               | Shorthand | Size          | Description                                                           |
| -------------------- | --------- | -----------   | --------------------------------------------------------------------- |
| **Interrupt Table**  | `IT`      | 2 KB          | 256 interrupt entries × 8 bytes (64 bits) each                        |
| **Graphics Segment** | `GS`      | 76.8 KB       | Memory-mapped display buffer (640×480 / 4 pixels × 2 bytes = 76.8 KB) |
| **Code Segment**     | `CS`      | Remaining 1/2 | Half of the remaining memory (after IT, GS, and SS)                   |
| **Data Segment**     | `DS`      | Remaining 1/2 | Other half of remaining memory (mirrored with code)                   |
| **Shadow Stack**     | `LSS`     | 128 KB        | Used exclusively by interrupts; uses shadow registers                 |
| **Main Stack**       | `HSS`     | 128 KB        | Used by program; stack grows downward from top of memory              |
| **Stack Segment**    | `SS`      | 256 KB        | Combined size of shadow and main stacks                               |
| **Total Memory**     | `MEM`     | 1 GB          | Total memory available for the system                                 |

Note: Default configuration is 1GB of memory in total so values here use that as a basis.

## Interrupts/syscalls

Viso-Fox supports interrupts which maybe triggered by machine state such as I/O, initialisation, etc. or by software. These interrupts are stored from 0x0000 to 0x00FE and are invoked via the `INT` instruction. State is saved as interrupts use shadow registers.

Interrupts run until completion and give control back to the CPU with the `IRET` instruction.

Each interrupt has a specific number which corresponds to directly to the entry in the table e.g. 0x00 corresponds to the first entry in the interrupt table. The table does not contain the interrupt number itself but an address to the interrupt handler.

Note: Registers are not shared between interrupts and the main program as the CPU uses shadow registers.

### Invoking interrupts via assembly

- **INT** INTERRUPT_NUMBER: Invoke a specific interrupt by number.
- **IRET**: Return from the last invoked interrupt.

## Time based interrupts

Viso-Fox supports time based interrupts which are triggered by the system clock. These interrupts are used for scheduling and timing operations.
0x00 - Is invoked every 1ms.
0x01 - Is invoked every 5ms.
0x02 - Is invoked every 10ms.

For time based interrupts, if no interrupt handler is defined (address is `0x00`), the CPU will simply return to the main program after the interrupt is invoked.

## Instruction

Each instruction must be at least 1 ulong in length with an optional three ulongs as operands.

### Breakdown

Instruction must have 0x0F (F0X0 backwards) to denote it as a valid instruction else the CPU will perform a NOP with operand count of 0.

Each each instruction increments the program counter by one plus the number of operands specified in the instruction.

The instruction format is as follows:

| Bits    | Field         | Description                                                          |
|---------|---------------|----------------------------------------------------------------------|
| 0–3     | F (4)         | Instruction prefix (fixed at `0x0F` to denote a valid instruction)   |
| 4–7     | O (4)         | Operand count (0 to 3)                                               |
| 8–11    | Read Mode (4) | Read addressing mode (e.g., register, indirect, memory)              |
| 12–15   | Write Mode (4)| Write addressing mode (e.g., register, indirect, memory)             |
| 16–31   | Opcode (16)   | Operation code (e.g., `0x000A` = ADD)                                |
| 32–63   | Reserved (32) | Reserved for future expansion                                        |
| 64-127 | Operand 1 (64) | First operand (e.g., source or destination register/memory address)  |
| 128-191 | Operand 2 (64) | Second operand (e.g., source or destination register/memory address)|
| 192-255 | Operand 3 (64) | Third operand (e.g., source or destination register/memory address) |

### Instruction opcodes

<!-- Miscellaneous instructions -->
- **NOP**: 0x0000 - No operation
- **MOV** SOURCE DEST: 0x0001 - Move value from source to destination
- **CMP** SOURCE_1 SOURCE_2: 0x0002 - Compare two values
- **HLT**: 0xFFFF - Halt execution (FFFF is used so iteration to test all instructions, this is last to run)

<!-- Jump instructions -->
- **JMP** (LABEL OR ADDRESS): 0x0003 - Jump to address
- **JZ** (LABEL OR ADDRESS): 0x0004 - Jump to address if zero
- **JNZ** (LABEL OR ADDRESS): 0x0005 - Jump to address if not zero
- **JL** (LABEL OR ADDRESS): 0x0006 - Jump to address if less than
- **JLE** (LABEL OR ADDRESS): 0x0007 - Jump to address if less than or equal
- **JG** (LABEL OR ADDRESS): 0x0008 - Jump to address if greater than
- **JGE** (LABEL OR ADDRESS): 0x0009 - Jump to address if greater than or equal

<!--  Arithmetic instructions -->
- **ADD** SOURCE_1 SOURCE_2 DEST: 0x000A - Add two values
- **SUB** SOURCE_1 SOURCE_2 DEST: 0x000B - Subtract two values
- **MUL** SOURCE_1 SOURCE_2 DEST: 0x000C - Multiply two values
- **DIV** SOURCE_1 SOURCE_2 DEST: 0x000D - Divide two values
- **INC** SOURCE: 0x000E - Increment value
- **DEC** SOURCE: 0x000F - Decrement value
- **NEG** SOURCE: 0x0010 - Negate value

<!-- Bitwise instructions -->
- **AND** SOURCE_1 SOURCE_2 DEST: 0x0011 - Bitwise AND two values
- **OR** SOURCE_1 SOURCE_2 DEST: 0x0012 - Bitwise OR two values
- **XOR** SOURCE_1 SOURCE_2 DEST: 0x0013 - Bitwise XOR two values
- **NOT** SOURCE: 0x0014 - Bitwise NOT value

<!-- Bitshift instructions -->
- **SHL** SOURCE DEST: 0x0015 - Shift left value
- **SHR** SOURCE DEST: 0x0016 - Shift right value
- **ROL** SOURCE DEST: 0x0017 - Rotate left value
- **ROR** SOURCE DEST: 0x0018 - Rotate right value
- **BSWAP** SOURCE: 0x0019 - Byte swap value

<!-- Interrupt instructions -->
- **INT** (NUMBER): 0x001A - Invoke an interrupt
- **IRET**: 0x001B - Return from interrupt

<!-- Stack instructions -->
- **PUSH** SOURCE: 0x001C - Push value onto stack
- **POP** DEST: 0x001D - Pop value from stack
- **CALL** (LABEL OR ADDRESS): 0x001E - Call subroutine
- **RET**: 0x001F - Return from subroutine


## Assembly syntax overview

Assembly `main` label must be included in the code segment else assembly will fail to compile.

```asm
; Viso-Fox Assembly Syntax
INSTRUCTION OPERAND_1, OPERAND_2, OPERAND_3
MOV SOURCE, DEST

label_declaration:
JMP label_declaration

; Comments start with a semicolon

INC [REGISTER] ; Increment the value pointed to by the register
INC 0xFF ; Increment the value at memory address 0xFF
INC REGISTER ; Increment the value in the register
```

Each assembly program is broken into two mandatory segments: `data` and `code`. and are defined as follows:

```asm
section data
; Data segment for variables and constants
section code
; Code segment for instructions
main:
; Main entry point of the program
```

### Defining data in assembly

As the CPU only supports 64 bit addressing, only 64 bit data types can be defined e.g.

```asm
section data
@real my_variable: 0x123456789ABCDEF0 ; Define a 64-bit variable
```

### Defining strings in assembly

Strings can be defined using the `@array_string` directive as such:

```asm
section data
@array_string my_string: "Hello, World!\n" ; Define a string
```

### Defining arrays in assembly

Arrays can be defined using the `@array` directive as such:

```asm
section data
@array my_array: 0x01, 0x02, 0x03, 0x04 ; Define an array of 64-bit values
```

### Types of data

Use [] for non-immediate values, i.e. values that are stored in memory or registers. Use immediate values without [].

<!-- Register -->
`[RX]` - Value at the memory address which is stored in RX.
`RX` - Value in the RX register.

<!-- Address -->
`[0xFF]` - Value at memory address 0xFF.
`0xFF` - Value 0xFF - immediate value.

<!-- Label -->
`[my_label]` - Value at the memory address of the label.
`my_label` - Value of the label - address in memory.

<!-- Variables -->
`[my_variable]` - Value at the memory address stored in my_variable.
`my_variable` - Value of the variable.
