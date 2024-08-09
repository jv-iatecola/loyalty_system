from django.views.decorators.http import require_http_methods
from ..repository.stores_repository import StoresRepository
from django.http import JsonResponse

@require_http_methods(["GET"])
def stores_get(request):
    found_user = request.found_user
    found_stores = StoresRepository.get_all_by_user_id(found_user.id)
    if not found_stores:
        return JsonResponse({"message": f"Failed to find Stores for the user {found_user}."}, status=400)

    return JsonResponse({"data": found_stores}, status=200)
