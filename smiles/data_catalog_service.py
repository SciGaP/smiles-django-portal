import logging
import threading
from typing import List

import grpc
from django.conf import settings
from grpc import StatusCode, RpcError

from smiles.proto import data_catalog_pb2_grpc, data_catalog_pb2 as pb2

logger = logging.getLogger(__name__)

_channel_lock = threading.Lock()
_grpc_channel = None

# Timeout for all gRPC calls, prevents hanging forever on a dead channel
_GRPC_TIMEOUT = 30  # seconds


def get_grpc_channel():
    global _grpc_channel
    if _grpc_channel is None:
        with _channel_lock:
            if _grpc_channel is None:
                _grpc_channel = grpc.insecure_channel(
                    settings.DATA_CATALOG_GRPC_SERVER
                )
    return _grpc_channel


class DataCatalogService:
    def __init__(self, request_data):
        channel = get_grpc_channel()
        self.stub = data_catalog_pb2_grpc.DataCatalogAPIServiceStub(channel)
        self.user_info = pb2.UserInfo(user_id=request_data['user_id'], tenant_id=request_data['tenant_id'])
        if 'group_ids' in request_data:
            self.user_info.group_ids.extend(request_data['group_ids'])

    def create_data_product(self, data_catalog_product: pb2.DataProduct) -> pb2.DataProduct:
        create_request = pb2.DataProductCreateRequest(user_info=self.user_info)
        create_request.data_product.CopyFrom(data_catalog_product)
        create_response = self.stub.createDataProduct(create_request, timeout=_GRPC_TIMEOUT)

        return create_response.data_product

    def update_data_product(self, data_catalog_product: pb2.DataProduct) -> pb2.DataProduct:
        update_request = pb2.DataProductUpdateRequest(user_info=self.user_info)
        update_request.data_product.CopyFrom(data_catalog_product)
        update_response = self.stub.updateDataProduct(update_request, timeout=_GRPC_TIMEOUT)

        return update_response.data_product

    def get_data_product(self, dp_id: str) -> pb2.DataProduct:
        get_request = pb2.DataProductGetRequest(user_info=self.user_info, data_product_id=dp_id)
        try:
            get_response = self.stub.getDataProduct(get_request, timeout=_GRPC_TIMEOUT)
            return get_response.data_product
        except Exception as e:
            if isinstance(e, RpcError) and e.code() == StatusCode.NOT_FOUND:
                raise Exception("Data product not found")

    def delete_data_product(self, dp_id: str):
        delete_request = pb2.DataProductDeleteRequest(user_info=self.user_info, data_product_id=dp_id)
        self.stub.deleteDataProduct(delete_request, timeout=_GRPC_TIMEOUT)

    def create_metadata_schema(self, schema_name: pb2.MetadataSchema) -> pb2.MetadataSchema:
        create_request = pb2.MetadataSchemaCreateRequest(user_info=self.user_info, meta_data_schema=schema_name)
        create_response = self.stub.createMetadataSchema(create_request, timeout=_GRPC_TIMEOUT)

        return create_response.metadata_schema

    def get_metadata_schema(self, schema_name: str) -> pb2.MetadataSchema:
        get_request = pb2.MetadataSchemaGetRequest(user_info=self.user_info, schema_name=schema_name)
        get_response = self.stub.getMetadataSchema(get_request, timeout=_GRPC_TIMEOUT)

        return get_response.metadata_schema

    def get_metadata_schemas(self) -> List[pb2.MetadataSchema]:
        get_request = pb2.MetadataSchemaListRequest(user_info=self.user_info)
        get_response = self.stub.getMetadataSchemas(get_request, timeout=_GRPC_TIMEOUT)

        return get_response.metadata_schemas

    def delete_metadata_schema(self, schema_name: str) -> pb2.MetadataSchema:
        delete_request = pb2.MetadataSchemaDeleteRequest(user_info=self.user_info, metadata_schema=schema_name)
        delete_response = self.stub.deleteMetadataSchema(delete_request, timeout=_GRPC_TIMEOUT)

        return delete_response.metadata_schema

    def create_metadata_schema_field(self, metadata_schema_field: pb2.MetadataSchemaField) -> pb2.MetadataSchemaField:
        create_request = pb2.MetadataSchemaFieldCreateRequest(user_info=self.user_info)
        create_request.metadata_schema_field.CopyFrom(metadata_schema_field)
        create_response = self.stub.createMetadataSchemaField(create_request, timeout=_GRPC_TIMEOUT)

        return create_response.metadata_schema_field

    def get_metadata_schema_field(self, schema_name: str, field_name: str) -> pb2.MetadataSchemaField:
        get_request = pb2.MetadataSchemaFieldGetRequest(user_info=self.user_info, schema_name=schema_name,
                                                        field_name=field_name)
        get_response = self.stub.getMetadataSchemaField(get_request, timeout=_GRPC_TIMEOUT)

        return get_response.metadata_schema_field

    def update_metadata_schema_field(self, schema_field: pb2.MetadataSchemaField) -> pb2.MetadataSchemaField:
        update_request = pb2.MetadataSchemaFieldUpdateRequest(user_info=self.user_info,
                                                              metadata_schema_field=schema_field)
        update_response = self.stub.updateMetadataSchemaField(update_request, timeout=_GRPC_TIMEOUT)

        return update_response.metadata_schema_field

    def delete_metadata_schema_field(self, schema_field: pb2.MetadataSchemaField):
        delete_request = pb2.MetadataSchemaDeleteRequest(user_info=self.user_info, metadata_schema_field=schema_field)
        delete_response = self.stub.deleteMetadataSchemaField(delete_request, timeout=_GRPC_TIMEOUT)

        return delete_response

    def get_metadata_schema_fields(self, schema_name: str) -> List[pb2.MetadataSchemaField]:
        get_request = pb2.MetadataSchemaFieldListRequest(user_info=self.user_info, schema_name=schema_name)
        get_response = self.stub.getMetadataSchemaFields(get_request, timeout=_GRPC_TIMEOUT)

        return get_response.metadata_schema_field

    def add_data_product_to_metadata_schema(self, data_product_id: str, schema_name: str) -> pb2.DataProduct:
        request = pb2.DataProductAddToMetadataSchemaRequest(user_info=self.user_info, data_product_id=data_product_id,
                                                            schema_name=schema_name)
        response = self.stub.addDataProductToMetadataSchema(request, timeout=_GRPC_TIMEOUT)

        return response.data_product

    def remove_data_product_from_metadata_schema(self, data_product_id: str, schema_name: str) -> pb2.DataProduct:
        request = pb2.DataProductRemoveFromMetadataSchemaRequest(user_info=self.user_info,
                                                                 data_product_id=data_product_id,
                                                                 schema_name=schema_name)
        response = self.stub.removeDataProductFromMetadataSchema(request, timeout=_GRPC_TIMEOUT)

        return response.data_product

    def search_data_products(self, sql: str, page: int, page_size: int) -> pb2.DataProductSearchResponse:
        search_request = pb2.DataProductSearchRequest(
            user_info=self.user_info,
            sql=sql,
            page=page,
            page_size=page_size
        )
        response = self.stub.searchDataProducts(search_request, timeout=_GRPC_TIMEOUT)
        return response

    def grant_permission_to_user(self, target_user_id: str, data_product_id: str, permission: pb2.Permission):
        target_user_info = pb2.UserInfo(user_id=target_user_id, tenant_id=self.user_info.tenant_id)
        req = pb2.GrantPermissionToUserRequest(
            user_info=self.user_info,
            target_user=target_user_info,
            data_product_id=data_product_id,
            permission=permission
        )
        self.stub.GrantPermissionToUser(req, timeout=_GRPC_TIMEOUT)

    def grant_permission_to_group(self, target_group_id: str, data_product_id: str, permission: pb2.Permission):
        target_group_info = pb2.GroupInfo(group_id=target_group_id, tenant_id=self.user_info.tenant_id)
        req = pb2.GrantPermissionToGroupRequest(
            user_info=self.user_info,
            target_group=target_group_info,
            data_product_id=data_product_id,
            permission=permission
        )
        self.stub.GrantPermissionToGroup(req, timeout=_GRPC_TIMEOUT)

    def grant_permission_to_user_on_all(self, target_user_id: str,
                                        permission: pb2.Permission):
        target_user_info = pb2.UserInfo(
            user_id=target_user_id,
            tenant_id=self.user_info.tenant_id
        )
        req = pb2.GrantPermissionToUserOnAllRequest(
            user_info=self.user_info,
            target_user=target_user_info,
            permission=permission
        )
        self.stub.GrantPermissionToUserOnAll(req, timeout=_GRPC_TIMEOUT)

    def grant_permission_to_group_on_all(self, target_group_id: str,
                                         permission: pb2.Permission):
        target_group_info = pb2.GroupInfo(
            group_id=target_group_id,
            tenant_id=self.user_info.tenant_id
        )
        req = pb2.GrantPermissionToGroupOnAllRequest(
            user_info=self.user_info,
            target_group=target_group_info,
            permission=permission
        )
        self.stub.GrantPermissionToGroupOnAll(req, timeout=_GRPC_TIMEOUT)
