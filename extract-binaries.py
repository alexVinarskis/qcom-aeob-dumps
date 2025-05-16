#!/usr/bin/python3

import os
import sys
import argparse
from pathlib import Path

# AeoB file header
MAGIC_HEADER = bytes.fromhex('41656f42')

def find_magic_offsets(data, magic):
    """Find all offsets where the magic header occurs."""
    offsets = []
    i = 0
    while True:
        i = data.find(magic, i)
        if i == -1:
            break
        offsets.append(i)
        i += len(magic)
    return offsets

def split_bin_file(bin_path, output_dir):
    with open(bin_path, 'rb') as f:
        data = f.read()

    offsets = find_magic_offsets(data, MAGIC_HEADER)

    if len(offsets) == 0:
        # Not all binaries are AeoB binaries
        return

    base_name = bin_path.stem
    extension = bin_path.suffix
    if len(offsets) == 1:
        # .bin only contains one AeoB, copy as is
        output_path = output_dir / bin_path.name
        with open(output_path, 'wb') as out:
            out.write(data)
        print(f"Found single AeoB in '{bin_path.name}'")
    else:
        # Multiple AeoBs in single .bin, split them
        for i in range(len(offsets)):
            start = offsets[i]
            end = offsets[i + 1] if i + 1 < len(offsets) else len(data)
            part_data = data[start:end]
            output_filename = f"{base_name}_part{i+1}.bin"
            output_path = output_dir / output_filename
            with open(output_path, 'wb') as out:
                out.write(part_data)
        print(f"Found x{i+1} AeoB(s) in '{base_name}.bin'")

def process_directory(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.bin'):
                bin_path = Path(root) / file
                split_bin_file(bin_path, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Find and extract AeoB binaries. If concatenated into single .bin, split by magic header.")
    parser.add_argument("input_dir", help="Directory to search for .bin files")
    parser.add_argument("output_dir", help="Directory to store split .bin files")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    process_directory(input_dir, output_dir)

if __name__ == "__main__":
    main()
