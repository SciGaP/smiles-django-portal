import json
from django.http import JsonResponse
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
