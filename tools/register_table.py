"""Utility module for converting between binary register indices and names."""

# Register name lookup (lowercase keys)
REGISTER_LUT = {
    0x00: "R0",
    0x01: "R1",
    0x02: "R2",
    0x03: "R3",
    0x04: "R4",
    0x05: "R5",
    0x06: "R6",
    0x07: "R7",
    0x08: "FLAGS",
    0x09: "PC",
    0x0A: "SP",
    0x0B: "BP",
    0x0C: "IO",
    0x0D: "IVT"
}

# Reverse LUT for name-to-index
REVERSE_REGISTER_LUT = {v.lower(): k for k, v in REGISTER_LUT.items()}


def binary_to_register(index: int) -> str:
    """Convert register index (int) to its name (e.g. R0, SP, FLAGS)."""
    return REGISTER_LUT.get(index, f"unknown_{index:#04x}")


def register_to_binary(name: str) -> int:
    """Convert register name (case-insensitive) to numeric index."""
    return REVERSE_REGISTER_LUT.get(name.lower(), -1)
