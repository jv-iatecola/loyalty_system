from django.views.decorators.http import require_http_methods
from ..repository.stores_repository import StoresRepository
from common.utils import json_validator, logger
from django.http import JsonResponse
from datetime import datetime


@require_http_methods(["POST"])
def create(request):
    found_user = request.found_user

    request_response = json_validator(request.body)
    if not request_response:
        return JsonResponse({"message": "Invalid JSON error"}, status=400)

    if 'store_name' not in request_response:
        logger.info(f"Parameter 'store_name' not found in '{request_response}' at Stores Create Controller.")
        return JsonResponse({"message": 'Invalid Fields Error: "store_name" Not Found.'}, status=400)
    
    found_store = StoresRepository.get_by_store_name(request_response['store_name'])
    if found_store:
        return JsonResponse({"message": 'Invalid Store Error: Store Already Exists.'}, status=400)

    store = StoresRepository.create(
        store_name=request_response['store_name'],
        accounts=found_user
    )

    return JsonResponse({"message": f"Store '{store.store_name}' created Successfully!"}, status=200)
