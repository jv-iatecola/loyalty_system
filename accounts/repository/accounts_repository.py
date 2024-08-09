from accounts.models import Accounts
from common.utils import logger
from uuid import uuid4


class AccountsRepository:
    
    @staticmethod
    def create(*args, **kwargs):
        email_is_validated = False
        
        try:
            email_is_validated = kwargs.pop("email_is_validated")
            
        except Exception as error:
            logger.info(f"Failed to retrieve 'email_is_validated' from {kwargs}, error: '{error}', at AccountsRepository/create.")
            email_is_validated = False

        accounts = Accounts(*args, **kwargs, id=str(uuid4()), email_is_validated=email_is_validated)
        accounts.save()
        logger.info(f"Account created for user '{accounts.email}', id '{accounts.id}' at AccountsRepository/create.")
        return accounts
    

    @staticmethod
    def get_by_email(email):
        try:
            found_user = Accounts.objects.get(email=email)
            logger.info(f"Found user '{found_user.id}' with email '{email}' at AccountsRepository/get_by_email.")
            return found_user
        
        except Accounts.DoesNotExist:
            logger.info(f"Failed to find a user with the email '{email}' at AccountsRepository/get_by_email.")
            return False


    @staticmethod
    def get_by_id(id):
        try:
            found_user = Accounts.objects.get(id=id)
            logger.info(f"Found user '{found_user.id}' with id '{id}' at AccountsRepository/get_by_id.")
            return found_user
        
        except Accounts.DoesNotExist:
            logger.info(f"Failed to find a user with the id '{id}' at AccountsRepository/get_by_id.")
            return False
