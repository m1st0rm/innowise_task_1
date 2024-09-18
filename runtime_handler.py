"""
runtime_handler Module

This module provides functions for handling various runtime operations including file reading, database operations, and output handling.
It includes functions to manage file reading with error handling, perform database operations with logging, and write output results to files in either JSON or XML format.
Logging is configured to track the operations and handle errors, including cases where operations fail or input data is empty.

Functions:
- handle_file_reading(func: Callable[[str], List[Tuple[int, str]] | List[Tuple[int, str, str, str, int]] | None], file_path: str, log_error_message: str, logger: Logger) -> int | List[Tuple[int, str]] | List[Tuple[int, str, str, str, int]] | None:
    Reads data from a file using a specified function and handles errors. Logs an error message and prints it if reading fails.
    Returns the result from the function or -1 if an error occurs.

- handle_db_operation(operation: Callable[..., None], error_message: str, logger: Logger, *args) -> bool:
    Executes a database operation and handles errors. Logs success or error messages and prints the error if the operation fails.
    Returns True if the operation is successful, or False if an error occurs.

- handle_output_operation(output_format: str, task_results: List, logger: Logger) -> bool:
    Writes the task results to a file in the specified format (JSON or XML). Handles errors during the writing process, logs them, and prints messages if any task data is empty or writing fails.
    Returns True if all output operations are successful, or False if an error occurs.
"""

from logging import Logger
from typing import Callable, List, Tuple, Union

from output_manager import output_json, output_xml


def handle_file_reading(
    func: Callable[
        [str], Union[List[Tuple[int, str]], List[Tuple[int, str, str, str, int]], None]
    ],
    file_path: str,
    log_error_message: str,
    logger: Logger,
) -> Union[int, List[Tuple[int, str]], List[Tuple[int, str, str, str, int]], None]:
    """
    Reads data from a file using a specified function and handles errors.

    Args:
        func (Callable[[str], Union[List[Tuple[int, str]], List[Tuple[int, str, str, str, int]], None]]): The function used to read data from the file.
        file_path (str): The path to the file to be read.
        log_error_message (str): The error message to log if reading the file fails.
        logger (Logger): The logger instance to use for logging errors.

    Returns:
        Union[int, List[Tuple[int, str]], List[Tuple[int, str, str, str, int]], None]: The data read from the file, -1 if an error occurs, or None if the file is empty.
    """
    try:
        return func(file_path)
    except Exception:
        logger.error(log_error_message)
        print(f"{log_error_message}. Look logs/json_parser.log for details.")
        return -1


def handle_db_operation(
    operation: Callable[..., None], error_message: str, logger: Logger, *args
) -> bool:
    """
    Executes a database operation and handles errors.

    Args:
        operation (Callable[..., None]): The database operation to perform.
        error_message (str): The error message to log if the operation fails.
        logger (Logger): The logger instance to use for logging errors.
        *args: Arguments to pass to the database operation.

    Returns:
        bool: True if the operation is successful, False if an error occurs.
    """
    try:
        operation(*args)
    except Exception:
        logger.error(error_message)
        print(f"{error_message}. Look logs/db_manager.log for details.")
        return False
    return True


def handle_output_operation(
    output_format: str, task_results: List, logger: Logger
) -> bool:
    """
    Writes the task results to a file in the specified format (JSON or XML).

    Args:
        output_format (str): The format for the output files, either "json" or "xml".
        task_results (List): The results of tasks to be written to files.
        logger (Logger): The logger instance to use for logging information and errors.

    Returns:
        bool: True if all output operations are successful, False if an error occurs.
    """
    output_func = output_xml if output_format == "xml" else output_json
    for index, result in enumerate(task_results):
        try:
            logger.info(
                f"Writing results for task {index + 1} to {output_format.upper()} file..."
            )
            task_result = output_func(result, f"task{index + 1}")
            if task_result is None:
                print(
                    f"Task {index + 1} data is empty. Output file for this task will not be created."
                )
            else:
                print(f"Task {index + 1} output file path: {task_result}.")
        except Exception:
            logger.error(f"Failed to write results to {output_format.upper()} file.")
            print(
                f"Failed to write results to {output_format.upper()} file. Look logs/output_manager.log for details."
            )
            return False
    return True
