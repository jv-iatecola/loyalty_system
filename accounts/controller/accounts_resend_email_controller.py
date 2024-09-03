from django.views.decorators.http import require_http_methods
from provider.mail_provider import send_email
from common.utils import hash_data, logger
from datetime import datetime, timedelta
from django.http import JsonResponse


@require_http_methods(["GET"])
def resend_email(request):
    found_user = request.found_user

    if found_user.email_is_validated:
        return JsonResponse(
            {"message": f"Invalid Request Error: User '{found_user.id}' Already Validated."},
            status=400
        )

    hashed_data = hash_data(found_user.id)
    if not hashed_data:
        return JsonResponse(
            {"message": "Account created successfully, but failed to send a validation email."},
            status=500
        )
    
    sent_email = send_email({
        "send_to": found_user.email,
        "name": found_user.username,
        "body": f"Please click on the link below to validate your new Django's Loyalty System Account: \n"
                f"https://loyalty-system.onrender.com/accounts/validate/{hashed_data}."
    })

    if not sent_email:
        return JsonResponse({"message": "Failed to send a validation email, try again."}, status=500)

    logger.info(f"Email sent successfully to '{found_user.email}' at provider/mail_provider.")
    
    return JsonResponse(
        {"message": f"Validation email sent successfully to '{found_user.email}'."},
        status=200
    )
