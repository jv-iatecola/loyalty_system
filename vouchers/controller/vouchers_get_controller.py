from vouchers.repository.vouchers_repository import VoucherRepository
from django.views.decorators.http import require_http_methods
from common.utils import logger, uuid_validator
from django.http import JsonResponse
from datetime import datetime

allowed_filters = ['from', 'until', 'stores_id', 'order_by', 'page', 'perPage']
allowed_orders = ['id', 'created_at', 'accounts_id', 'stores_id']

@require_http_methods(["GET"])
def vouchers_get(request):
    query_parameters = request.GET.copy()
    found_user = request.found_user

    if len(query_parameters) == 0:
        response = VoucherRepository.get_by_user_id(found_user.id)
        return JsonResponse({"data": response}, status=200)

    for parameter in query_parameters.keys():
        if parameter not in allowed_filters:
            logger.info(f"The invalid parameter '{parameter}' was given in '{query_parameters}' at Vouchers Get Controller.")
            return JsonResponse({"message": f"Parameter '{parameter}' is not allowed, the allowed parameters are: {allowed_filters}."}, status=400)

    if 'from' in query_parameters:
        try:
            datetime.strptime(query_parameters.get('from'), "%Y-%m-%d")

        except ValueError:
            logger.info(f"The invalid 'from' parameter '{query_parameters.get('from')}' was given at Vouchers Get Controller.")
            return JsonResponse({"message": f"Pagination by 'from' param: '{query_parameters.get('from')}' is not allowed, please insert a valid date."}, status=400)

    if 'until' in query_parameters:
        try:
            datetime.strptime(query_parameters.get('until'), "%Y-%m-%d")
            
        except ValueError:
            logger.info(f"The invalid 'until' parameter '{query_parameters.get('until')}' was given at Vouchers Get Controller.")
            return JsonResponse({"message": f"Pagination by 'until' param: '{query_parameters.get('until')}' is not allowed, please insert a valid date."}, status=400)

    if 'page' in query_parameters and not query_parameters.get('page').isnumeric():
        logger.info(f"The invalid 'page' parameter '{query_parameters.get('page')}' was given at Vouchers Get Controller.")
        return JsonResponse({"message": f"Pagination by 'page' param:'{query_parameters.get('page')}' is not allowed, please insert a valid number."}, status=400)

    if 'perPage' in query_parameters and not query_parameters.get('perPage').isnumeric():
        logger.info(f"The invalid 'perPage' parameter '{query_parameters.get('perPage')}' was given at Vouchers Get Controller.")
        return JsonResponse({"message": f"Pagination by 'perPage' param:'{query_parameters.get('perPage')}' is not allowed, please insert a valid number."}, status=400)

    if 'order_by' in query_parameters and query_parameters.get('order_by') not in allowed_orders:
        logger.info(f"The invalid 'order_by' parameter '{query_parameters.get('order_by')}' was given at Vouchers Get Controller.")
        return JsonResponse({"message": f"Ordering by '{query_parameters.get('order_by')}' is not allowed, the allowed assortments are: {allowed_orders}."}, status=400)
    
    if 'stores_id' in query_parameters:
        isvalidUuid = uuid_validator(query_parameters.get('stores_id'))
        if not isvalidUuid:
            return JsonResponse({"message": f"Parameter '{query_parameters.get('stores_id')}' in 'stores_id' is not valid."}, status=400)

    response = VoucherRepository.get_by_filters(**query_parameters, user_id=found_user.id)
    return JsonResponse({"data": response}, status=200)
