#!/ousr/bin/env python

import ase
from ase.io.vasp import read_vasp_out
from ase.io.extxyz import write_extxyz

def convert_optout(input_file="OUTCAR"):
    try:
        atoms = read_vasp_out(input_file, index=":")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    output_file = f"opt.extxyz"
    write_extxyz(output_file, atoms)

if __name__ == "__main__":
    convert_optout()
