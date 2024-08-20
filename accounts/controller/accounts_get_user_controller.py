from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

@require_http_methods(["GET"])
def get_user(request):
    found_user = request.found_user

    response_data = {}
    response_data['id'] = found_user.id
    response_data['username'] = found_user.username
    response_data['email'] = found_user.email

    return JsonResponse({"data": response_data}, status=200)
