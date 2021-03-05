from .utils import check_mobile_ua


class MobileDetectMiddleware:
    """
        Проверяет request на мобильный ua и добавляет флаг is_mobile в request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        setattr(request, 'is_mobile',  check_mobile_ua(request))
