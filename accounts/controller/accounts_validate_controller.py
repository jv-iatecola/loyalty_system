from accounts.repository.accounts_repository import AccountsRepository
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from common.utils import logger
from datetime import datetime
from base64 import b64decode
from ast import literal_eval


@require_http_methods(["GET"])
def validate(request, hashed_data):
    data_content = None
    try:
        data_content = literal_eval((b64decode(hashed_data)).decode())

    except Exception as error:
        logger.info(f"Failed to consume data due to error: '{error}' at accounts_validate_controller.")
        return JsonResponse({"message": "Invalid Request Error"}, status=500)

    found_user = AccountsRepository.get_by_id(data_content.get('id'))
    print("FOUND USER", found_user)
    if not found_user:
        return JsonResponse({"message": f"Invalid User Error: User '{data_content.get('id')}' not found."}, status=400)

    if found_user.email_is_validated:
        return JsonResponse({"message": f"Invalid Request Error: User '{data_content.get('id')}' Already Validated."}, status=400)

    if str(datetime.now().time()) > data_content.get('exp'):
        logger.info(f"Failed to validate user '{data_content.get('id')}' datetime.now param: '{str(datetime.now().time())}', exp param: '{data_content.get('exp')}' at accounts_validate_controller.")
        return JsonResponse({"message": f"Invalid Date Parameter Error: Date '{data_content.get('exp')}' has expired."}, status=400)

    found_user.email_is_validated = True
    found_user.save()

    return JsonResponse({"message": "Your account was validated successfully!!!"}, status=200)
