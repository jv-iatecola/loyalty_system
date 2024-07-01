from accounts.repository.accounts_repository import AccountsRepository
from vouchers.repository.vouchers_repository import VoucherRepository
from stores.repository.stores_repository import StoresRepository
from django.views.decorators.http import require_http_methods
from common.utils import json_validator, logger
from django.http import JsonResponse


@require_http_methods(["POST"])
def create(request):
    found_user = request.found_user
    request_response = json_validator(request.body)
    if not request_response:
        return JsonResponse({"message": "Invalid JSON error"}, status=400)    
    
    if "email" not in request_response:
        logger.info(f"Email not found in '{request_response}' at Vouchers Create Controller.")
        return JsonResponse({"message": "Invalid Fields Error: 'email' is required."}, status=400)
    
    if "store_id" not in request_response:
    
        found_store = StoresRepository.get_by_user_id(found_user.id)
        if not found_store:
            return JsonResponse({"message": "Invalid Store Error: Store Not Found."}, status=400)
        
    else:    
        found_store = StoresRepository.get_by_store_id(request_response.get("store_id"))
        if not found_store:
            return JsonResponse({"message": "Invalid Store Error: Store Not Found."}, status=400)
        
    found_requester = AccountsRepository.get_by_email(request_response.get('email'))
    if not found_requester:
        return JsonResponse({"message": f"Invalid User Error: Requester '{request_response.get('email')}' not found."}, status=400)

    voucher = VoucherRepository.create(
        accounts=found_requester,
        stores=found_store
    )


    return JsonResponse({"message": "Voucher generated successfully!"}, status=200)
