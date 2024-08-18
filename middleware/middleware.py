from accounts.repository.accounts_repository import AccountsRepository
from common.utils import jwt_decoder, logger
from django.http import JsonResponse
import jwt

class JwtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_routes = ["/accounts/create", "/accounts/login"]
        special_routes = ["/accounts/resend_email", "validate"]

        found_user = None
        jwt_token = None

        if special_routes[1] in request.path:
            return self.get_response(request)

        if request.path not in public_routes:
            if "authorization" not in request.headers:
                logger.info(f"Failed to find a JWT token in '{request.headers}' at JwtMiddleware.")
                return JsonResponse({"message": "Invalid Token Error: Token Not Found."}, status=401)

            try:
                jwt_token = jwt_decoder(request.headers.get("authorization"))

            except jwt.InvalidTokenError:
                logger.info(f"Error {jwt.InvalidTokenError}, invalid token '{request.headers.get('authorization')}' provided at JwtMiddleware.")
                return JsonResponse({"message": "Invalid Token Error."}, status=401)

            found_user = AccountsRepository.get_by_email(jwt_token.get("email"))
            if not found_user:
                return JsonResponse(
                    {"message": f"Invalid User Error: User '{jwt_token.get('email')}' not found."}, 
                    status=400
                )
            if not found_user.email_is_validated and request.path not in special_routes[0]:
                return JsonResponse({"message": "Invalid Request Error: Account Not Validated."}, status=401)

        request.jwt_token = jwt_token
        request.found_user = found_user
        return self.get_response(request)
