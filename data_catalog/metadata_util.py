import data_catalog_pb2 as dc_pb2
from . import data_catalog_service as dcs

SCHEMA_NAME = "smilesdb"


def create_metadata_schema(schema_name: str) -> dc_pb2.MetadataSchema:
    catalog_service = dcs.DataCatalogService()
    metadata_schema = dc_pb2.MetadataSchema()
    # TODO proper way to extract the schema name or should this be a constant for SMILES project
    metadata_schema.schema_name = SCHEMA_NAME

    return catalog_service.create_metadata_schema(metadata_schema)


def get_metadata_schema_field(data):
    catalog_service = dcs.DataCatalogService()
    return catalog_service.get_metadata_schema_field(data["schema_name"], data["field_name"])


def create_metadata_schema_field(data) -> dc_pb2.MetadataSchemaField:
    catalog_service = dcs.DataCatalogService()
    schema_field = dc_pb2.MetadataSchemaField(**data)

    return catalog_service.create_metadata_schema_field(schema_field)


def delete_metadata_schema_field(data):
    catalog_service = dcs.DataCatalogService()
    schema_field = dc_pb2.MetadataSchemaField(**data)

    return catalog_service.delete_metadata_schema_field(schema_field)


def add_dp_to_schemas(data_product: dc_pb2.DataProduct):
    # Adding the data product to all the relevant schemas
    catalog_service = dcs.DataCatalogService()
    for schema in data_product.metadata_schemas:
        catalog_service.add_data_product_to_metadata_schema(data_product.data_product_id, schema)


def remove_dp_from_schemas(data_product: dc_pb2.DataProduct):
    catalog_service = dcs.DataCatalogService()
    for schema in data_product.metadata_schemas:
        catalog_service.remove_data_product_from_metadata_schema(data_product.data_product_id, schema)
