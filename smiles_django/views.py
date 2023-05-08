import json
import os
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import smiles_dp_util
from django.shortcuts import render
from .apps import SmilesDjangoPortalConfig


@method_decorator(csrf_exempt, name='dispatch')
class ComputationalDPView(View):
    UPLOAD_URL = '/' + SmilesDjangoPortalConfig.name + '/computational-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        result_dp = smiles_dp_util.create_smiles_data_product(request, smiles_dp_util.SmilesDP.COMPUTATIONAL, data)

        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get_one(self, request, dp_id):
        try:
            result = smiles_dp_util.get_smiles_data_product(request, dp_id, smiles_dp_util.SmilesDP.COMPUTATIONAL)
            return JsonResponse(result, status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def get(self, request):
        result = smiles_dp_util.get_smiles_data_products(request, smiles_dp_util.SmilesDP.COMPUTATIONAL)
        return JsonResponse(result, safe=False, status=200)

    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = smiles_dp_util.update_smiles_data_product(request, dp_id,
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
            smiles_dp_util.delete_smiles_data_product(request, dp_id)
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


@method_decorator(csrf_exempt, name='dispatch')
class ExperimentalDPView(View):
    UPLOAD_URL = '/' + SmilesDjangoPortalConfig.name + '/experimental-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        result_dp = smiles_dp_util.create_smiles_data_product(request, smiles_dp_util.SmilesDP.EXPERIMENTAL, data)

        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get_one(self, request, dp_id):
        try:
            result = smiles_dp_util.get_smiles_data_product(request, dp_id, smiles_dp_util.SmilesDP.EXPERIMENTAL)
            return JsonResponse(result, status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def get(self, request):
        result = smiles_dp_util.get_smiles_data_products(request, smiles_dp_util.SmilesDP.EXPERIMENTAL)
        return JsonResponse(result, safe=False, status=200)

    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = smiles_dp_util.update_smiles_data_product(request, dp_id, smiles_dp_util.SmilesDP.EXPERIMENTAL,
                                                                   data)
            if updated_dp:
                return JsonResponse(updated_dp, status=200)
            else:
                return JsonResponse({'message': f'Error updating experimental data product with ID {dp_id}'},
                                    status=500)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def delete(self, request, dp_id):
        try:
            smiles_dp_util.delete_smiles_data_product(request, dp_id)
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


@method_decorator(csrf_exempt, name='dispatch')
class LiteratureDPView(View):
    UPLOAD_URL = '/' + SmilesDjangoPortalConfig.name + '/literature-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        result_dp = smiles_dp_util.create_smiles_data_product(request, smiles_dp_util.SmilesDP.LITERATURE, data)

        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get_one(self, request, dp_id):
        try:
            result = smiles_dp_util.get_smiles_data_product(request, dp_id, smiles_dp_util.SmilesDP.LITERATURE)
            return JsonResponse(result, status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def get(self, request):
        result = smiles_dp_util.get_smiles_data_products(request, smiles_dp_util.SmilesDP.EXPERIMENTAL)
        return JsonResponse(result, safe=False, status=200)

    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = smiles_dp_util.update_smiles_data_product(request, dp_id, smiles_dp_util.SmilesDP.LITERATURE,
                                                                   data)
            if updated_dp:
                return JsonResponse(updated_dp, status=200)
            else:
                return JsonResponse({'message': f'Error updating literature data product with ID {dp_id}'},
                                    status=500)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def delete(self, request, dp_id):
        try:
            smiles_dp_util.delete_smiles_data_product(request, dp_id)
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


def home(request):
    return render(request, "smiles_django/home.html", {
        'project_name': "SMILES Django Portal"
    })


def upload_smile_dps(request, dp_type):
    file = request.FILES['file']
    if file.size > settings.FILE_UPLOAD_MAX_FILE_SIZE:
        return HttpResponseBadRequest('File too large')
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    filename = fs.save(file.name, file)
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    smiles_dp_util.upload_smiles_data_products.delay(file_path, dp_type.value)
