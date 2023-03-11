import grpc
import data_catalog_pb2 as pb2
import data_catalog_pb2_grpc

from typing import List
from grpc import StatusCode, RpcError


class DataCatalogService:
    def __init__(self):
        # Connect to the gRPC service (DataCatalogAPI gRPC Server)
        channel = grpc.insecure_channel('localhost:6565')
        self.stub = data_catalog_pb2_grpc.DataCatalogAPIServiceStub(channel)

    def create_data_product(self, data_catalog_product: pb2.DataProduct) -> pb2.DataProduct:
        create_request = pb2.DataProductCreateRequest()
        create_request.data_product.CopyFrom(data_catalog_product)
        create_response = self.stub.createDataProduct(create_request)

        return create_response.data_product

    def update_data_product(self, data_catalog_product: pb2.DataProduct) -> pb2.DataProduct:
        update_request = pb2.DataProductUpdateRequest()
        update_request.data_product.CopyFrom(data_catalog_product)
        update_response = self.stub.updateDataProduct(update_request)

        return update_response.data_product

    def get_data_product(self, dp_id: str) -> pb2.DataProduct:
        get_request = pb2.DataProductGetRequest(data_product_id=dp_id)
        try:
            get_response = self.stub.getDataProduct(get_request)
            return get_response.data_product
        except Exception as e:
            if isinstance(e, RpcError) and e.code() == StatusCode.NOT_FOUND:
                raise Exception("Data product not found")

    def delete_data_product(self, dp_id: str):
        delete_request = pb2.DataProductDeleteRequest(data_product_id=dp_id)
        self.stub.deleteDataProduct(delete_request)

    def create_metadata_schema(self, meta_data_schema: pb2.MetadataSchema) -> pb2.MetadataSchema:
        create_request = pb2.MetadataSchemaCreateRequest(meta_data_schema)
        create_response = self.stub.createMetadataSchema(create_request)

        return create_response.metadata_schema

    def get_metadata_schema(self, schema_name: str) -> pb2.MetadataSchema:
        get_request = pb2.MetadataSchemaGetRequest(schema_name=schema_name)
        get_response = self.stub.getMetadataSchema(get_request)

        return get_response.metadata_schema

    def delete_metadata_schema(self, schema_name: str) -> pb2.MetadataSchema:
        delete_request = pb2.MetadataSchemaDeleteRequest(metadata_schema=schema_name)
        delete_response = self.stub.deleteMetadataSchema(delete_request)

        return delete_response.metadata_schema

    def create_metadata_schema_field(self, metadata_schema_field: pb2.MetadataSchemaField) -> pb2.MetadataSchemaField:
        create_request = pb2.MetadataSchemaFieldCreateRequest()
        create_request.metadata_schema_field.CopyFrom(metadata_schema_field)
        create_response = self.stub.createMetadataSchemaField(create_request)

        return create_response.metadata_schema_field

    def get_metadata_schema_field(self, schema_name: str, field_name: str) -> pb2.MetadataSchemaField:
        get_request = pb2.MetadataSchemaFieldGetRequest(schema_name, field_name)
        get_response = self.stub.getMetadataSchemaField(get_request)

        return get_response.metadata_schema_field

    def update_metadata_schema_field(self, schema_field: pb2.MetadataSchemaField) -> pb2.MetadataSchemaField:
        update_request = pb2.MetadataSchemaFieldUpdateRequest(metadata_schema_field=schema_field)
        update_response = self.stub.updateMetadataSchemaField(update_request)

        return update_response.metadata_schema_field

    def delete_metadata_schema_field(self, schema_field: pb2.MetadataSchemaField):
        delete_request = pb2.MetadataSchemaDeleteRequest(metadata_schema_field=schema_field)
        delete_response = self.stub.deleteMetadataSchemaField(delete_request)

        return delete_response

    def get_metadata_schema_fields(self, schema_name: str) -> List[pb2.MetadataSchemaField]:
        get_request = pb2.MetadataSchemaFieldListRequest(schema_name=schema_name)
        get_response = self.stub.getMetadataSchemaFields(get_request)

        return get_response.metadata_schema_field

    def add_data_product_to_metadata_schema(self, data_product_id: str, schema_name: str) -> pb2.DataProduct:
        request = pb2.DataProductAddToMetadataSchemaRequest(data_product_id=data_product_id, schema_name=schema_name)
        response = self.stub.addDataProductToMetadataSchema(request)

        return response.data_product

    def remove_data_product_from_metadata_schema(self, data_product_id: str, schema_name: str) -> pb2.DataProduct:
        request = pb2.DataProductRemoveFromMetadataSchemaRequest(data_product_id=data_product_id,
                                                                 schema_name=schema_name)
        response = self.stub.removeDataProductFromMetadataSchema(request)

        return response.data_product
