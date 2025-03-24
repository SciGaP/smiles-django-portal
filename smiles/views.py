import json
import os
import logging
import grpc

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from django.views import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import smiles_dp_util
from . import smiles_data_migration
from django.shortcuts import render
from .apps import SmilesDjangoPortalConfig

from .airavata_portal_service import AiravataPortalAPIService
from .data_catalog_service import DataCatalogService
from smiles.proto import data_catalog_pb2 as pb2
from django.views.decorators.csrf import csrf_exempt
from grpc import StatusCode

logger = logging.getLogger(__name__)

class ComputationalDPView(View):
    UPLOAD_URL = '/' + SmilesDjangoPortalConfig.name + '/comp-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        result_dp = smiles_dp_util.create_smiles_data_product(extract_request_data(request),
                                                              smiles_dp_util.SmilesDP.COMPUTATIONAL, data)
        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get_one(self, request, dp_id):
        try:
            result = smiles_dp_util.get_smiles_data_product(extract_request_data(request), dp_id,
                                                            smiles_dp_util.SmilesDP.COMPUTATIONAL)
            return JsonResponse(result, status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def get(self, request):
        page = int(request.GET.get("page", 1))
        size = int(request.GET.get("size", 20))
        result = smiles_dp_util.get_smiles_data_products(
            extract_request_data(request),
            smiles_dp_util.SmilesDP.COMPUTATIONAL,
            page,
            size
        )
        return JsonResponse(result, safe=False, status=200)    
    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = smiles_dp_util.update_smiles_data_product(extract_request_data(request), dp_id,
                                                                   smiles_dp_util.SmilesDP.COMPUTATIONAL, data)
            if updated_dp:
                return JsonResponse(updated_dp, status=200)
            else:
                return JsonResponse({'message': f'Error updating computational data product with ID {dp_id}'},
                                    status=500)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def delete(self, request, dp_id):
        try:
            smiles_dp_util.delete_smiles_data_product(extract_request_data(request), dp_id)
            return HttpResponse()
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def upload(self, request):
        upload_smile_dps(request, smiles_dp_util.SmilesDP.COMPUTATIONAL)
        # accepted response
        return HttpResponse('File uploaded and processed successfully.', status=202)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.path.rstrip('/') == self.UPLOAD_URL:
            return self.upload(request)
        elif request.method == 'GET' and 'dp_id' in kwargs:
            return self.get_one(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)


ComputationalDPView = login_required(ComputationalDPView.as_view())


class ExperimentalDPView(View):
    UPLOAD_URL = '/' + SmilesDjangoPortalConfig.name + '/exp-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        result_dp = smiles_dp_util.create_smiles_data_product(extract_request_data(request),
                                                              smiles_dp_util.SmilesDP.EXPERIMENTAL, data)

        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get_one(self, request, dp_id):
        try:
            result = smiles_dp_util.get_smiles_data_product(extract_request_data(request), dp_id,
                                                            smiles_dp_util.SmilesDP.EXPERIMENTAL)
            return JsonResponse(result, status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def get(self, request):
        page = int(request.GET.get("page", 1))
        size = int(request.GET.get("size", 20))
        result = smiles_dp_util.get_smiles_data_products(
            extract_request_data(request),
            smiles_dp_util.SmilesDP.EXPERIMENTAL,
            page,
            size
        )
        return JsonResponse(result, safe=False, status=200)
    
    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = smiles_dp_util.update_smiles_data_product(extract_request_data(request), dp_id,
                                                                   smiles_dp_util.SmilesDP.EXPERIMENTAL, data)
            if updated_dp:
                return JsonResponse(updated_dp, status=200)
            else:
                return JsonResponse({'message': f'Error updating experimental data product with ID {dp_id}'},
                                    status=500)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def delete(self, request, dp_id):
        try:
            smiles_dp_util.delete_smiles_data_product(extract_request_data(request), dp_id)
            return HttpResponse()
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def upload(self, request):
        upload_smile_dps(request, smiles_dp_util.SmilesDP.EXPERIMENTAL)

        # accepted response
        return HttpResponse('File uploaded and processed successfully.', status=202)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.path.rstrip('/') == self.UPLOAD_URL:
            return self.upload(request)
        elif request.method == 'GET' and 'dp_id' in kwargs:
            return self.get_one(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)


ExperimentalDPView = login_required(ExperimentalDPView.as_view())


class LiteratureDPView(View):
    UPLOAD_URL = '/' + SmilesDjangoPortalConfig.name + '/lit-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        result_dp = smiles_dp_util.create_smiles_data_product(extract_request_data(request),
                                                              smiles_dp_util.SmilesDP.LITERATURE, data)

        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get_one(self, request, dp_id):
        try:
            result = smiles_dp_util.get_smiles_data_product(extract_request_data(request), dp_id,
                                                            smiles_dp_util.SmilesDP.LITERATURE)
            return JsonResponse(result, status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))
    
    def get(self, request):
        page = int(request.GET.get("page", 1))
        size = int(request.GET.get("size", 20))
        result = smiles_dp_util.get_smiles_data_products(
            extract_request_data(request),
            smiles_dp_util.SmilesDP.LITERATURE,
            page,
            size
        )
        return JsonResponse(result, safe=False, status=200)
    
    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = smiles_dp_util.update_smiles_data_product(extract_request_data(request), dp_id,
                                                                   smiles_dp_util.SmilesDP.LITERATURE, data)
            if updated_dp:
                return JsonResponse(updated_dp, status=200)
            else:
                return JsonResponse({'message': f'Error updating literature data product with ID {dp_id}'},
                                    status=500)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def delete(self, request, dp_id):
        try:
            smiles_dp_util.delete_smiles_data_product(extract_request_data(request), dp_id)
            return HttpResponse()
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def upload(self, request):
        upload_smile_dps(request, smiles_dp_util.SmilesDP.LITERATURE)

        # accepted response
        return HttpResponse('File uploaded and processed successfully.', status=202)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.path.rstrip('/') == self.UPLOAD_URL:
            return self.upload(request)
        elif request.method == 'GET' and 'dp_id' in kwargs:
            return self.get_one(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)


LiteratureDPView = login_required(LiteratureDPView.as_view())


@login_required()
def home(request):
    return render(request, "smiles/application.html", {
        'project_name': "SMILES Django Portal"
    })


@login_required
def dp_list(request):
    return render(request, "smiles/application.html", {
        'project_name': "SMILES Django Portal"
    })


def upload_smile_dps(request, dp_type):
    file = request.FILES['file']
    if file.size > settings.FILE_UPLOAD_MAX_FILE_SIZE:
        return HttpResponseBadRequest('File too large')
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    filename = fs.save(file.name, file)
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    request_data = extract_request_data(request)
    old_schema_param = request.GET.get('oldSchema', 'false').lower()
    if old_schema_param == 'true':
        smiles_data_migration.migrate_smiles_dps(request_data, file_path, dp_type.value)
    else:
        smiles_dp_util.upload_smiles_data_products.delay(request_data, file_path, dp_type.value)


def extract_request_data(request):
    groups_response = my_groups(request)
    groups_list = json.loads(groups_response.content)
    return {
        'user_id': request.user.username + "@smiles",#airavataInternalUserId
        'tenant_id': "demotenant",
        'group_ids': groups_list
    }

@login_required
def search_users_groups(request):
    search_type = request.GET.get("type", "").strip().lower()  # user/group/...
    query = request.GET.get("query", "").strip().lower()

    service = AiravataPortalAPIService(request)

    resp_data = {
        "users": [],
        "groups": []
    }
    if search_type in ("user", ""):
        all_users = service.get_user_profiles()
        if query:
            def user_matches(u):
                combined = (
                    f"{u.get('firstName','')} "
                    f"{u.get('lastName','')} "
                    f"{u.get('userId','')} "
                    f"{u.get('airavataInternalUserId','')}"
                ).lower()
                return query in combined
            filtered_users = [u for u in all_users if user_matches(u)]
        else:
            filtered_users = all_users

        user_list = []
        for u in filtered_users:
            display_name = (f"{u.get('firstName','')} {u.get('lastName','')}".strip()) or u.get('userId', 'unknown-user')
            user_id = u.get('airavataInternalUserId', '')
            user_list.append({
                "id": user_id,         # internalUserId
                "name": display_name
            })
        resp_data["users"] = user_list

    if search_type in ("group", ""):
        all_groups_response = service.get_groups()
        groups_list = all_groups_response.get("results", [])

        if query:
            def group_matches(g):
                combined = (
                    f"{g.get('name','')} "
                    f"{g.get('id','')}"
                ).lower()
                return query in combined
            filtered_groups = [g for g in groups_list if group_matches(g)]
        else:
            filtered_groups = groups_list

        group_list = []
        for g in filtered_groups:
            group_list.append({
                "id": g.get("id", ""),
                "name": g.get("name", "")
            })
        resp_data["groups"] = group_list

    return JsonResponse(resp_data)

@login_required
def my_groups(request):
    if not hasattr(request, 'profile_service'):
        logger.error("No profile_service found in request; possibly the middleware is missing.")
        return HttpResponseForbidden("Profile service unavailable.")

    group_manager_client = request.profile_service.get('group_manager')
    if not group_manager_client:
        logger.error("No group_manager found in profile_service.")
        return HttpResponseForbidden("Group manager client not available.")

    user_name = request.user.username + "@" + settings.GATEWAY_ID

    user_groups = group_manager_client.getAllGroupsUserBelongs(
        request.authz_token,
        user_name
    )

    group_ids = []
    for grp in user_groups:
        group_ids.append(grp.name)

    return JsonResponse(group_ids, safe=False)

@csrf_exempt
@login_required
def share_data_product(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed")

    body = json.loads(request.body)
    data_product_ids = body.get("data_product_ids", [])
    share_type = body.get("share_type")
    share_target = body.get("share_target")

    if not data_product_ids:
        return HttpResponseBadRequest("No data_product_ids provided")

    if share_type not in ("user", "group"):
        return HttpResponseBadRequest("Invalid share_type")

    request_data = {
        "user_id": request.user.username + "@smiles",
        "tenant_id": "demotenant"
    }
    catalog_service = DataCatalogService(request_data)

    if share_type == "user":
        user_ids = [share_target]
        group_ids = []
    else:
        user_ids = []
        group_ids = [share_target]

    try:
        for dp_id in data_product_ids:
            for u in user_ids:
                catalog_service.grant_permission_to_user(
                    target_user_id=u,
                    data_product_id=dp_id,
                    permission=pb2.READ
                )
            for g in group_ids:
                catalog_service.grant_permission_to_group(
                    target_group_id=g,
                    data_product_id=dp_id,
                    permission=pb2.READ
                )
    except grpc.RpcError as e:
        if e.code() == StatusCode.PERMISSION_DENIED:
            return HttpResponseForbidden("You do not have the OWNER or MANAGE_SHARING permission to share this data product.")
        else:
            return HttpResponseBadRequest(f"Error sharing data product: {e.details()}")

    return JsonResponse({"status": "ok", "data_product_ids": data_product_ids})
