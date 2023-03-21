import json
import os
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .proto import computational_dp_pb2
from .util import computational_data_util as comp_util


@method_decorator(csrf_exempt, name='dispatch')
class ComputationalDPView(View):
    UPLOAD_URL = 'smiles/computational-dp/upload'

    def post(self, request):
        data = json.loads(request.body)
        computational_dp = computational_dp_pb2.ComputationalDP(**data)
        result_dp = comp_util.create_computational_data_product(computational_dp)

        return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)

    def get(self, request, dp_id):
        try:
            result_json_dp = comp_util.get_computational_data_product(dp_id)
            return JsonResponse(json.loads(result_json_dp), status=200)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def put(self, request, dp_id):
        data = json.loads(request.body)
        try:
            updated_dp = comp_util.update_computational_data_product(data, dp_id)
            if updated_dp:
                return JsonResponse(json.loads(updated_dp), status=200)
            else:
                return JsonResponse({'message': f'Error updating computational data product with ID {dp_id}'},
                                    status=500)
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def delete(self, request, dp_id):
        try:
            comp_util.delete_computational_data_product(dp_id)
            return HttpResponse()
        except Exception as e:
            return HttpResponseNotFound(str(e))

    def upload(self, request):
        file = request.FILES['file']
        if file.size > settings.MAX_UPLOAD_SIZE:
            return HttpResponseBadRequest('File too large')
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(file.name, file)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        comp_util.upload_computational_data_products.delay(file_path)

        # accepted response
        return HttpResponse('File uploaded and processed successfully.', status=202)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.path == '/' + self.UPLOAD_URL and request.FILES.get('file'):
            return self.upload(request)
        else:
            return super().dispatch(request, *args, **kwargs)
