from django.core.cache import cache
from .proto import data_catalog_pb2 as dc_pb2
from . import data_catalog_service as dcs

SCHEMA_CACHE_TTL = 300  # 5 minutes
_SCHEMA_CACHE_KEY = "smiles:metadata_schemas:all"


def create_metadata_schema(request_data, schema_name: str) -> dc_pb2.MetadataSchema:
    catalog_service = dcs.DataCatalogService(request_data)
    metadata_schema = dc_pb2.MetadataSchema()
    metadata_schema.schema_name = schema_name
    result = catalog_service.create_metadata_schema(metadata_schema)
    invalidate_schema_cache()
    return result


def get_metadata_schemas(request_data, prefix=None):
    schema_names = cache.get(_SCHEMA_CACHE_KEY)
    if schema_names is None:
        catalog_service = dcs.DataCatalogService(request_data)
        schemas = catalog_service.get_metadata_schemas()
        schema_names = [schema.schema_name for schema in schemas]
        cache.set(_SCHEMA_CACHE_KEY, schema_names, SCHEMA_CACHE_TTL)
    if prefix:
        return [name for name in schema_names if name.lower().startswith(prefix)]
    return schema_names


def invalidate_schema_cache():
    cache.delete(_SCHEMA_CACHE_KEY)


def get_metadata_schema_field(request_data, data):
    catalog_service = dcs.DataCatalogService(request_data)
    return catalog_service.get_metadata_schema_field(data["schema_name"], data["field_name"])


def create_metadata_schema_field(request_data, data) -> dc_pb2.MetadataSchemaField:
    catalog_service = dcs.DataCatalogService(request_data)
    schema_field = dc_pb2.MetadataSchemaField(**data)

    return catalog_service.create_metadata_schema_field(schema_field)


def delete_metadata_schema_field(request_data, data):
    catalog_service = dcs.DataCatalogService(request_data)
    schema_field = dc_pb2.MetadataSchemaField(**data)

    return catalog_service.delete_metadata_schema_field(schema_field)


def add_dp_to_schemas(request_data, data_product: dc_pb2.DataProduct):
    # Adding the data product to all the relevant schemas
    catalog_service = dcs.DataCatalogService(request_data)
    for schema in data_product.metadata_schemas:
        if catalog_service.get_metadata_schema(schema):
            catalog_service.add_data_product_to_metadata_schema(data_product.data_product_id, schema)


def remove_dp_from_schemas(request_data, data_product: dc_pb2.DataProduct):
    catalog_service = dcs.DataCatalogService(request_data)
    for schema in data_product.metadata_schemas:
        catalog_service.remove_data_product_from_metadata_schema(data_product.data_product_id, schema)
