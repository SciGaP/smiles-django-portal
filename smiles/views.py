import json
import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import smiles_dp_util
from . import smiles_data_migration
from django.shortcuts import render
from .apps import SmilesDjangoPortalConfig


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
    return {
        'user_id': str(request.user.id),
        'tenant_id': "demotenant"
    }
