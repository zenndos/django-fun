"""
Errors raised by application.
"""

import abc


class Error(Exception, abc.ABC):
    """
    Error.

    Base class for exceptions raised by the applicatin.
    """

    @property
    @abc.abstractmethod
    def status_code(self):
        """
        HTTP error code corresponding to the exception.
        """

    @property
    @abc.abstractmethod
    def message(self):
        """
        Message corresponding to the exception.
        """


class BadRequest(Error):
    """
    BadRequest Error.

    Error indicating the error in implementation of the service.
    """

    @property
    def status_code(self):
        """
        HTTP error code corresponding to the exception.
        """
        return 400

    @property
    def message(self):
        """
        Message corresponding to the exception.
        """
        return "bad request"
