#!/usr/bin/env python3

from ase.io import write
from ase.cluster import wulff_construction as wc

surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
esurf = [1.0, 1.1, 0.9]
lc = 3.61
size = 1000
atoms = wc('Cu', surfaces, esurf, size,
           'fcc', rounding='closest', latticeconstant=lc)
write('Cu.xyz', atoms)
