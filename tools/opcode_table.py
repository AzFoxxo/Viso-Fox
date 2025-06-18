"""Utility module for converting between binary opcodes and mnemonics."""

# Lowercase opcode lookup
OPCODE_LUT = {
    0x0000: "nop",
    0x0001: "mov",
    0x0002: "cmp",
    0xFFFF: "hlt",

    # Control flow
    0x0003: "jmp",
    0x0004: "jz",
    0x0005: "jnz",
    0x0006: "jl",
    0x0007: "jle",
    0x0008: "jg",
    0x0009: "jge",

    # Arithmetic
    0x000A: "add",
    0x000B: "sub",
    0x000C: "mul",
    0x000D: "div",
    0x000E: "inc",
    0x000F: "dec",
    0x0010: "neg",

    # Bitwise
    0x0011: "and",
    0x0012: "or",
    0x0013: "xor",
    0x0014: "not",

    # Shift / Rotate
    0x0015: "shl",
    0x0016: "shr",
    0x0017: "rol",
    0x0018: "ror",
    0x0019: "bswap",

    # Interrupt
    0x001A: "int",
    0x001B: "iret",

    # Stack
    0x001C: "push",
    0x001D: "pop",
    0x001E: "call",
    0x001F: "ret",

    # I/O
    0x0020: "in",
    0x0021: "out"
}

# Reverse mapping: mnemonic -> binary
MNEMONIC_LUT = {v: k for k, v in OPCODE_LUT.items()}


def binary_to_opcode(binary: int) -> str:
    """Convert a 16-bit binary opcode to a lowercase mnemonic."""
    return OPCODE_LUT.get(binary, f"unknown_{binary:#06x}")


def opcode_to_binary(mnemonic: str) -> int:
    """Convert a lowercase mnemonic to its corresponding 16-bit binary opcode."""
    return MNEMONIC_LUT.get(mnemonic.lower(), -1)
