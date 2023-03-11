import json
import data_catalog_pb2 as dc_pb2
from .proto import computational_dp_pb2 as pb2
from google.protobuf.json_format import MessageToJson, ParseDict
from . import data_catalog_service as dcs
from . import metadata_util


def create_computational_data_product(computational_dp: pb2.ComputationalDP()) -> dc_pb2.DataProduct:
    data_product = map_computational_dp_to_catalog_dp(computational_dp)
    catalog_service = dcs.DataCatalogService()
    result_dp = catalog_service.create_data_product(data_product)
    metadata_util.add_dp_to_schemas(result_dp)

    return result_dp


def get_computational_data_product(data_product_id: str):
    catalog_service = dcs.DataCatalogService()
    catalog_dp = catalog_service.get_data_product(data_product_id)
    result_comp_dp = map_catalog_dp_to_computational_dp(catalog_dp)

    return result_comp_dp


def update_computational_data_product(data, data_product_id: str) -> pb2.ComputationalDP:
    catalog_service = dcs.DataCatalogService()
    catalog_dp = catalog_service.get_data_product(data_product_id)
    if catalog_dp.data_product_id:
        comp_dp = pb2.ComputationalDP(**data)
        catalog_dp = map_computational_dp_to_catalog_dp(comp_dp)
        updated_dp = catalog_service.update_data_product(catalog_dp)

        return map_catalog_dp_to_computational_dp(updated_dp)


def delete_computational_data_product(data_product_id: str):
    catalog_service = dcs.DataCatalogService()
    catalog_dp = catalog_service.get_data_product(data_product_id)
    if catalog_dp.data_product_id:
        catalog_service.delete_data_product(data_product_id)


def map_computational_dp_to_catalog_dp(comp_dp: pb2.ComputationalDP()) -> dc_pb2.DataProduct:
    data_catalog_product = dc_pb2.DataProduct()
    data_catalog_product.data_product_id = comp_dp.data_product_id
    data_catalog_product.parent_data_product_id = comp_dp.parent_data_product_id
    data_catalog_product.name = comp_dp.name

    # TODO For the time being, a constant value is set clearing the existing values
    data_catalog_product.metadata_schemas[:] = []
    data_catalog_product.metadata_schemas.append("smilesdb")

    # Convert the model to a JSON string, excluding fields 'data_product_id', 'parent_data_product_id', 'name
    comp_dp.data_product_id = ""
    comp_dp.name = ""
    comp_dp.parent_data_product_id = ""
    data_catalog_product.metadata = MessageToJson(comp_dp, including_default_value_fields=False,
                                                  preserving_proto_field_name=True)

    return data_catalog_product


def map_catalog_dp_to_computational_dp(catalog_dp: dc_pb2.DataProduct) -> pb2.ComputationalDP:
    comp_dp = pb2.ComputationalDP()
    comp_dp.data_product_id = catalog_dp.data_product_id
    comp_dp.parent_data_product_id = catalog_dp.parent_data_product_id
    comp_dp.name = catalog_dp.name
    ParseDict(json.loads(catalog_dp.metadata), comp_dp)

    return MessageToJson(comp_dp, including_default_value_fields=False, preserving_proto_field_name=True)
