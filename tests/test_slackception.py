from logging import getLogger, INFO, ERROR
from exceptme.logging import SlackAlertHandler


def test_exception_sent():
    # Given
    channel_url = "https://hooks.slack.com/services/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"
    handler = SlackAlertHandler(channel_url, ERROR)
    logger = getLogger("test")
    logger.addHandler(handler)
    logger.setLevel(INFO)
    try:
        # When
        raise ValueError("This is a test")
    except ValueError as e:
        # Then
        logger.exception(e, extra={"user": "test_user"})
