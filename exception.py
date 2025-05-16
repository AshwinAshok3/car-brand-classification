# Purpose: Custom Exception Handling with detailed error tracking.

import sys  # To fetch runtime exception details like traceback
from logger import logger  #  Import logger.py
# Error message formatting function
def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()  # Extract traceback info
    file_name = exc_tb.tb_frame.f_code.co_filename  # Which file caused the error
    line_number = exc_tb.tb_lineno  # Line number of error

    # Formatted error message
    error_message = (
        f"Error occurred in Python script: [{file_name}], "
        f"Line Number: [{line_number}], "
        f"Error Details: [{str(error)}]"
    )
    #  Log the error
    logger.error(error_message)

    return error_message


# Custom Exception Class
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)  # Initialize base Exception class
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message  # When printed

    def __repr__(self):
        return self.error_message  # For object representation
