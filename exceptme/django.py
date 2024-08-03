from logging import getLogger, ERROR
from django.conf import settings
from exceptme.logging import SlackAlertHandler

logger = getattr(settings, "LOGGER", None)
if logger is None and getattr(settings, "ERROR_SLACK_CHANNEL_URL", None):
    logger = getLogger(__name__)
    logger.handlers.clear()
    logger.setLevel(level=ERROR)
    slack = SlackAlertHandler(channel_url=settings.ERROR_SLACK_CHANNEL_URL, level=ERROR)
    logger.addHandler(slack)


class AnnounceExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if logger:
            logger.exception(
                exception,
                extra={
                    "user": request.user,
                    "path": request.path,
                    "method": request.method,
                    "IP": request.META.get("REMOTE_ADDR", ""),
                    "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                    "referer": request.META.get("HTTP_REFERER", ""),
                    "origin": request.META.get("HTTP_ORIGIN"),
                },
            )
        else:
            print(exception)
        return None
