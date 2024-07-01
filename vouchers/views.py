from .controller.vouchers_get_controller import vouchers_get as vouchers_get
from .controller.vouchers_create_controller import create as create
from .controller.vouchers_delete_controller import delete as delete


def sort_methods(request):

    match request.method:
        case 'POST':
            return create(request)

        case 'GET':
            return vouchers_get(request)
        
        case 'DELETE':
            return delete(request)
            