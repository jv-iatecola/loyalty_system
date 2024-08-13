from stores.models import Stores
from common.utils import logger
from datetime import datetime
from uuid import uuid4


class StoresRepository:

    @staticmethod
    def create(*args, **kwargs):
        store = Stores(*args, **kwargs, created_at=datetime.now(), id=str(uuid4()))
        store.save()
        logger.info(f"Store '{store.store_name}' created by user '{store.accounts}' at StoresRepository/create.")
        return store
    
    @staticmethod
    def get_by_store_name(store_name):
        try:
            found_store = Stores.objects.get(store_name=store_name)
            logger.info(f"Found Store '{found_store.id}' with the name '{store_name}' at StoresRepository/get_by_store_name.")
            return found_store
        
        except:
            logger.info(f"Failed to find a Store by the name '{store_name}' at StoresRepository/get_by_store_name.")
            return False

    @staticmethod
    def get_by_user_id(user_id):
        try:
            found_store = Stores.objects.filter(accounts_id=user_id)[0]
            logger.info(f"Found Store '{found_store.id}' for the user's id '{user_id}' at StoresRepository/get_by_user_id.")
            return found_store
        
        except Exception as error:
            logger.info(f"Failed to find a Store by the user '{user_id}', error '{error}' at StoresRepository/get_by_user_id.")
            return False

    @staticmethod
    def get_all_by_user_id(user_id):
        try:
            found_stores = list(Stores.objects.filter(accounts_id=user_id).values())
            logger.info(f"Found '{len(found_stores)}' Store(s) for the user's id '{user_id}' at StoresRepository/get_all_by_user_id.")
            return found_stores
        
        except Exception as error:
            logger.info(f"Failed to find a Store by the user '{user_id}', error '{error}' at StoresRepository/get_all_by_user_id.")
            return False
        
    @staticmethod
    def get_by_store_id(store_id):
        try:
            found_store = Stores.objects.get(id=store_id)
            logger.info(f"Found Store '{found_store.id}' at StoresRepository/get_by_store_id.")
            return found_store
        
        except Exception as error:
            logger.info(f"Failed to find a Store with the id '{store_id}', error '{error}' at StoresRepository/get_by_store_id.")
            return False
