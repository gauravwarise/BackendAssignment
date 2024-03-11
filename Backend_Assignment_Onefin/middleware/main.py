from django.core.cache import cache

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_count = cache.get("request_count")
        if request_count is None:
            request_count = 0
            cache.set("request_count", request_count)
        request_count = cache.incr("request_count", 1)
        request.request_count = request_count
        response = self.get_response(request)
        return response