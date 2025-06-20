section meta
@meta version: 1.0
@meta entry: main

section data
@real my_variable: "A"   ; Define a real variable with ASCII value of 'A'

section code
main:
    mov my_variable, %R1  ; Move the value of my_variable into R1
    out %R1, 0x04         ; Output the value of R1 to I/O port 0x04
    hlt                  ; Halt execution