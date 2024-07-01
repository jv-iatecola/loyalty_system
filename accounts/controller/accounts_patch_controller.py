from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from common.utils import logger


@require_http_methods(["PATCH"])
def patch(request):
    queryparameters = request.GET.copy()
    found_user = request.found_user

    if "new_username" not in queryparameters:
        logger.info(f"Parameter 'new_username' not found in {queryparameters} at accounts_patch_controller.")
        return JsonResponse({"message": "Invalid Request Error: Parameter 'new_username' is required."}, status=400)
    
    new_username = queryparameters.get("new_username")
    if new_username == found_user.username:
        return JsonResponse({"message": f"Invalid Request Error: Username '{new_username}' already provided for this account."}, status=400)


    old_username = found_user.username
    found_user.username = new_username
    found_user.save()

    logger.info(
        f"Username '{old_username}' updated to '{new_username}' for user '{found_user.id}' at accounts_patch_controller."
    )

    return JsonResponse({"message": "Username updated successfully!"}, status=200)
