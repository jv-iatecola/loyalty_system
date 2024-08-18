from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

@require_http_methods(["GET"])
def verify(request):
    found_user = request.found_user

    return JsonResponse({"message": f"Account '{found_user.id}' already validated."}, status=200)
