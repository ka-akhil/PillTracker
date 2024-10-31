import sys
from src.logger import logging


def error_message_detail(error: Exception, error_details: sys) -> str:
    """
    Returns a formatted error message with file name, line number, and error details.

    Args:
        error (Exception): The error that occurred.
        error_details (sys): The error details.

    Returns:
        str: The formatted error message.
    """

    _, _, tb = error_details.exc_info()
    file_name = tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in file [{0}] line number [{1}] Error message [{2}]".format(
        file_name, tb.tb_lineno, str(error)
    )
    return error_message


class CustomException(Exception):
    """
    Custom exception class for handling specific errors in the application.

    Attributes:
        error_message (str): The error message associated with the exception.

    Methods:
        __init__(self, error_message: str, error_details: sys): Initializes the CustomException object.
        __str__(self): Returns the error message as a string representation of the exception.
    """

    def __init__(self, error_message: str, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_details)

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as e:
        logging.info("Logging started")
        raise CustomException(e, sys)
