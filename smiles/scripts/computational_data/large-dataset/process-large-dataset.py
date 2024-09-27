import os
import csv
import json
import base64

data_file = 'sample-data/data.txt'
coordinates_dir = 'sample-data/coordinates'
dye_family_dir = 'sample-data/dye_family'
output_file = 'data.json'

index_to_dye_family = {}

for dye_family_file in os.listdir(dye_family_dir):
    if dye_family_file.endswith('.txt'):
        dye_family_name = os.path.splitext(dye_family_file)[0]
        dye_family_path = os.path.join(dye_family_dir, dye_family_file)
        with open(dye_family_path, 'r') as f:
            indices = f.read().splitlines()
            for idx in indices:
                index_to_dye_family[idx.strip()] = dye_family_name

records = []

with open(data_file, 'r', newline='', encoding='utf-8') as csvfile_in:
    reader = csv.DictReader(csvfile_in)
    for row in reader:
        index = row['Index'].strip()
        record = {
            'data_product_id': f'comp_{index}',
            'name': index,
            'dye_family': index_to_dye_family.get(index, None),
            'final_molecule_structural_formats': {},
            'calculated_properties': {}
        }

        # Map 'xyz' data
        xyz_file_path = os.path.join(coordinates_dir, f'{index}.xyz')
        try:
            with open(xyz_file_path, 'rb') as xyz_file:
                xyz_bytes = xyz_file.read()
                # Encode bytes to Base64 string
                xyz_base64 = base64.b64encode(xyz_bytes).decode('utf-8')
                record['final_molecule_structural_formats']['xyz'] = xyz_base64
        except FileNotFoundError:
            pass

        # Map 'Experimental Emission max (eV)' to 'experimental_emission_max'
        exp_emission_max_str = row.get('Experimental Emission max (eV)', '').strip()
        if exp_emission_max_str:
            try:
                exp_emission_max_value = float(exp_emission_max_str)
                record['calculated_properties']['experimental_emission_max'] = {
                    'value': exp_emission_max_value,
                    'unit': 'eV'
                }
            except ValueError:
                pass

        # Map 'SC-IMOM Emission (eV)' to 'sc_imom_emission'
        sc_imom_emission_str = row.get('SC-IMOM Emission (eV)', '').strip()
        if sc_imom_emission_str:
            try:
                sc_imom_emission_value = float(sc_imom_emission_str)
                record['calculated_properties']['sc_imom_emission'] = {
                    'value': sc_imom_emission_value,
                    'unit': 'eV'
                }
            except ValueError:
                pass

        records.append(record)

with open(output_file, 'w', encoding='utf-8') as jsonfile:
    json.dump(records, jsonfile, ensure_ascii=False, indent=2)

print(f"Data processing complete. JSON output saved as {output_file}.")
