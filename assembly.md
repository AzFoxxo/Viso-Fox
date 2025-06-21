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
`@meta replace: old_string new_string` - Defines a string replacement directive that replaces all occurrences of `old_string` with `new_string` in the assembly code. This is useful for macros or aliases. old_string and new_string can be any valid string, including labels, variables, or constant but must not contain spaces. This directive is processed before the assembly code is compiled.

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
| `[%R1]`          | Value at the memory address stored in register `R1`                   |
| `%R1`            | Value stored in register `R1`                                         |
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
    mov my_variable, %R1  ; Move the value of my_variable into R1
    add %R1, 10, R2       ; Add 10 to R1 and store the result in R2
    out %R1, 0x04         ; Output the value of R1 to I/O port 0x04
    hlt                  ; Halt execution
```

## String literals

Viso-Fox assembly supports string literals in the data segment or single character strings as immediate values. Single characters are stored with `@real "A"` syntax, while strings can be defined using `@array` directive. Strings do not hold their length so it is recommended to use null-terminated strings for easier handling.

### Special characters in strings

A string bound is denoted by anything between double quotes `"`.

Say you want want to include a double quote or any other special characters (`DQUOTE`, `TAB`, `NULL` or `NL`), you exit the string and add to the list e.g.
`"My string", NULL` will create a string of `My string` and append the ASCII code for for null terminated string.

## Built-in constants

Viso-Fox assembly provides a number of built-in constants that can be used in the assembly code. These constants are predefined values that represent common values or registers in the architecture. They can be used directly in the code without needing to define them explicitly.

It is possible to define your own compile-time constants using the `@meta replace` directive, but built-in constants are always available.

List of built-in constants:

| Constant  | Value | Description                                    |
| --------- | ----- | ---------------------------------------------- |
| `TRUE`    | 1     | Boolean true value                             |
| `FALSE`   | 0     | Boolean false value                            |
| `NULL`    | 0x0   | Null pointer value                             |
| `R0`      | 0x0   | General-purpose register 0                     |
| `R1`      | 0x1   | General-purpose register 1                     |
| `R2`      | 0x2   | General-purpose register 2                     |
| `R3`      | 0x3   | General-purpose register 3                     |
| `R4`      | 0x4   | General-purpose register 4                     |
| `R5`      | 0x5   | General-purpose register 5                     |
| `R6`      | 0x6   | General-purpose register 6                     |
| `R7`      | 0x7   | General-purpose register 7                     |
| `FLAGS`   | 0x8   | Flags register (status flags)                  |
| `PC`      | 0x9   | Program Counter register (instruction pointer) |
| `SP`      | 0xA   | Stack Pointer register                         |
| `BP`      | 0xB   | Base Pointer register                          |
| `IO`      | 0xC   | I/O port register                              |
| `IVT`     | 0xD   | Interrupt Vector Table register                |
| `PORT_0`  | 0x0   | I/O port 0                                     |
| `PORT_1`  | 0x1   | I/O port 1                                     |
| `PORT_2`  | 0x2   | I/O port 2                                     |
| `PORT_3`  | 0x3   | I/O port 3                                     |
| `PORT_4`  | 0x4   | I/O port 4                                     |
| `PORT_5`  | 0x5   | I/O port 5                                     |
| `PORT_6`  | 0x6   | I/O port 6                                     |
| `PORT_7`  | 0x7   | I/O port 7                                     |
| `PORT_8`  | 0x8   | I/O port 8                                     |
| `PORT_9`  | 0x9   | I/O port 9                                     |
| `PORT_10` | 0xA   | I/O port A                                     |
| `PORT_11` | 0xB   | I/O port B                                     |
| `PORT_12` | 0xC   | I/O port C                                     |
| `PORT_13` | 0xD   | I/O port D                                     |
| `PORT_14` | 0xE   | I/O port E                                     |
| `PORT_15` | 0xF   | I/O port F                                     |
| `NL`      | 13    | Newline ASCII value                            |
| `NULL`    | 0     | Null terminator ASCII value                    |
| `TAB`     | 9     | Tab ASCII value                                |
| `DQUOTE`  | 34    | Double-quote ASCII VALUE                       |
