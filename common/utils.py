from django.core.validators import EmailValidator
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from base64 import b64encode
import logging
import json
import uuid
import jwt

logger = logging.getLogger("default_logger")

def json_validator(json_data):
    try:
        json_validator_response = json.loads(json_data)
        return json_validator_response
    
    except Exception as error:
        logger.info(f"Failed to decode '{json_data}', error '{error}' at common/utils/json_validator.")
        return None

def make_pagination(found_items, per_page, page_number):
    paginator = Paginator(found_items, per_page)
    next_page = None

    results = paginator.page(page_number).object_list
    page = paginator.get_page(page_number)

    if page.has_next():
        next_page = page.next_page_number()

    logger.info(
        f"Found '{len(results)}' items, '{per_page}' per page, Max Page: {paginator.num_pages} at common/utils/make_pagination."
    )

    return {
        "results": results,
        "max_page": paginator.num_pages,
        "current_page": int(page_number),
        "next_page": next_page,
        "per_page": int(per_page)
    }

def make_filter(kwargs):
    if 'from' in kwargs and 'until' in kwargs:
        return {"created_at__range": (kwargs.pop('from')[0], kwargs.pop('until')[0])}
    
    if 'from' in kwargs:
        return {"created_at__gte": kwargs.pop('from')[0]}
    
    if 'until' in kwargs:
        return {"created_at__lte": kwargs.pop('until')[0]}

def validate_email(email):
    email_validator = EmailValidator()
    try:
        email_validator(email)
        return email
    except Exception:
        logger.info(f"Failed to validate email '{email}' at common/utils/validate_email.")
        return False

def jwt_encoder(**kwargs):
    email = kwargs.pop("email")
    iat = kwargs.pop("iat")
    exp = kwargs.pop("exp")

    jwt_token = jwt.encode(
        {
            "email": email,
            "iat": iat,
            "exp": exp
        },
        "token_secret",
        algorithm="HS256"
    )
    return jwt_token

def jwt_decoder(jwt_token):
    return jwt.decode(jwt_token, "token_secret", algorithms="HS256")

def hash_data(id):
    try:
        exp = exp=datetime.now() + timedelta(minutes=15)

        json_str = json.dumps({
            "id": id,
            "exp": str(exp.time())
        })

    except:
        logger.info("Failed to parse data at common/utils/hash_data.")
        return False

    return b64encode(json_str.encode()).decode()

def uuid_validator(store_id):
    try:
        isvalidUuid = uuid.UUID(store_id, version=4)
        return isvalidUuid

    except Exception as error:
        logger.info(f"Failed to validate data '{store_id}' in 'store_id' param at common/utils/uuid_validator.")
        return False
