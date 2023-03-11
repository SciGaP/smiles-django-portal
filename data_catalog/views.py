import json
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .proto import computational_dp_pb2
from django.utils.decorators import method_decorator

from . import computational_data_util as comp_util


@method_decorator(csrf_exempt, name='dispatch')
class ComputationalDPView(View):

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
