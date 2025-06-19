"""Utility functions and disassembler for VFOX ROM files."""

import argparse
import sys

from io import BufferedReader, BufferedWriter
from typing import Dict, List, NamedTuple
import random

from register_table import REGISTER_LUT, binary_to_register
from addressing_table import ADDRESSING_MODE_LUT, code_to_addressing_mode
from opcode_table import OPCODE_LUT, binary_to_opcode

# Version of the disassembler
VERSION = "1.0.0"

class ROMHeader (NamedTuple):
    """A simple ROM header structure."""
    magic_number: bytes  # 4 bytes
    version: int         # 4 bytes
    data_start: int      # 8 bytes
    code_start: int      # 8 bytes

def show_help() -> None:
    """Display the help message for the disassembler utility."""
    print("""
Usage: disassembler <command> [arguments]

Commands:
\t--create-dummy <out.bin>       Create a dummy ROM file with random data (not a valid ROM).
\t--debug <out.bin>              Show debug view of a ROM file.
\t--disassembly <source> <out>   Generate an assembly file from a ROM (no labels except main).
\t--version                      Show version number.
\t--help                         Show this help message.

Examples:
\tdisassembler --create-dummy test.bin
\tdisassembler --debug test.bin
\tdisassembler --disassembly test.bin out.asm
""")

def main() -> None:
    """Main function to parse arguments and execute commands."""
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--create-dummy', nargs=1)
    parser.add_argument('--debug', nargs=1)
    parser.add_argument('--disassembly', nargs=2)
    parser.add_argument('--version', action='store_true')
    parser.add_argument('--help', action='store_true')

    if len(sys.argv) == 1:
        print("No arguments provided.\n")
        print("Usage: disassembler --help for details.")
        sys.exit(1)

    args = parser.parse_args()

    if args.help:
        show_help()
    elif args.version:
        print(f"disassembler version {VERSION}")
    elif args.create_dummy:
        create_dummy_rom(args.create_dummy[0])
    elif args.debug:
        debug_read_rom(args.debug[0])
    elif args.disassembly:
        # raise NotImplementedError("Disassembly functionality is not implemented yet.")
        source, output = args.disassembly
        disassemble_rom(source, output)
    else:
        print("Invalid command. Use --help to see usage.")
        sys.exit(1)

def write_rom_header(file: BufferedWriter, data_start: int, code_start: int) -> None:
    """Write the ROM header to the file."""

    # Write magic number "VFOX"
    file.write(b"VFOX")  # 4 bytes

    # Write 8 byte long version number 0x01
    file.write((0x01).to_bytes(4, byteorder='little'))  # 4 bytes

    # Write section data start
    file.write(data_start.to_bytes(8, byteorder='little'))  # 8 bytes

    # Write section code start
    file.write(code_start.to_bytes(8, byteorder='little'))  # 8 bytes

def read_rom_header(file: BufferedReader) -> ROMHeader:
    """Read the ROM header from the file and return section start addresses."""

    # Read magic number
    magic_number = file.read(4)
    if magic_number != b"VFOX":
        raise ValueError("Invalid ROM magic number. Expected 'VFOX'.")

    # Read version number
    version = int.from_bytes(file.read(4), 'little')

    # Read section data start
    data_start = int.from_bytes(file.read(8), 'little')

    # Read section code start
    code_start = int.from_bytes(file.read(8), 'little')

    return ROMHeader(magic_number, version, data_start, code_start)

def create_dummy_pack(instruction: int) -> List[int]:
    """Create dummy operands for the dummy instruction."""
    dummy_pack: List[int] = [instruction]

    # Get the number of operands from the instruction
    operand_count = (instruction >> 20) & 0xF

    # Get the modes for each operand
    mode1 = (instruction >> 24) & 0xF if operand_count > 0 else 0
    mode2 = (instruction >> 28) & 0xF if operand_count > 1 else 0
    mode3 = (instruction >> 32) & 0xF if operand_count > 2 else 0

    modes = [mode1, mode2, mode3]

    # Generate dummy operands based on the modes
    for i in range(operand_count):
        # Check for IMM
        if modes[i] == 0x1:
            dummy_pack.append(random.randint(0, 0xFFFFFFFF))
        # Check for REG
        if modes[i] == 0x2:
            dummy_pack.append(random.choice(list(REGISTER_LUT.keys())))
        # Check for MEM
        if modes[i] == 0x3:
            dummy_pack.append(random.randint(0, 0xFFFFFFFF))
        # Check for IND
        if modes[i] == 0x4:
            dummy_pack.append(random.choice(list(REGISTER_LUT.keys())))
        # Check for PORT
        if modes[i] == 0x5:
            dummy_pack.append(random.randint(0, 16))

    return dummy_pack

def get_instruction_operand_count(instruction: int) -> int:
    """Get the number of operands for a given instruction."""
    return (instruction >> 20) & 0xF

def create_dummy_instruction() -> int:
    """Create a dummy instruction for testing purposes."""
    designation: int = 0xF  # Instruction prefix

    # Random opcode
    opcode: int = random.choice(list(OPCODE_LUT.keys()))

    # Random operand count (0-3)
    operand_count = random.randint(0, 3)

    # Random addressing modes for operands
    mode1: int = random.choice(list(ADDRESSING_MODE_LUT.keys())) if operand_count > 0 else 0
    mode2: int = random.choice(list(ADDRESSING_MODE_LUT.keys())) if operand_count > 1 else 0
    mode3: int = random.choice(list(ADDRESSING_MODE_LUT.keys())) if operand_count > 2 else 0

    # Check none are zero if operand count is greater than 0
    if operand_count > 0:
        if mode1 == 0: # If mode1 is zero, set it to IMM
            mode1 = 0x1
        if operand_count > 1 and mode2 == 0:
            mode2 = 0x1
        if operand_count > 2 and mode3 == 0:
            mode3 = 0x1

    reserved: int = 0  # Reserved bits

    return (
    (designation & 0xF) |
    ((opcode & 0xFFFF) << 4) |
    ((operand_count & 0xF) << 20) |
    ((mode1 & 0xF) << 24) |
    ((mode2 & 0xF) << 28) |
    ((mode3 & 0xF) << 32) |
    ((reserved & 0xFFFFFFF) << 36)
    )

def decode_instruction(instruction: int) -> Dict[str, int]:
    """
    Decode a 64-bit instruction into its individual components.

    Args:
        instruction (int): The encoded 64-bit instruction.

    Returns:
        dict: A dictionary with decoded fields:
            - designation (int)
            - opcode (int)
            - operand_count (int)
            - mode1 (int)
            - mode2 (int)
            - mode3 (int)
            - reserved (int)
    """

    designation    = instruction & 0xF                  # bits 0–3
    opcode         = (instruction >> 4) & 0xFFFF         # bits 4–19 (16 bits)
    operand_count  = (instruction >> 20) & 0xF           # bits 20–23
    mode1          = (instruction >> 24) & 0xF           # bits 24–27
    mode2          = (instruction >> 28) & 0xF           # bits 28–31
    mode3          = (instruction >> 32) & 0xF           # bits 32–35
    reserved       = (instruction >> 36) & 0xFFFFFFF     # bits 36–63 (28 bits)

    return {
        "DESIGNATION": designation,
        "OPCODE": opcode,
        "OPERAND_COUNT": operand_count,
        "MODE1": mode1,
        "MODE2": mode2,
        "MODE3": mode3,
        "RESERVED": reserved
    }

def create_dummy_data_section(length: int) -> List[int]:
    """Create a dummy data section with random values."""
    return [random.randint(0, 0xFFFFFFFF) for _ in range(length)]

def write_rom(data_section: List[int], code_packs: List[List[int]], filename: str) -> None:
    """Write the ROM data and instruction packs to a file."""
    with open(filename, 'wb') as f:
        # Offset after the header
        offset_bytes: int = 4 + 4 + 8 + 8

        # Data offset
        data_start: int = offset_bytes

        # Code offset
        code_start: int = data_start + (len(data_section) * 8)

        # Write the ROM header
        write_rom_header(f, data_start, code_start)

        # Write data section
        for value in data_section:
            f.write(value.to_bytes(8, byteorder='little'))

        # Write instruction packs
        for pack in code_packs:
            for value in pack:
                f.write(value.to_bytes(8, byteorder='little'))

def create_dummy_rom(filename: str) -> None:
    """Create a dummy ROM file with random data and instructions."""
    # Create a data section
    data_section_length = random.randint(5, 15)  # Random length between 5 and 15

    # Create a list of dummy instructions
    instructions = [create_dummy_instruction() for _ in range(random.randint(10, 20))]

    # Print the number of instructions
    print(f"Number of instructions: {len(instructions)}")
    # Print the data section length
    print(f"Data section length: {data_section_length}")

    # Create dummy instruction packs
    instruction_packs = [create_dummy_pack(instruction) for instruction in instructions]

    # Write the ROM file
    write_rom(create_dummy_data_section(data_section_length), instruction_packs, filename)
    print(f"Dummy ROM file '{filename}' created successfully.")


class PackedInstruction(NamedTuple):
    """A simple instruction structure."""
    instruction: int
    operands: List[int]

def convert_to_instructions(code_section: List[int]) -> List[PackedInstruction]:
    """Convert a list of 64-bit instructions into PackedInstructions."""

    entries: List[PackedInstruction] = []
    current_entry: int = 0

    while current_entry < len(code_section):
        current_instruction: int = code_section[current_entry]
        operand_count = get_instruction_operand_count(current_instruction)
        operands: List[int] = []
        for i in range(1, operand_count + 1):
            operands.append(code_section[current_entry + i])
        entries.append(PackedInstruction(current_instruction, operands))

        current_entry += (operand_count + 1)  # Move to the next instruction

    return entries

def debug_read_rom(filename: str) -> None:
    """Read and print the ROM header and contents for debugging."""

    # Check if the file exists
    try:
        with open(filename, 'rb') as f:
            pass
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    with open(filename, 'rb') as f:
        header = read_rom_header(f)
        print("---- ROM Header ----")
        print(f"Magic Number: {header.magic_number.decode('ascii')}")
        print(f"Version: {header.version}")
        print(f"Data Start: {header.data_start:#x}")
        print(f"Code Start: {header.code_start:#x}")
        print("---- End of ROM Header ----")

        # Data section
        print("---- Data Section ----")
        f.seek(header.data_start)
        data_section: List[int] = []

        # Read until we reach the code section
        address: int = 0
        while f.tell() < header.code_start:
            data_value = int.from_bytes(f.read(8), 'little')
            data_section.append(data_value)
            print(f"${address:#x}: {data_value:#x} ({data_value})")
            address += 1
        print("---- End of Data Section ----")

        # Code section
        print("---- Code Section ----")
        f.seek(header.code_start)

        code_section: List[int] = []

        # Load the code section until EOF
        while True:
            code_bytes = f.read(8)
            if not code_bytes:
                break
            code_section.append(int.from_bytes(code_bytes, 'little'))

        # Convert code section to instructions
        packs: List[PackedInstruction] = convert_to_instructions(code_section)

        for i, pack in enumerate(packs):
            decoded = decode_instruction(pack.instruction)

            # Decode the opcode and addressing modes
            opcode_str = binary_to_opcode(decoded['OPCODE'])
            mode1 = decoded['MODE1']
            mode2 = decoded['MODE2']
            mode3 = decoded['MODE3']
            modes = [mode1, mode2, mode3]

            # Format operands based on their addressing modes
            formatted_operands: List[str] = []
            for idx in range(decoded["OPERAND_COUNT"]):
                operand = pack.operands[idx]
                mode = modes[idx]

                if code_to_addressing_mode(mode) == "REG":
                    formatted = binary_to_register(operand)
                elif code_to_addressing_mode(mode) == "IND":
                    formatted = f"[{binary_to_register(operand)}]"
                elif code_to_addressing_mode(mode) == "MEM":
                    formatted = f"[{operand:#x}]"
                elif code_to_addressing_mode(mode) == "IMM":
                    formatted = f"#{operand:#x}"
                elif code_to_addressing_mode(mode) == "PORT":
                    formatted = f"PORT_{operand}"
                else:
                    formatted = f"{operand:#x}"

                formatted_operands.append(formatted)

            # Final printout
            print(
                f"{i:#x}: {opcode_str} "
                f"({code_to_addressing_mode(mode1)} ",
                f"{code_to_addressing_mode(mode2)} ",
                f"{code_to_addressing_mode(mode3)}) "
                f"Operands ({decoded['OPERAND_COUNT']}): {', '.join(formatted_operands)}"
            )

        print("---- End of Code Section ----")

def disassemble_rom(source_file: str, output_file: str) -> None:
    """Disassemble a ROM file into assembly source code."""

    entry_point: str = "_start_of_assembly_"

    # Check if the file exists
    try:
        with open(source_file, 'rb') as f:
            pass
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
        sys.exit(1)

    with open(source_file, 'rb') as f:
        header = read_rom_header(f)

        # Read data section
        data_section: List[int] = []
        f.seek(header.data_start)
        while f.tell() < header.code_start:
            raw = f.read(8)
            if not raw:
                break
            value = int.from_bytes(raw, 'little')
            data_section.append(value)

        # Read code section
        f.seek(header.code_start)
        code_section: List[int] = []
        while True:
            chunk = f.read(8)
            if not chunk:
                break
            code_section.append(int.from_bytes(chunk, 'little'))

    # Decode code instructions
    instructions: List[PackedInstruction] = convert_to_instructions(code_section)

    # ---- Write Disassembled Output ----
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"; Disassembly of ROM file: {source_file}\n")
        out.write(f"; ROM format version: {header.version}\n")
        out.write(f"; Generated by disassembler version {VERSION}\n")
        out.write("\n")

        # Caveat
        out.write("; Note: Disassembly does not include labels except for the main entry point.\n")
        out.write("; Label addresses likely to be inaccurate and will require manual adjustment.\n")
        out.write("\n")

        # Write meta section
        out.write("section meta\n")
        out.write(f"@meta version: {header.version}.0\n")
        out.write(f"@meta entry: {entry_point}\n")
        out.write("\n")

        # Write data section
        out.write("section data\n")
        count: int = 0
        for value in data_section:
            out.write(f"@real reconstructed_data_{count} {value}\n")
            count += 1
        out.write("\n")

        # Write code section
        out.write("section code\n")
        out.write(f"{entry_point}:\n")

        for _, pack in enumerate(instructions):
            decoded = decode_instruction(pack.instruction)
            opcode = binary_to_opcode(decoded["OPCODE"])
            operand_count = decoded["OPERAND_COUNT"]
            modes = [decoded["MODE1"], decoded["MODE2"], decoded["MODE3"]]

            operands_text: List[str] = []
            for j in range(operand_count):
                operand = pack.operands[j]
                mode = modes[j]
                mode_str = code_to_addressing_mode(mode)

                if mode_str == "REG":
                    operand_str = binary_to_register(operand)
                elif mode_str == "IND":
                    operand_str = f"[{binary_to_register(operand)}]"
                elif mode_str == "MEM":
                    operand_str = f"[0x{operand:X}]"
                elif mode_str == "IMM":
                    operand_str = f"#{hex(operand)}"
                elif mode_str == "PORT":
                    operand_str = f"0x{operand:X}"
                else:
                    operand_str = f"0x{operand:X}"

                operands_text.append(operand_str)

            if operands_text:
                out.write(f"\t{opcode} {', '.join(operands_text)}\n")
            else:
                out.write(f"\t{opcode}\n")

    print(f"Disassembly written to '{output_file}'.")


# Test read utility
if __name__ == "__main__":
    main()
