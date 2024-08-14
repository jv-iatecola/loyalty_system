from vouchers.repository.vouchers_repository import VoucherRepository
from django.http import JsonResponse


def delete(request):
    found_user = request.found_user
    query_parameters = request.GET.copy()

    if 'id' in query_parameters and 'store_id' in query_parameters:
        delete_by_voucher_id_response = VoucherRepository.delete_by_voucher_id(**query_parameters)
        if not delete_by_voucher_id_response:
            return JsonResponse(
                {"message": f"Failed to find vouchers for the id '{query_parameters['id']}'."}, status=400)

        return JsonResponse({"message": delete_by_voucher_id_response}, status=200)

    if 'id' in query_parameters:
        delete_by_voucher_id_response = VoucherRepository.delete_by_voucher_id(**query_parameters)
        if not delete_by_voucher_id_response:
            return JsonResponse(
                {"message": f"Failed to find vouchers for the id '{query_parameters['id']}'."}, status=400)

        return JsonResponse({"message": delete_by_voucher_id_response}, status=200)

    if 'store_id' in query_parameters:
        delete_all_vouchers_by_store_id = VoucherRepository.delete_all_vouchers_by_store_id(**query_parameters)
        if not delete_all_vouchers_by_store_id:
            return JsonResponse(
                {"message": f"Failed to find vouchers for the store '{query_parameters['store_id']}'."}, status=400)

        return JsonResponse({"message": delete_all_vouchers_by_store_id}, status=200)

    delete_all_vouchers_response = VoucherRepository.delete_all_vouchers(found_user.id) 
    return JsonResponse(
        {"message": f"Deleted '{delete_all_vouchers_response[0]}' voucher(s) for user '{found_user.id}' at vouchers_delete_controller."},
        status=200
    )
