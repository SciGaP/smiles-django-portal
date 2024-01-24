import pandas as pd
import ijson
from .proto import (computational_dp_pb2 as comp_pb2,
                    experimental_dp_pb2 as exp_pb2,
                    literature_dp_pb2 as lit_pb2)
from . import data_catalog_service as dcs
from . import smiles_dp_util
from . import metadata_util


def json_data_upload(request_data, json_file, dp_id):
    with open(json_file, 'rb') as input_file:
        jsons = (o for o in ijson.items(input_file, 'item'))
        count = 0
        failed_count = 0
        for j in jsons:
            try:
                smiles_dp = smiles_dp_util.get_smiles_dp(smiles_dp_util.SmilesDP(dp_id), j)
                data_product = smiles_dp_util.map_smiles_dp_to_catalog_dp(request_data, smiles_dp,
                                                                          smiles_dp_util.SmilesDP(dp_id))
                catalog_service = dcs.DataCatalogService(request_data)
                result_dp = catalog_service.create_data_product(data_product)
                metadata_util.add_dp_to_schemas(request_data, result_dp)

                print("Created DP: " + result_dp.data_product_id)
                count += 1

            except Exception as e:
                failed_count += 1
                print("Error while uploading the dp " + str(e))
                continue

        print("Smiles DP success count/error count %d/%d" % (count, failed_count))


def csv_data_upload(request_data, csv_file, dp_id):
    dp_type = smiles_dp_util.SmilesDP(dp_id)
    if dp_type == smiles_dp_util.SmilesDP.COMPUTATIONAL:
        raise NotImplemented("CSV file upload is not supported for Computational Data type yet")
    elif dp_type == smiles_dp_util.SmilesDP.EXPERIMENTAL:
        raise NotImplemented("CSV file upload is not supported for Experimental Data type yet")
    elif dp_type == smiles_dp_util.SmilesDP.LITERATURE:
        csv_lit_data_upload(request_data, csv_file, dp_type)
    else:
        raise Exception("Undefined SMILES data product type: " + str(dp_type))


def csv_lit_data_upload(request_data, csv_file, dp_type):
    df = pd.read_csv(csv_file)
    # Group by 'biblio-doi'
    grouped = df.groupby('biblio-doi')

    count = 0
    failed_count = 0

    for doi, group in grouped:
        try:
            literature_dp = lit_pb2.LiteratureDP()
            literature_dp.biblio.doi = doi
            literature_dp.name = doi

            first_row = group.iloc[0]
            if pd.notna(first_row.get('biblio-html_info', None)):
                literature_dp.biblio.html_info = first_row['biblio-html_info']
            if pd.notna(first_row.get('user', None)):
                literature_dp.user = first_row['user']
            if pd.notna(first_row.get('search_keywords_count', None)):
                literature_dp.search_keywords_count = int(first_row['search_keywords_count'])
            if pd.notna(first_row.get('redox_info', None)):
                literature_dp.redox_info = first_row['redox_info']
            if pd.notna(first_row.get('note', None)):
                literature_dp.note = first_row['note']

            for index, row in group.iterrows():
                # Create and populate Record for each row
                record = lit_pb2.Record()
                if pd.notna(row.get('record-smiles', None)):
                    record.smiles = row['record-smiles']
                if pd.notna(row.get('record-other_names', None)):
                    record.other_names.extend(row['record-other_names'].split(';'))
                if pd.notna(row.get('record-molecular_weight', None)):
                    record.molecular_weight = float(row['record-molecular_weight'])

                # SpectralData
                spectral_data = lit_pb2.SpectralData()
                if pd.notna(row.get('record-spectral_data-solvent', None)):
                    spectral_data.solvent = row['record-spectral_data-solvent']
                if pd.notna(row.get('record-spectral_data-absorb_max_nm', None)):
                    spectral_data.absorb_max_nm = float(row['record-spectral_data-absorb_max_nm'])
                if pd.notna(row.get('record-spectral_data-emis_max_nm', None)):
                    spectral_data.emis_max_nm = float(row['record-spectral_data-emis_max_nm'])
                if pd.notna(row.get('record-spectral_data-lifetime', None)):
                    lifetime_str = row['record-spectral_data-lifetime']
                    if ',' in lifetime_str:
                        lifetime_values = lifetime_str.split(',')
                    else:
                        lifetime_values = [lifetime_str]

                    for value in lifetime_values:
                        spectral_data.lifetime.append(float(value.strip()))
                if pd.notna(row.get('record-spectral_data-quantum_yield', None)):
                    spectral_data.quantum_yield = float(row['record-spectral_data-quantum_yield'])
                if pd.notna(row.get('record-spectral_data-molar_absorb_coefficient', None)):
                    spectral_data.molar_absorb_coefficient = float(row['record-spectral_data-molar_absorb_coefficient'])

                # Add SpectralData to Record
                record.spectral_data.CopyFrom(spectral_data)

                # Define a mapping between DataFrame columns and fields
                field_mapping = {
                    'record-electrochemical_potential-cathodic-red_v': ('cathodic.red_v', float),
                    'record-electrochemical_potential-cathodic-hw_or_pk': ('cathodic.hw_or_pk', str),
                    'record-electrochemical_potential-cathodic-solvent': ('cathodic.solvent', str),
                    'record-electrochemical_potential-cathodic-electrolyte': ('cathodic.electrolyte', str),
                    'record-electrochemical_potential-anodic-ox_v': ('anodic.ox_v', float),
                    'record-electrochemical_potential-anodic-hw_or_pk': ('anodic.hw_or_pk', str),
                    'record-electrochemical_potential-anodic-solvent': ('anodic.solvent', str),
                    'record-electrochemical_potential-anodic-electrolyte': ('anodic.electrolyte', str),
                    'record-electrochemical_potential-value_quoted_ref': ('value_quoted_ref', str),
                    'record-electrochemical_potential-data_measured_ref': ('data_measured_ref', str),
                    'record-electrochemical_potential-method': ('method', str),
                    'record-electrochemical_potential-temperature': ('temperature', float),
                    'record-electrochemical_potential-data_type': ('data_type', str),
                    'record-electrochemical_potential-human_validator': ('human_validator', str),
                    'record-electrochemical_potential-elec_val_status_red': ('elec_val_status_red', str),
                    'record-electrochemical_potential-elec_val_status_ox': ('elec_val_status_ox', str)
                }

                ecp = lit_pb2.ElectroChemicalPotential()

                for column, (protobuf_field, field_type) in field_mapping.items():
                    if pd.notna(row.get(column, None)):
                        # Split the field into parts if it's nested (e.g., 'cathodic.red_v')
                        nested_fields = protobuf_field.split('.')
                        target = ecp
                        # Traverse nested fields, if any
                        for field in nested_fields[:-1]:
                            target = getattr(target, field)
                        # Set the value on the appropriate field, converting to the correct type
                        setattr(target, nested_fields[-1], field_type(row[column]))

                # Add ElectroChemicalPotential to Record
                record.electrochemical_potential.CopyFrom(ecp)

                # Add the Record to LiteratureDP
                literature_dp.records.append(record)

            data_product = smiles_dp_util.map_smiles_dp_to_catalog_dp(request_data, literature_dp, dp_type)
            catalog_service = dcs.DataCatalogService(request_data)
            result_dp = catalog_service.create_data_product(data_product)
            metadata_util.add_dp_to_schemas(request_data, result_dp)

            print("Created DP: " + result_dp.data_product_id)
            count += 1

        except Exception as e:
            failed_count += 1
            print("Error while uploading the dp " + str(e))
            continue

    print("Smiles DP success count/error count %d/%d" % (count, failed_count))
