import os
import json
import ijson
from smiles_django.proto import data_catalog_pb2 as dc_pb2
from enum import Enum
from . import data_catalog_service as dcs
from . import metadata_util
from .proto import (computational_dp_pb2 as comp_pb2,
                    experimental_dp_pb2 as exp_pb2,
                    literature_dp_pb2 as lit_pb2)
from google.protobuf.json_format import MessageToJson, ParseDict
from celery import shared_task


def create_smiles_data_product(dp_type, data) -> dc_pb2.DataProduct:
    smiles_dp = get_smiles_dp(dp_type, data)
    data_product = map_smiles_dp_to_catalog_dp(smiles_dp)
    catalog_service = dcs.DataCatalogService()
    result_dp = catalog_service.create_data_product(data_product)
    metadata_util.add_dp_to_schemas(result_dp)

    return result_dp


def get_smiles_data_product(data_product_id: str, dp_type):
    catalog_service = dcs.DataCatalogService()
    catalog_dp = catalog_service.get_data_product(data_product_id)
    result_comp_dp = map_catalog_dp_to_smiles_dp(catalog_dp, dp_type)

    return result_comp_dp


def update_smiles_data_product(data_product_id: str, dp_type, data):
    catalog_service = dcs.DataCatalogService()
    catalog_dp = catalog_service.get_data_product(data_product_id)
    if catalog_dp.data_product_id:
        comp_dp = get_smiles_dp(dp_type, data)
        catalog_dp = map_smiles_dp_to_catalog_dp(comp_dp)
        updated_dp = catalog_service.update_data_product(catalog_dp)

        return map_catalog_dp_to_smiles_dp(updated_dp, dp_type)


def delete_smiles_data_product(data_product_id: str):
    catalog_service = dcs.DataCatalogService()
    catalog_dp = catalog_service.get_data_product(data_product_id)
    if catalog_dp.data_product_id:
        catalog_service.delete_data_product(data_product_id)


def get_smiles_data_products(dp_type):
    json_array = [
        {
            "data_product_id": "1234",
            "parent_data_product_id": "",
            "name": "Experimental DP 1",
            "mol_id": "M123",
            "cas_nr": "123-45-6",
            "smiles": "C1CCCCC1",
            "smiles_stereo": "C[C@@H]1CC[C@@H](C)C[C@@H](C)C1",
            "inchi": "InChI=1S/C6H12/c1-2-3-4-5-6-1/h1-6H2",
            "molfile_blob_source": {
                "kind": "stringValue",
                "stringValue": "BLOB DATA HERE"
            },
            "emp_formula": "C6H12",
            "emp_formula_sort": "C6H12",
            "emp_formula_source": "Manual Entry",
            "mw": 84.16,
            "mw_monoiso": 84.16,
            "rdb": 0,
            "mw_source": "Calculated",
            "validated_by": "John Doe",
            "journal": "Journal of Experimental Chemistry",
            "auth_of_intr": "Jane Smith",
            "jour_cit": "Vol. 1, No. 1, pp. 1-10",
            "year_publ": 2022,
            "doi_link": "https://doi.org/10.1234/abcd",
            "comp_class": "Organic Compound",
            "cuniq": "UNIQ-123",
            "calc_perf": False,
            "org_met": "Synthetic",
            "mol_chrg": 0,
            "state_ofmat": "Solid",
            "color_white": "Yes",
            "color_uv": "No",
            "absorb_max": 200.0,
            "solvent_ae": "Ethanol",
            "absorb": 1.2,
            "conc": 0.1,
            "extinc": 12.0,
            "emis_max": 0.5,
            "temp_abs": 25.0,
            "emis_qy": 0.5,
            "temp_ems": 25.0,
            "lifetime": 2.5,
            "temp_cv": 25.0,
            "reduc_pot": 0.8,
            "hw_or_pk_rp": "Half-Wave Reduction Potential",
            "oxid_pot": 1.2,
            "hw_or_pk_op": "Half-Wave Oxidation Potential",
            "solvent_cv": "Acetonitrile",
            "electrolyte": "KCl",
            "ref_electrd": "Ag/AgCl",
            "inter_thngs": "None",
            "density_20": 0.8,
            "density_20_source": "Calculated",
            "default_warn_level": 0.1,
            "n_20": 1.4,
            "n_20_source": "Manual Entry",
            "mp_low": 20.0,
            "mp_high": 25.0,
            "mp_source": "Manual Entry",
            "bp_low": 70.0,
            "bp_high": 75.0,
            "bp_press": 101.3,
            "press_unit": "kPa",
            "bp_source": "Calculated",
            "safety_r": "R10",
            "safety_h": "H224"
        },
        {
            "data_product_id": "5678",
            "parent_data_product_id": "",
            "name": "Experimental DP 2",
            "mol_id": "M456",
            "cas_nr": "987-65-4",
            "smiles": "CC(C)CC(C)(C)C",
            "smiles_stereo": "CC(C)[C@@H](C)[C@@H](C)C",
            "inchi": "InChI=1S/C8H18/c1-7(2)5-6-8(3,4)9/h7-9H,5-6H2,1-4H3/t7-,8+/m1/s1",
            "molfile_blob_source": {
                "kind": "stringValue",
                "stringValue": "BLOB DATA HERE"
            },
            "emp_formula": "C8H18",
            "emp_formula_sort": "C8H18",
            "emp_formula_source": "Manual Entry",
            "mw": 114.23,
            "mw_monoiso": 114.23,
            "rdb": 0,
            "mw_source": "Calculated",
            "validated_by": "Jane Doe",
            "journal": "Journal of Chemical Sciences",
            "auth_of_intr": "John Smith",
            "jour_cit": "Vol. 2, No. 1, pp. 11-20",
            "year_publ": 2023,
            "doi_link": "https://doi.org/10.5678/efgh",
            "comp_class": "Organic Compound",
            "cuniq": "UNIQ-456",
            "calc_perf": True,
            "org_met": "Biological",
            "mol_chrg": 0,
            "state_ofmat": "Liquid",
            "color_white": "No",
            "color_uv": "Yes",
            "absorb_max": 300.0,
            "solvent_ae": "Methanol",
            "absorb": 1.5,
            "conc": 0.2,
            "extinc": 15.0,
            "emis_max": 0.6,
            "temp_abs": 30.0,
            "emis_qy": 0.6,
            "temp_ems": 30.0,
            "lifetime": 3.5,
            "temp_cv": 30.0,
            "reduc_pot": 1.0,
            "hw_or_pk_rp": "Half-Wave Reduction Potential",
            "oxid_pot": 1.5,
            "hw_or_pk_op": "Half-Wave Oxidation Potential",
            "solvent_cv": "Acetone",
            "electrolyte": "NaCl",
            "ref_electrd": "Hg/Hg2Cl2",
            "inter_thngs": "Silica Gel",
            "density_20": 0.85,
            "density_20_source": "Calculated",
            "default_warn_level": 0.2,
            "n_20": 1.45,
            "n_20_source": "Manual Entry",
            "mp_low": -10.0,
            "mp_high": -5.0,
            "mp_source": "Manual Entry",
            "bp_low": 90.0,
            "bp_high": 95.0,
            "bp_press": 101.3,
            "press_unit": "kPa",
            "bp_source": "Calculated",
            "safety_r": "R10",
            "safety_h": "H224"
        },
        {
            "data_product_id": "7890",
            "parent_data_product_id": "",
            "name": "Experimental DP 3",
            "mol_id": "M234678",
            "cas_nr": "987-65-4",
            "smiles": "CC1=CC=CC=C1",
            "smiles_stereo": "C[C@@H]1C=C[C@H](C)C=C1",
            "inchi": "InChI=1S/C10H12/c1-9-7-6-8-10(9)4-2-3-5-10/h2-8H,1H3/t9-,10+",
            "molfile_blob_source": {
                "kind": "stringValue",
                "stringValue": "BLOB DATA HERE"
            },
            "emp_formula": "C10H12",
            "emp_formula_sort": "C10H12",
            "emp_formula_source": "Manual Entry",
            "mw": 132.21,
            "mw_monoiso": 132.21,
            "rdb": 1,
            "mw_source": "Calculated",
            "validated_by": "Jane Doe",
            "journal": "Journal of Organic Chemistry",
            "auth_of_intr": "John Smith",
            "jour_cit": "Vol. 2, No. 2, pp. 20-30",
            "year_publ": 2023,
            "doi_link": "https://doi.org/10.5678/efgh",
            "comp_class": "Aromatic Compound",
            "cuniq": "UNIQ-456",
            "calc_perf": True,
            "org_met": "Natural",
            "mol_chrg": -1,
            "state_ofmat": "Liquid",
            "color_white": "No",
            "color_uv": "Yes",
            "absorb_max": 300.0,
            "solvent_ae": "Methanol",
            "absorb": 1.8,
            "conc": 0.05,
            "extinc": 18.0,
            "emis_max": 0.3,
            "temp_abs": 20.0,
            "emis_qy": 0.3,
            "temp_ems": 20.0,
            "lifetime": 3.5,
            "temp_cv": 20.0,
            "reduc_pot": 1.0,
            "hw_or_pk_rp": "Peak Reduction Potential",
            "oxid_pot": 1.5,
            "hw_or_pk_op": "Peak Oxidation Potential",
            "solvent_cv": "Dimethyl sulfoxide",
            "electrolyte": "LiCl",
            "ref_electrd": "Ag/AgBr",
            "inter_thngs": "Surfactant",
            "density_20": 1.0,
            "density_20_source": "Manual Entry",
            "default_warn_level": 0.05,
            "n_20": 1.5,
            "n_20_source": "Calculated",
            "mp_low": 40.0,
            "mp_high": 45.0,
            "mp_source": "Calculated",
            "bp_low": 130.0,
            "bp_high": 135.0,
            "bp_press": 101.3,
            "press_unit": "kPa",
            "bp_source": "Manual Entry",
            "safety_r": "R10",
            "safety_h": "H224"
        }
    ]
    return json_array


def map_smiles_dp_to_catalog_dp(smiles_dp) -> dc_pb2.DataProduct:
    data_catalog_product = dc_pb2.DataProduct()
    data_catalog_product.data_product_id = smiles_dp.data_product_id
    data_catalog_product.parent_data_product_id = smiles_dp.parent_data_product_id
    data_catalog_product.name = smiles_dp.name

    # TODO For the time being, a constant value is set clearing the existing values
    data_catalog_product.metadata_schemas[:] = []
    data_catalog_product.metadata_schemas.append("smilesdb")

    # Convert the model to a JSON string, excluding fields 'data_product_id', 'parent_data_product_id', and 'name'
    smiles_dp.data_product_id = ""
    smiles_dp.name = ""
    smiles_dp.parent_data_product_id = ""
    data_catalog_product.metadata = MessageToJson(smiles_dp, including_default_value_fields=False,
                                                  preserving_proto_field_name=True)

    return data_catalog_product


def map_catalog_dp_to_smiles_dp(catalog_dp: dc_pb2.DataProduct, dp_type):
    smiles_dp = get_smiles_dp(dp_type)
    smiles_dp.data_product_id = catalog_dp.data_product_id
    smiles_dp.parent_data_product_id = catalog_dp.parent_data_product_id
    smiles_dp.name = catalog_dp.name
    ParseDict(json.loads(catalog_dp.metadata), smiles_dp)

    return MessageToJson(smiles_dp, including_default_value_fields=False, preserving_proto_field_name=True)


@shared_task()
def upload_smiles_data_products(filename, dp_id):
    with open(filename, 'rb') as input_file:
        jsons = (o for o in ijson.items(input_file, 'item'))
        count = 0
        failed_count = 0
        for j in jsons:
            try:
                smiles_dp = ParseDict(j, get_smiles_dp(SmilesDP(dp_id)), ignore_unknown_fields=True)
                data_product = map_smiles_dp_to_catalog_dp(smiles_dp)
                catalog_service = dcs.DataCatalogService()
                result_dp = catalog_service.create_data_product(data_product)
                metadata_util.add_dp_to_schemas(result_dp)

                print("Created DP: " + result_dp.data_product_id)
                count += 1
            except Exception as e:
                failed_count += 1
                continue
        print("Smiles DP success count/error count %d/%d" % (count, failed_count))

    os.remove(filename)


def get_smiles_dp(dp_type, data=None):
    match dp_type:
        case SmilesDP.COMPUTATIONAL:
            smiles_dp = comp_pb2.ComputationalDP()
            ParseDict(data, smiles_dp) if data is not None else None
        case SmilesDP.EXPERIMENTAL:
            smiles_dp = exp_pb2.ExperimentalDP()
            ParseDict(data, smiles_dp) if data is not None else None
        case SmilesDP.LITERATURE:
            smiles_dp = lit_pb2.LiteratureDP()
            ParseDict(data, smiles_dp) if data is not None else None
        case _:
            raise Exception("Undefined SMILES data product type: " + str(dp_type))

    return smiles_dp


class SmilesDP(Enum):
    COMPUTATIONAL = 1
    EXPERIMENTAL = 2
    LITERATURE = 3
