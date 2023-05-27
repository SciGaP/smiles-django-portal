import os
import json
import ijson
from smiles.proto import data_catalog_pb2 as dc_pb2
from enum import Enum
from . import data_catalog_service as dcs
from . import metadata_util
from .proto import (computational_dp_pb2 as comp_pb2,
                    experimental_dp_pb2 as exp_pb2,
                    literature_dp_pb2 as lit_pb2)
from google.protobuf.json_format import MessageToJson, ParseDict, MessageToDict
from celery import shared_task


def create_smiles_data_product(request_data, dp_type, data) -> dc_pb2.DataProduct:
    smiles_dp = get_smiles_dp(dp_type, data)
    data_product = map_smiles_dp_to_catalog_dp(request_data, smiles_dp, dp_type)
    catalog_service = dcs.DataCatalogService(request_data)
    result_dp = catalog_service.create_data_product(data_product)
    metadata_util.add_dp_to_schemas(request_data, result_dp)

    return result_dp


def get_smiles_data_product(request_data, data_product_id: str, dp_type):
    catalog_service = dcs.DataCatalogService(request_data)
    catalog_dp = catalog_service.get_data_product(data_product_id)
    result_comp_dp = map_catalog_dp_to_smiles_dp(catalog_dp, dp_type)

    return MessageToDict(result_comp_dp, preserving_proto_field_name=True)


def update_smiles_data_product(request_data, data_product_id: str, dp_type, data):
    catalog_service = dcs.DataCatalogService(request_data)
    catalog_dp = catalog_service.get_data_product(data_product_id)
    if catalog_dp.data_product_id:
        comp_dp = get_smiles_dp(dp_type, data)
        catalog_dp = map_smiles_dp_to_catalog_dp(request_data, comp_dp, dp_type)
        updated_dp = catalog_service.update_data_product(catalog_dp)

        return MessageToDict(map_catalog_dp_to_smiles_dp(updated_dp, dp_type), preserving_proto_field_name=True)


def delete_smiles_data_product(request_data, data_product_id: str):
    catalog_service = dcs.DataCatalogService(request_data)
    catalog_dp = catalog_service.get_data_product(data_product_id)
    if catalog_dp.data_product_id:
        catalog_service.delete_data_product(data_product_id)


def get_smiles_data_products(request_data, dp_type):
    catalog_service = dcs.DataCatalogService(request_data)
    filtered_schema_list = metadata_util.get_metadata_schemas(request_data, dp_type.prefix)

    if len(filtered_schema_list) == 1:
        sql = f"SELECT data_product_id FROM {filtered_schema_list[0]}"
    elif len(filtered_schema_list) > 1:
        sql = " UNION ".join([f"SELECT data_product_id FROM {schema}" for schema in filtered_schema_list])
    else:
        raise Exception("No Schemas have been defined")

    data_products = catalog_service.search_data_products(sql)
    smiles_products = [
        MessageToDict(map_catalog_dp_to_smiles_dp(data_product, dp_type), preserving_proto_field_name=True) for
        data_product in data_products]

    return smiles_products


def map_smiles_dp_to_catalog_dp(request_data, smiles_dp, dp_type) -> dc_pb2.DataProduct:
    data_catalog_product = dc_pb2.DataProduct()
    data_catalog_product.data_product_id = smiles_dp.data_product_id
    data_catalog_product.parent_data_product_id = smiles_dp.parent_data_product_id
    data_catalog_product.name = smiles_dp.name

    # TODO For the time being, all the specific schemas will be added
    data_catalog_product.metadata_schemas[:] = metadata_util.get_metadata_schemas(request_data, dp_type.prefix)

    # Convert the model to a JSON string, excluding fields 'data_product_id', 'parent_data_product_id', and 'name'
    smiles_dp.data_product_id = ""
    smiles_dp.name = ""
    smiles_dp.parent_data_product_id = ""
    data_catalog_product.metadata = MessageToJson(smiles_dp, including_default_value_fields=False,
                                                  preserving_proto_field_name=True)

    return data_catalog_product


def map_catalog_dp_to_smiles_dp(catalog_dp: dc_pb2.DataProduct, dp_type):
    smiles_dp = get_smiles_dp(dp_type)
    ParseDict(json.loads(catalog_dp.metadata), smiles_dp)
    smiles_dp.data_product_id = catalog_dp.data_product_id
    smiles_dp.parent_data_product_id = catalog_dp.parent_data_product_id
    smiles_dp.name = catalog_dp.name

    return smiles_dp


@shared_task()
def upload_smiles_data_products(request_data, filename, dp_id):
    with open(filename, 'rb') as input_file:
        jsons = (o for o in ijson.items(input_file, 'item'))
        count = 0
        failed_count = 0
        for j in jsons:
            try:
                smiles_dp = ParseDict(j, get_smiles_dp(SmilesDP(dp_id)), ignore_unknown_fields=True)
                data_product = map_smiles_dp_to_catalog_dp(request_data, smiles_dp, SmilesDP(dp_id))
                catalog_service = dcs.DataCatalogService(request_data)
                result_dp = catalog_service.create_data_product(data_product)
                metadata_util.add_dp_to_schemas(request_data, result_dp)

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

    # For all the specific schema types a prefix will be appended,
    # and it will be used to differentiate data product types
    @property
    def prefix(self):
        if self == SmilesDP.COMPUTATIONAL:
            return "comp_"
        elif self == SmilesDP.EXPERIMENTAL:
            return "exp_"
        elif self == SmilesDP.LITERATURE:
            return "lit_"
        else:
            raise ValueError(f"Unknown enum value: {self}")
