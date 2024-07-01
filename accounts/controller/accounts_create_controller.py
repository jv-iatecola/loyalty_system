from common.utils import json_validator, logger, validate_email, hash_data, jwt_encoder
from ..repository.accounts_repository import AccountsRepository
from django.views.decorators.http import require_http_methods
from provider.mail_provider import send_email
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password


@require_http_methods(["POST"])
def create(request):
    request_response = json_validator(request.body)
    if not request_response:
        return JsonResponse({"message": "Invalid JSON error"}, status=400)

    if "email" not in request_response or "password" not in request_response or "username" not in request_response:
        logger.info(f"Parameter 'Email', 'Password' or 'Username' not found in: {request_response}. at accounts_create_controller.")
        return JsonResponse({"message": 'Invalid Fields Error: Email, Password and Username are required.'}, status=400)

    validated_email = validate_email(request_response.get("email"))
    if not validated_email:
        return JsonResponse({"message": "Invalid Email Error: Enter a valid email address"}, status=400)

    found_user = AccountsRepository.get_by_email(request_response.get("email"))
    if found_user:
        return JsonResponse({"message": f"Invalid User Error: User '{request_response.get('email')}' already exists."}, status=400)

    jwt_token = jwt_encoder(email=request_response['email'], iat=datetime.now(), exp=datetime.now() + timedelta(minutes=15))

    try:
        password = make_password(request_response.get("password"))

    except Exception as error:
        logger.info(f"Failed to hash password due to error: '{error}' at accounts_create_controller.")
        return JsonResponse({"message": "Invalid Password Error: Failed due to internal error."}, status=500)

    accounts = AccountsRepository.create(
        email=request_response.get("email"), 
        password=password, 
        username=request_response.get("username")
    )
    hashed_data = hash_data(accounts.id)
    if not hashed_data:
        return JsonResponse({"message": "Account created successfully, but failed to send a validation email."}, status=500)

    sent_email = send_email(
        {
            "sendto": accounts.email, 
            "name": accounts.username, 
            "body": f"Please click on the link below to validate your new Django's Loyalty System Account: \nhttp://localhost:8000/accounts/validate/{hashed_data}."
        }
    )

    if sent_email.get("error"):
        logger.info(f"Failed to send a validation email to '{accounts.email}' at accounts_create_controller.")
        return JsonResponse({"message": "Account created successfully, but failed to send a validation email."}, status=500)

    logger.info(f"Email sent successfully to '{accounts.email}' at provider/mail_provider.")

    return JsonResponse({"message": jwt_token})
