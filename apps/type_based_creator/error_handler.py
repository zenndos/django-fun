import logging

import rest_framework.views
import rest_framework.response

from . import errors

logger = logging.getLogger(__name__)


def error_handler(error, context):
    response = rest_framework.views.exception_handler(error, context)

    logger.exception(f"error while handling request: {error}")

    if response is not None:
        ...

    elif isinstance(error, errors.Error):
        response = rest_framework.response.Response(
            {
                "error": error.message,
            },
            status=error.status_code,
        )
    else:
        response = rest_framework.response.Response(
            {
                "error": "Internal server error.",
            },
            status=500,
        )

    return response
