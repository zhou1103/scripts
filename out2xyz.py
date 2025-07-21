#!/usr/bin/env python

import ase
from ase.io import read,write

def convert_optout(input_file="OUTCAR"):
    try:
        atoms = read(input_file, index=":")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    output_file = f"opt.xyz"
    write(output_file, atoms, format="extxyz")

if __name__ == "__main__":
    convert_optout()
