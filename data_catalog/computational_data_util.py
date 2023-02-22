import data_catalog_pb2
from .proto import computational_dp_pb2
from google.protobuf.json_format import MessageToJson


def map_computational_dp_to_catalog_dp(comp_dp: computational_dp_pb2.ComputationalDP()) -> data_catalog_pb2.DataProduct:
    data_catalog_product = data_catalog_pb2.DataProduct()
    data_catalog_product.data_product_id = comp_dp.data_product_id
    data_catalog_product.parent_data_product_id = comp_dp.parent_data_product_id
    data_catalog_product.name = comp_dp.name

    # Convert the model to a JSON string, excluding fields 'data_product_id', 'parent_data_product_id', 'name
    comp_dp.data_product_id = ""
    comp_dp.name = ""
    comp_dp.parent_data_product_id = ""
    data_catalog_product.metadata = MessageToJson(comp_dp, including_default_value_fields=False,
                                                  preserving_proto_field_name=True)

    return data_catalog_product
