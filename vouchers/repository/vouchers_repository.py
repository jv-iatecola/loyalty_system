from common.utils import logger, make_pagination, make_filter
from vouchers.models import Vouchers
from stores.models import Stores
from datetime import datetime
from uuid import uuid4


class VoucherRepository:

    @staticmethod
    def create(*args, **kwargs):
        voucher = Vouchers(*args, **kwargs, created_at=datetime.now(), id=str(uuid4()))
        voucher.save()
        logger.info(f"Voucher '{voucher.id}' created by '{voucher.accounts}' at VoucherRepository/create.")
        return voucher  
    
    @staticmethod
    def get_by_user_id(id):
        found_vouchers = list(Vouchers.objects.filter(accounts_id=id).values())
        store_ids = [voucher['stores_id'] for voucher in found_vouchers]
        found_stores = list(Stores.objects.filter(id__in=store_ids))
        stores_dict = {store.id: store for store in found_stores}
        updated_vouchers = []

        for voucher in found_vouchers:
            store_id = voucher['stores_id']
            store = stores_dict.get(store_id)
            if store:
                updated_voucher = voucher.copy()
                updated_voucher['store_name'] = store.store_name
                updated_vouchers.append(updated_voucher)

        logger.info(f"Found '{len(updated_vouchers)}' voucher(s) for the user '{id}' at VoucherRepository/get_by_user_id.")
        return updated_vouchers

    @staticmethod
    def get_by_filters(**kwargs):
        filter_type = {}
        stores_id = {}
        order_by = 'id'
        page_number = 1
        per_page = 10
        user_id = kwargs.pop("user_id")


        if 'order_by' in kwargs:
            order_by = kwargs.pop('order_by')[0]

        if 'page' in kwargs:
            page_number = kwargs.pop('page')[0]
            
        if 'perPage' in kwargs:
            per_page = kwargs.pop('perPage')[0]

        if 'from' in kwargs or 'until' in kwargs:
            filter_type = make_filter(kwargs)

        if 'stores_id' in kwargs:
            stores_id['stores_id'] = kwargs.pop('stores_id')[0]


        found_vouchers = list(Vouchers.objects.filter(accounts=user_id).filter(**stores_id).filter(**kwargs, **filter_type).values().order_by(order_by))
        kwargs.clear()
        
        logger.info(f"Found '{len(found_vouchers)}' voucher(s) at VoucherRepository/get_by_filters.")

        return make_pagination(found_vouchers, per_page, page_number)

    @staticmethod
    def delete_by_voucher_id(**kwargs):
        voucher_id = kwargs.pop('id')[0]
        
        try:
            found_voucher = Vouchers.objects.get(id=voucher_id)
            found_voucher.delete()
            logger.info(f"Voucher '{voucher_id}' deleted for the user '{found_voucher.accounts}' at VoucherRepository/delete_by_voucher_id..")
            
            return f"Voucher '{voucher_id}' deleted successfully."

        except Exception as error:
            logger.info(f"Voucher id '{voucher_id}' not found at VoucherRepository/delete_by_voucher_id.")
            return False

    @staticmethod
    def delete_all_vouchers(user_id):
        found_vouchers = Vouchers.objects.filter(accounts=user_id).delete()
        logger.info(f"Deleted '{found_vouchers[0]}' voucher(s) for the user '{user_id}' at VoucherRepository/delete_all_vouchers.")

        return found_vouchers
