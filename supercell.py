import os
import numpy as np

def read_poscar(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    title = lines[0].strip()
    scale_factor = float(lines[1].strip())
    lattice_vectors = np.array([list(map(float, lines[i].strip().split())) for i in range(2, 5)])
    elements = lines[5].strip().split()
    num_atoms = list(map(int, lines[6].strip().split()))
    coordinate_type = lines[7].strip().lower()
    coordinates = np.array([list(map(float, lines[i].strip().split()[:3])) for i in range(8, 8 + sum(num_atoms))])

    return title, scale_factor, lattice_vectors, elements, num_atoms, coordinate_type, coordinates

def write_poscar(file_path, title, scale_factor, lattice_vectors, elements, num_atoms, coordinate_type, coordinates):
    with open(file_path, 'w') as f:
        f.write(f"{title}\n")
        f.write(f"{scale_factor}\n")
        for vec in lattice_vectors:
            f.write("  {:.12f}  {:.12f}  {:.12f}\n".format(*vec))
        f.write("  " + "  ".join(elements) + "\n")
        f.write("  " + "  ".join(map(str, num_atoms)) + "\n")
        f.write(f"{coordinate_type}\n")
        for coord in coordinates:
            f.write("  {:.12f}  {:.12f}  {:.12f}\n".format(*coord))

def frac_to_cart(frac_coords, lattice_vectors):
    return np.dot(frac_coords, lattice_vectors)

def cart_to_frac(cart_coords, lattice_vectors):
    return np.dot(cart_coords, np.linalg.inv(lattice_vectors))

def expand_cell(lattice_vectors, coordinates, elements, num_atoms, expand_factors):
    new_lattice_vectors = np.array([expand_factors[i] * lattice_vectors[i] for i in range(3)])
    new_coordinates = []
    new_elements = []

    # Convert fractional coordinates to Cartesian coordinates
    cart_coords = frac_to_cart(coordinates, lattice_vectors)
    
    # Expanded coordinates and elements lists
    expanded_coordinates = {element: [] for element in elements}
    
    for i in range(expand_factors[0]):
        for j in range(expand_factors[1]):
            for k in range(expand_factors[2]):
                shift = np.array([i, j, k]) @ lattice_vectors
                for index, num in enumerate(num_atoms):
                    for atom_idx in range(num):
                        coord_idx = sum(num_atoms[:index]) + atom_idx
                        new_coord = cart_coords[coord_idx] + shift
                        expanded_coordinates[elements[index]].append(new_coord)

    # Convert expanded Cartesian coordinates back to fractional coordinates
    final_coordinates = []
    for element in elements:
        final_coordinates.extend(expanded_coordinates[element])
    final_coordinates = np.array(final_coordinates)
    new_frac_coords = cart_to_frac(final_coordinates, new_lattice_vectors)
    new_num_atoms = [n * np.prod(expand_factors) for n in num_atoms]

    return new_lattice_vectors, new_frac_coords, elements, new_num_atoms

def expand_poscars_in_directory(directory):
    # List all POSCAR files in the directory
    poscar_files = [f for f in os.listdir(directory) if f.startswith('POSCAR')]

    for poscar_file in poscar_files:
        input_path = os.path.join(directory, poscar_file)
        output_path = os.path.join(directory, poscar_file.split('.')[0] + '_expanded')

        # Perform expansion
        title, scale_factor, lattice_vectors, elements, num_atoms, coordinate_type, coordinates = read_poscar(input_path)
        
        a_len = np.linalg.norm(lattice_vectors[0])
        b_len = np.linalg.norm(lattice_vectors[1])
        c_len = np.linalg.norm(lattice_vectors[2])

        expand_factors = np.array([max(1, int(np.ceil(10 / a_len))),
                                   max(1, int(np.ceil(10 / b_len))),
                                   1])

        new_lattice_vectors, new_coordinates, new_elements, new_num_atoms = expand_cell(lattice_vectors, coordinates, elements, num_atoms, expand_factors)
        
        write_poscar(output_path, title + " expanded", scale_factor, new_lattice_vectors, new_elements, new_num_atoms, coordinate_type, new_coordinates)
        print(f"Expanded POSCAR saved to {output_path}")

# Specify the directory containing POSCAR files
directory = './'

# Run the expansion function for all POSCAR files in the directory
expand_poscars_in_directory(directory)
