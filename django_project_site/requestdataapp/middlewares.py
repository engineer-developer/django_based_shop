from datetime import datetime, timedelta

from django.http import HttpRequest, HttpResponse


def set_useragent_on_request_middleware(get_response):

    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.response_count = 0
        self.exception_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("request count", self.requests_count)
        response = self.get_response(request)
        self.response_count += 1
        print("response count", self.response_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print("got", self.exception_count, "exceptions so far")


class ThrottlingMiddleware:
    """
    Middleware, ограничивает обработку запросов пользователя,
    которые поступают чаще чем 1 раз в 2 секунды.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.throttling_time = 2
        self.requests_data = {}

    def __call__(self, request: HttpRequest):
        request_host = request.META["HTTP_HOST"]
        print("request data:", self.requests_data)

        if request_host not in self.requests_data:
            self.requests_data[request_host] = datetime.now()
            response = self.get_response(request)
        else:
            last_access_time = self.requests_data[request_host]
            difference = datetime.now() - last_access_time
            if difference.seconds < self.throttling_time and not request.path.endswith(
                "favicon.ico"
            ):
                print(f"Time difference: {difference} seconds")
                self.requests_data[request_host] = datetime.now()
                return HttpResponse("Too many requests", status=429)

            response = self.get_response(request)
            self.requests_data[request_host] = datetime.now()

        return response
