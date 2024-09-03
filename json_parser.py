"""
json_parser Module

This module provides functions to read and parse JSON files containing data about rooms and students.
It includes functions for reading room and student data from JSON files and returning them as lists of tuples.
Logging is configured to track the parsing process and handle errors.

Functions:
- read_rooms_file(file_path: str) -> Optional[List[Tuple[int, str]]]:
    Parses a JSON file containing room data and returns a list of tuples with room IDs and names.

- read_students_file(file_path: str) -> Optional[List[Tuple[int, str, str, str, int]]]:
    Parses a JSON file containing student data and returns a list of tuples with student details.
"""

import json
import logging
from typing import List, Optional, Tuple


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/json_parser.log"),
    ],
)
logger = logging.getLogger(__name__)


def read_rooms_file(file_path: str) -> Optional[List[Tuple[int, str]]]:
    """
    Parses a JSON file and returns a list of tuples.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Optional[List[Tuple[int, str]]]: A list of tuples where each tuple contains
                                         an ID and a name from the JSON file,
                                         or None if the file is empty.
    """
    logger.info("Reading rooms data from file: %s", file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not data:  # If the JSON file is empty
            logger.warning("Rooms file is empty.")
            return None
        rooms = [(item["id"], item["name"]) for item in data]
        logger.info("Successfully parsed %d rooms from file.", len(rooms))
        return rooms
    except Exception as e:
        logger.error("Error reading rooms file: %s (%s)", e, type(e).__name__)
        raise


def read_students_file(file_path: str) -> Optional[List[Tuple[int, str, str, str, int]]]:
    """
    Parses a JSON file and returns a list of tuples.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Optional[List[Tuple[int, str, str, str, int]]]: A list of tuples where each tuple contains
                                                        an ID, name, birthday, sex, and room number
                                                        from the JSON file, or None if the file is empty.
    """
    logger.info("Reading students data from file: %s", file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not data:  # If the JSON file is empty
            logger.warning("Students file is empty.")
            return None
        students = [
            (
                item["id"],
                item["name"],
                item["birthday"],
                item["sex"],
                item["room"],
            )
            for item in data
        ]
        logger.info("Successfully parsed %d students from file.", len(students))
        return students
    except Exception as e:
        logger.error("Error reading students file: %s (%s)", e, type(e).__name__)
        raise
