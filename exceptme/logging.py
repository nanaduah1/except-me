import requests
import logging
from logging import Handler, LogRecord, Logger


class SlackAlertHandler(Handler):
    def __init__(self, channel_url: str, level=logging.INFO, exclude: list = None):
        """
        :param channel_url: Slack channel webhook URL
        :param level: Log level to send to slack
        :param exclude: List of attributes to exclude from the log message (e.g. user, password)
            Default is ["msg", "args", "exc_info", "exc_text", "stack_info", "taskname", "msecs", "created", "relativeCreated", "thread"]
        """
        Handler.__init__(self, level)
        self.channel_url = channel_url
        self._exclude = exclude or [
            "msg",
            "args",
            "exc_info",
            "exc_text",
            "stack_info",
            "taskname",
            "msecs",
            "created",
            "relativeCreated",
            "thread",
        ]

    def emit(self, record: LogRecord):
        try:
            msg = self.format(record)

            # Create a slack message
            slack_message = {
                "text": f"```{msg}```",
                "attachments": [
                    {
                        "color": "#FF0000",
                        "fields": [
                            {
                                "title": "File",
                                "value": record.filename,
                                "short": True,
                            },
                            {
                                "title": "Module",
                                "value": record.module,
                                "short": True,
                            },
                            {
                                "title": "Function",
                                "value": record.funcName,
                                "short": True,
                            },
                            {
                                "title": "Line",
                                "value": record.lineno,
                                "short": True,
                            },
                        ],
                    }
                ],
            }

            if self._exclude:
                slack_message["attachments"][0]["fields"].extend(
                    [
                        {
                            "title": k,  # k.capitalize(),
                            "value": str(getattr(record, k)),
                            "short": True,
                        }
                        for k in record.__dict__.keys()
                        if k not in self._exclude
                    ]
                )
            requests.post(self.channel_url, json=slack_message)

        except Exception as ex:
            print(ex)


def addSlackAlert(logger: Logger, channel_url: str, level=logging.ERROR):
    handler = SlackAlertHandler(channel_url, level)
    logger.addHandler(handler)
