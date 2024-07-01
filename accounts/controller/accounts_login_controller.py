from ..repository.accounts_repository import AccountsRepository
from django.views.decorators.http import require_http_methods
from common.utils import jwt_encoder, logger, json_validator
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from django.http import JsonResponse


@require_http_methods(["POST"])
def login(request):
    request_response = json_validator(request.body)
    valid_password = None
    
    if not request_response:
        return JsonResponse({"message": "Invalid JSON error"}, status=400)

    if "email" not in request_response or "password" not in request_response:
        logger.info(f"Parameter 'Email' or 'Password' not found in: {request_response}.")
        return JsonResponse({"message": "Invalid Fields Error: Email and Password are required."}, status=400)

    found_user = AccountsRepository.get_by_email(request_response['email'])
    if not found_user:
        return JsonResponse({"message": f"Invalid User Error: User '{request_response['email']}' Not Found."}, status=400)


    try:
       valid_password = check_password(request_response.get("password"), found_user.password)

    except Exception as error:
        logger.info(f"Failed to hash password due to error: '{error}' at accounts_login_controller.")
        return JsonResponse({"message": "Invalid Password Error: Failed due to internal error."}, status=500)
    
    if not valid_password:
        return JsonResponse({"message": "Invalid User Error: Invalid Password."}, status=401)
    

    jwt_token = jwt_encoder(
        email=request_response['email'],
        iat=datetime.now(),
        exp=datetime.now() + timedelta(minutes=15)
    )

    logger.info(f"User '{request_response['email']}' logged in at accounts_login_controller/login.")
    return JsonResponse({"message": jwt_token}, status=200)
