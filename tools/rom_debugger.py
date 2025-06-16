"""
    Display the ROM information:
        - Show the header information
        - Data section
        - Code section with instructions
"""

# Dictionary lookup for read/write modes
from typing import Tuple


READ_WRITE_MODES = {
    0b0000: "register",     # Register access
    0b0001: "memory",       # Memory address (indirect access)
    0b0010: "immediate"     # Immediate value
}

# Opcode lookup for instruction designations
OPCODE_LOOKUP = {
    # Miscellaneous instructions
    0x0: "NOP",
    0x1: "MOV",
    0x2: "CMP",
    0xFFFF: "HLT",
    # Branching instructions
    0x3: "JMP",
    0x4: "JZ",
    0x5: "JNZ",
    0x6: "JL",
    0x7: "JLE",
    0x8: "JG",
    0x9: "JGE",
    # Arithmetic instructions
    0xA: "ADD",
    0xB: "SUB",
    0xC: "MUL",
    0xD: "DIV",
    0xE: "INC",
    0xF: "DEC",
    0x10: "NEG",
    # Logical instructions
    0x11: "AND",
    0x12: "OR",
    0x13: "XOR",
    0x14: "NOT",
    # Bitwise instructions
    0x15: "SHL",
    0x16: "SHR",
    0x17: "ROL",
    0x18: "ROR",
    0x19: "BSWAP",
    # Interrupt instructions
    0x1A: "INT",
    0x1B: "IRET",
    # Stack instructions
    0x1C: "PUSH",
    0x1D: "POP",
    0x1E: "CALL",
    0x1F: "RET"
}

# Constants
HEADER_REQUIRED_SIZE = 24  # Minimum size for the ROM header

def print_instruction_unit_details(opcode: int) -> None:
    """Print instruction unit details

    Args:
        opcode (int): instruction (bytes)
    """
    instruction_designation = (opcode >> 0) & 0xF
    operand_count = (opcode >> 4) & 0xF
    read_mode = (opcode >> 8) & 0xF
    write_mode = (opcode >> 12) & 0xF
    opcode_value = (opcode >> 16) & 0xFFFF

    # Check if instruction designation is valid else likely an operand (some ambiguity is possible)
    if instruction_designation == 0xF:
        print(f"{OPCODE_LOOKUP.get(opcode_value, 'unknown')} (R: {READ_WRITE_MODES.get(read_mode, 'unknown')}, W: {READ_WRITE_MODES.get(write_mode, 'unknown')}, OP: {operand_count})")
    else:
        print(f"{opcode_value:#06x} (likely operand)")

def extract_rom_header(data: bytes) -> Tuple[int, int]:
    """
    Extract header information from the ROM data.
    
    Args:
        data (bytes): The ROM data.
    Returns:
        Tuple[int, int]: The header information (start of data section, start of code section).
    """

    if len(data) < HEADER_REQUIRED_SIZE:
        print("ROM data is too small to contain a valid header.")
        return 0, 0

    # Extract the magic number
    magic_number_bytes = data[0:4]
    if magic_number_bytes != b"VFOX":
        print("Invalid ROM magic number. Expected 'VFOX'.")
        return 0, 0

    # Extract the version
    version = int.from_bytes(data[4:8], 'little')

    # Extract the start of data section and code section
    start_data = int.from_bytes(data[8:16], 'little')
    start_code = int.from_bytes(data[16:24], 'little')

    # Display header information
    print("ROM Header:")
    print(f" - Magic Number: {magic_number_bytes.decode('utf-8')}")
    print(f" - Version: {version}")
    print(f" - Start of Data Section: {start_data:#010x}")
    print(f" - Start of Code Section: {start_code:#010x}")

    # Return the start addresses of data and code sections
    return start_data, start_code


def extract_data_section(data: bytes, start_data: int, start_code: int) -> None:
    """
    Extract the data section from the ROM data.
    
    Args:
        data (bytes): The ROM data.
        start_data (int): The start address of the data section.
        start_code (int): The start address of the code section.
    Returns:
        bytes: The extracted data section.
    """

    # Print data section
    print("Data:")
    for i in range(start_data, start_code, 8):
        print(f"{(i - start_data):08x}: {data[i:i+8].hex()}")

def extract_code_section(data: bytes, start_code: int) -> None:
    """
    Extract the code section from the ROM data.
    
    Args:
        data (bytes): The ROM data.
        start_code_section (int): The start address of the code section.
    Returns:
        bytes: The extracted code section.
    """

    # Iterate over all code starting from start_code_section
    code_section = data[start_code:]

    # Display the code section
    print("Code Section:")
    for i in range(0, len(code_section), 8):
        print(f"{(i):08x}: {code_section[i:i+8].hex()}", end=' ')
        print_instruction_unit_details(int.from_bytes(code_section[i:i+8], 'little'))
# Main
if __name__ == "__main__":
    # Check if one argument is provided
    import sys
    if len(sys.argv) != 2:
        print("Usage: python rom_debugger.py <rom_file>")
        sys.exit(1)

    # Check if the file exists
    rom_file = sys.argv[1]
    try:
        with open(rom_file, "rb") as f:
            rom_data = f.read()
    except FileNotFoundError:
        print(f"File '{rom_file}' not found.")
        sys.exit(1)

    # Extract and display the ROM header
    start_data_section, start_code_section = extract_rom_header(rom_data)

    # Data section extraction
    extract_data_section(rom_data, start_data_section, start_code_section)

    # Code section extraction
    extract_code_section(rom_data, start_code_section)
