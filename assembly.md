# Assembly syntax overview

This section describes the Viso-Fox assembly standard syntax used for the Viso-Fox architecture. The assembly syntax is designed to be simple and easy to read.

The assembly is case sensitive and requires all opcodes to use lowercase only e.g. `nop` and registers to use uppercase only `R1`, `R2`, etc. Labels and variables can use both uppercase and lowercase and underscores and after the first character, numbers. Convention is to use lowercase with underscores for labels and variables, and uppercase constants.

Each assembly file is composed of three segments:

- `meta` segment: Contains metadata about the assembly file.
- `data` segment: Contains variables and constants.
- `code` segment: Contains the instructions to be executed.

## Meta segment

The meta segment contains @meta directives which define required assembly version and other metadata. It is optional but recommended to include it for clarity. It is defined using the `section meta` directive.

Meta directives are more for future proofing and are currently limited in use.

### Meta Directives

`@meta version: 1.0` - Defines the minimum version of the assembly syntax required to run the code.
`@meta entry main` - Defines the entry point of the assembly program, which is the main function that will be executed when the program starts. (default is `main`)

## Data segment

The data segment is used to define variables, constants, and other data that the program will use. It is defined using the `section data` directive.

### Data Directives

`@real` - Defines a 64-bit real number variable including characters using their corresponding ASCII values.
`@array` - Defines an array of 64-bit values. You may use an ASCII string e.g. "Hello, World!\n" too (null terminated is recommended amd each character is 64 bits).

## Code segment

The code segment contains the instructions that the CPU will execute. It is defined using the `section code` directive. The main entry point of the program is defined using the `main:` label unless specified in the meta section.

Each instruction is written in the format `opcode` `operand1, operand2, operand3`. It follows source-destination format where the first operand is the source and the second operand is the destination. If a third operand is specified, it is used as an additional source or destination depending on the instruction. In some cases, the destination operand can be omitted, in which case the first source operand is used as the destination.

## Addressing mode syntax

Operands can be specified in various addressing modes. The syntax for each addressing mode is as follows:

Use [] for non-immediate values, i.e. values that are stored in memory or registers. Use immediate values without []. Use @ for shadow registers.

| Syntax          | Description                                                           |
| --------------- | --------------------------------------------------------------------- |
| `[R1]`          | Value at the memory address stored in register `R1`                   |
| `R1`            | Value stored in register `R1`                                         |
| `[0xFF]`        | Value at memory address `0xFF`                                        |
| `0xFF`          | Immediate value `0xFF`                                                |
| `[my_label]`    | Value at the memory address of the label `my_label`                   |
| `my_label`      | Value of the label — address in memory                                |
| `[my_variable]` | Value at the memory address stored in the variable `my_variable`      |
| `my_variable`   | Value of the variable (i.e., its memory address or assigned constant) |
| `#0X10`         | Immediate value `0x10` (hexadecimal)                                  |

## Labels

Labels are defined in the code segment to mark specific locations in the code. They are defined using the `label:` syntax. Labels can be used as jump targets or to reference memory addresses.

## Comments

Comments are denoted by the `;` at the start or end of a line.

## Example assembly code

```assembly
section meta
@meta version: 1.0
@meta entry: main

section data
@real my_variable: "A"   ; Define a real variable with ASCII value of 'A'

section code
main:
    mov my_variable, R1  ; Move the value of my_variable into R1
    add R1, 10, R2       ; Add 10 to R1 and store the result in R2
    out R1, 0x04         ; Output the value of R1 to I/O port 0x04
    hlt                  ; Halt execution
```
