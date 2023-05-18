from .proto import data_catalog_pb2 as dc_pb2
from . import data_catalog_service as dcs


def create_metadata_schema(request, schema_name: str) -> dc_pb2.MetadataSchema:
    catalog_service = dcs.DataCatalogService(request.user)
    metadata_schema = dc_pb2.MetadataSchema()
    metadata_schema.schema_name = schema_name

    return catalog_service.create_metadata_schema(metadata_schema)


def get_metadata_schemas(request, prefix=None):
    catalog_service = dcs.DataCatalogService(request.user)
    schemas = catalog_service.get_metadata_schemas()

    if prefix:
        schemas = [schema.schema_name for schema in schemas if schema.schema_name.lower().startswith(prefix)]
    return schemas


def get_metadata_schema_field(request, data):
    catalog_service = dcs.DataCatalogService(request.user)
    return catalog_service.get_metadata_schema_field(data["schema_name"], data["field_name"])


def create_metadata_schema_field(request, data) -> dc_pb2.MetadataSchemaField:
    catalog_service = dcs.DataCatalogService(request.user)
    schema_field = dc_pb2.MetadataSchemaField(**data)

    return catalog_service.create_metadata_schema_field(schema_field)


def delete_metadata_schema_field(request, data):
    catalog_service = dcs.DataCatalogService(request.user)
    schema_field = dc_pb2.MetadataSchemaField(**data)

    return catalog_service.delete_metadata_schema_field(schema_field)


def add_dp_to_schemas(request, data_product: dc_pb2.DataProduct):
    # Adding the data product to all the relevant schemas
    catalog_service = dcs.DataCatalogService(request.user)
    for schema in data_product.metadata_schemas:
        if catalog_service.get_metadata_schema(schema):
            catalog_service.add_data_product_to_metadata_schema(data_product.data_product_id, schema)


def remove_dp_from_schemas(request, data_product: dc_pb2.DataProduct):
    catalog_service = dcs.DataCatalogService(request.user)
    for schema in data_product.metadata_schemas:
        catalog_service.remove_data_product_from_metadata_schema(data_product.data_product_id, schema)
