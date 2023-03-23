import json
import os
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import smiles_dp_util
from data_catalog.smiles_dp_util import SmilesDP


@method_decorator(csrf_exempt, name='dispatch')
class ComputationalDPView(View):
    UPLOAD_URL = 'smiles/computational-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        result_dp = smiles_dp_util.create_smiles_data_product(SmilesDP.COMPUTATIONAL, data)

        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get(self, request, dp_id):
        try:
            result_json_dp = smiles_dp_util.get_smiles_data_product(dp_id, SmilesDP.COMPUTATIONAL)
            return JsonResponse(json.loads(result_json_dp), status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = smiles_dp_util.update_smiles_data_product(dp_id, SmilesDP.COMPUTATIONAL, data)
            if updated_dp:
                return JsonResponse(json.loads(updated_dp), status=200)
            else:
                return JsonResponse({'message': f'Error updating computational data product with ID {dp_id}'},
                                    status=500)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def delete(self, request, dp_id):
        try:
            smiles_dp_util.delete_smiles_data_product(dp_id)
            return HttpResponse()
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def upload(self, request):
        upload_smile_dps(request, SmilesDP.COMPUTATIONAL)
        # accepted response
        return HttpResponse('File uploaded and processed successfully.', status=202)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.path == '/' + self.UPLOAD_URL and request.FILES.get('file'):
            return self.upload(request)
        else:
            return super().dispatch(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class ExperimentalDPView(View):
    UPLOAD_URL = 'smiles/experimental-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        result_dp = smiles_dp_util.create_smiles_data_product(SmilesDP.COMPUTATIONAL, data)

        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get(self, request, dp_id):
        try:
            result_json_dp = smiles_dp_util.get_smiles_data_product(dp_id, SmilesDP.COMPUTATIONAL)
            return JsonResponse(json.loads(result_json_dp), status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = smiles_dp_util.update_smiles_data_product(dp_id, SmilesDP.COMPUTATIONAL, data)
            if updated_dp:
                return JsonResponse(json.loads(updated_dp), status=200)
            else:
                return JsonResponse({'message': f'Error updating experimental data product with ID {dp_id}'},
                                    status=500)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def delete(self, request, dp_id):
        try:
            smiles_dp_util.delete_smiles_data_product(dp_id)
            return HttpResponse()
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def upload(self, request):
        upload_smile_dps(request, SmilesDP.COMPUTATIONAL)

        # accepted response
        return HttpResponse('File uploaded and processed successfully.', status=202)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.path == '/' + self.UPLOAD_URL and request.FILES.get('file'):
            return self.upload(request)
        else:
            return super().dispatch(request, *args, **kwargs)


class LiteratureDPView(View):
    UPLOAD_URL = 'smiles/literature-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        result_dp = smiles_dp_util.create_smiles_data_product(SmilesDP.LITERATURE, data)

        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get(self, request, dp_id):
        try:
            result_json_dp = smiles_dp_util.get_smiles_data_product(dp_id, SmilesDP.LITERATURE)
            return JsonResponse(json.loads(result_json_dp), status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = smiles_dp_util.update_smiles_data_product(dp_id, SmilesDP.LITERATURE, data)
            if updated_dp:
                return JsonResponse(json.loads(updated_dp), status=200)
            else:
                return JsonResponse({'message': f'Error updating literature data product with ID {dp_id}'},
                                    status=500)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def delete(self, request, dp_id):
        try:
            smiles_dp_util.delete_smiles_data_product(dp_id)
            return HttpResponse()
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def upload(self, request):
        upload_smile_dps(request, SmilesDP.LITERATURE)

        # accepted response
        return HttpResponse('File uploaded and processed successfully.', status=202)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.path == '/' + self.UPLOAD_URL and request.FILES.get('file'):
            return self.upload(request)
        else:
            return super().dispatch(request, *args, **kwargs)


def upload_smile_dps(request, dp_type):
    file = request.FILES['file']
    if file.size > settings.MAX_UPLOAD_SIZE:
        return HttpResponseBadRequest('File too large')
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    filename = fs.save(file.name, file)
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    smiles_dp_util.upload_smiles_data_products.delay(file_path, dp_type)