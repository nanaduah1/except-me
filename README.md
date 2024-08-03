# ExceptMe

A simple logging handler to post exceptions to slack.
It also has an optional django middleware to catch exceptions and post them to slack.

## Installation

```bash
poetry add git+https://github.com/nanaduah1/except-me.git
```

## Usage

```python
import logging
from exceptme import SlackAlertHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(SlackAlertHandler('SLACK_WEBHOOK_URL'))

# Log an exception as usual and it will be posted to slack
try:
    raise Exception('This is an exception')
except Exception as e:
    logger.exception(e)
```

## Django Middleware

    ```python
    MIDDLEWARE = [
        ...
        'exceptme.middleware.ExceptMeMiddleware',
    ]
    ```
