from accounts.repository.accounts_repository import AccountsRepository
from common.utils import json_validator, logger, validate_email
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

@require_http_methods(["PUT"])
def put(request):
    found_user = request.found_user
    request_response = json_validator(request.body)
    password = None
    
    if not request_response:
        return JsonResponse({"message": "Invalid JSON error"}, status=400)

    validated_email = validate_email(request_response.get("email"))
    if not validated_email:
        return JsonResponse({"message": "Invalid Email Error: Enter a valid email address"}, status=400)

    found_user_with_request_email = AccountsRepository.get_by_email(request_response.get('email'))
    if found_user_with_request_email:
        logger.info(
            f"Email '{found_user_with_request_email.email}' already taken by user '{found_user_with_request_email.id}' at accounts_put_controller."
        )
        return JsonResponse(
            {"message": f"Invalid Email Error: Email '{request_response.get('email')}' is not valid."},
            status=400
        )

    if "email" in request_response:
        found_user.email = request_response.get("email")
        logger.info(f"Email updated for user '{found_user.id}' at accounts_put_controller.")

    if "username" in request_response:
        found_user.username = request_response.get("username")
        logger.info(f"Username updated for user '{found_user.id}' at accounts_put_controller.")

    if "password" in request_response:
        try:
            password = make_password(request_response.get("password"))
            found_user.password = password
            logger.info(f"Password updated for user '{found_user.id}' at accounts_put_controller.")

        except Exception as error:
            logger.info(f"Failed to hash password due to error: '{error}' at accounts_put_controller.")
            return JsonResponse({"message": "Invalid Password Error: Failed due to an internal error."}, status=500)

    found_user.save()

    return JsonResponse({"message": "User updated successfully!"})
