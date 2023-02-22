import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .proto import computational_dp_pb2
from django.utils.decorators import method_decorator

from . import computational_data_util as comp_util
from . import data_catalog_service as dcs


@method_decorator(csrf_exempt, name='dispatch')
class ComputationalDPView(View):

    def post(self, request):
        data = json.loads(request.body)
        computational_dp = computational_dp_pb2.ComputationalDP(**data)
        create_computational_data_product(computational_dp)

        return JsonResponse({'status': 'success'})


def create_computational_data_product(computational_dp: computational_dp_pb2.ComputationalDP()):
    data_product = comp_util.map_computational_dp_to_catalog_dp(computational_dp)
    catalog_service = dcs.DataCatalogService()
    result_dp = catalog_service.create_data_product(data_product)

    return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)
