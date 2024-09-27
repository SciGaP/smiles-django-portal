import os
import csv
import json
import base64

data_file = 'sample-data/data.txt'
coordinates_dir = 'sample-data/coordinates'
output_file = 'data.json'

records = []

with open(data_file, 'r', newline='', encoding='utf-8') as csvfile_in:
    reader = csv.DictReader(csvfile_in)
    for row in reader:
        index = row['Index'].strip()
        record = {
            'data_product_id': f'comp_{index}',
            'name': index,
            'calculated_properties': {},
            'final_molecule_structural_formats': {
                'optimized_geometries': []
            }
        }

        property_mapping = {
            'Experimental Absorption max (eV)': 'experimental_absorption_max',
            'IMOM Absorption (eV)': 'imom_absorption',
            'SC-IMOM Absorption (eV)': 'sc_imom_absorption',
            'TDDFT Absorption (eV)': 'tddft_absorption',
            'TDDFT Absorption S2 (eV)': 'tddft_absorption_s2',
            'Experimental Emission max (eV)': 'experimental_emission_max',
            'SC-IMOM Emission (eV)': 'sc_imom_emission',
            'TDDFT Emission (eV)': 'tddft_emission'
        }

        for csv_field, proto_field in property_mapping.items():
            value_str = row.get(csv_field, '').strip()
            if value_str:
                try:
                    value = float(value_str)
                    record['calculated_properties'][proto_field] = {
                        'value': value,
                        'unit': 'eV'
                    }
                except ValueError:
                    pass

        geometry_types = ['ground_state_geometry', 'IMOM_geometry', 'TDDFT_geometry']
        for geometry_type in geometry_types:
            geometry_dir = os.path.join(coordinates_dir, geometry_type)
            for dye_family in os.listdir(geometry_dir):
                dye_family_dir = os.path.join(geometry_dir, dye_family)
                xyz_file_path = os.path.join(dye_family_dir, f'{index}.xyz')

                if os.path.isfile(xyz_file_path):
                    try:
                        with open(xyz_file_path, 'rb') as xyz_file:
                            xyz_bytes = xyz_file.read()
                            xyz_base64 = base64.b64encode(xyz_bytes).decode('utf-8')
                            record['final_molecule_structural_formats']['optimized_geometries'].append({
                                'xyz': xyz_base64,
                                'type': geometry_type
                            })
                    except Exception:
                        pass

        records.append(record)

with open(output_file, 'w', encoding='utf-8') as jsonfile:
    json.dump(records, jsonfile, ensure_ascii=False, indent=2)

print(f"Data processing complete. JSON output saved as {output_file}.")
