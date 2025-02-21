
from smiles.proto.data_catalog_pb2 import GrantPermissionRequest, GrantPermissionToGroupRequest
from smiles.proto.data_catalog_pb2 import SearchRequest
from smiles.proto.data_catalog_pb2_grpc import SharingServiceStub
import grpc

class SharingService:
    def __init__(self, grpc_channel):
        self.client = SharingServiceStub(grpc_channel)

    def share_with_user(self, user_info, data_product_ids, permission):
        for data_product_id in data_product_ids:
            request = GrantPermissionRequest(
                user_info=user_info,
                data_product={"data_product_id": data_product_id},
                permission=permission
            )
            response = self.client.GrantPermissionToUser(request)
            if not response:
                raise Exception(f"Failed to share data product {data_product_id} with user {user_info.user_id}")
        return True

    def share_with_group(self, group_info, data_product_ids, permission):
        for data_product_id in data_product_ids:
            request = GrantPermissionToGroupRequest(
                group_info=group_info,
                data_product={"data_product_id": data_product_id},
                permission=permission
            )
            response = self.client.GrantPermissionToGroup(request)
            if not response:
                raise Exception(f"Failed to share data product {data_product_id} with group {group_info.group_id}")
        return True

    def search_users(self, query, tenant_id):
        request = SearchRequest(query=query, tenant_id=tenant_id)
        response = self.client.SearchUsers(request)
        return response.users

    def search_groups(self, query, tenant_id):
        request = SearchRequest(query=query, tenant_id=tenant_id)
        response = self.client.SearchGroups(request)
        return response.groups

