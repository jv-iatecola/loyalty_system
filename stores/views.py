from .controller.stores_create_controller import create as create
from .controller.stores_get_controller import stores_get as stores_get

def sort_methods(request):

    match request.method:
        case "POST":
            return create(request)

        case "GET":
            return stores_get(request)
