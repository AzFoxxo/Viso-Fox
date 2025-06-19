"""Utility module for converting between binary addressing modes and mnemonics."""

# Addressing Mode LUT (Capitalized)
ADDRESSING_MODE_LUT = {
    0x0: "NULL",  # Zero addressing (debug/no-op)
    0x1: "IMM",   # Immediate
    0x2: "REG",   # Register
    0x3: "MEM",   # Direct Memory
    0x4: "IND",   # Indirect Memory
    0x5: "PORT"   # I/O Port
}

# Reverse LUT (Mnemonic → Code)
REVERSE_ADDRESSING_MODE_LUT = {v: k for k, v in ADDRESSING_MODE_LUT.items()}

def code_to_addressing_mode(code: int) -> str:
    """
    Convert addressing mode code (int) to mnemonic (str).
    
    Args:
        code (int): Addressing mode code (0x0–0x5)
    Returns:
        str: Addressing mode mnemonic (e.g., "IMM", "PORT")
    """
    return ADDRESSING_MODE_LUT.get(code, f"UNKNOWN_{code:#04x}")

def addressing_mode_to_code(name: str) -> int:
    """
    Convert addressing mode mnemonic (str) to code (int).
    
    Args:
        name (str): Addressing mode mnemonic (case-insensitive)
    Returns:
        int: Corresponding code (0–5), or -1 if not found
    """
    return REVERSE_ADDRESSING_MODE_LUT.get(name.upper(), -1)
