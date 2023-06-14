"""
Error handler module.
"""
import logging
import typing

import rest_framework.response
import rest_framework.views

from . import errors

logger = logging.getLogger(__name__)


def error_handler(error: Exception, context: typing.Any):
    """
    Error handler.
    """
    response = rest_framework.views.exception_handler(error, context)

    logger.exception("error while handling request: %s", error)

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
