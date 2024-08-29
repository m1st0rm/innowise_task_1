"""
This module contains functions for parsing JSON files related to room & students data.

It includes the following functionality:
- Reading a JSON file and extracting a list of tuples with room IDs and names.
- Reading a JSON file and extracting a list of tuples with student IDs, names,
  birthday, sex, and room number.
"""

import json
import logging
from typing import List, Tuple


# Configure logging to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/json_parser.log"),
    ],
)
logger = logging.getLogger(__name__)


def read_rooms_file(file_path: str) -> List[Tuple[int, str]]:
    """
    Parses a JSON file and returns a list of tuples.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        List[Tuple[int, str]]: A list of tuples where each tuple contains
                                an ID and a name from the JSON file.
    """
    logger.info("Reading rooms data from file: %s", file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        rooms = [(item["id"], item["name"]) for item in data]
        logger.info("Successfully parsed %d rooms from file.", len(rooms))
        return rooms
    except Exception as e:
        logger.error("Error reading rooms file: %s", e)
        raise


def read_students_file(file_path: str) -> List[Tuple[int, str, str, str, int]]:
    """
    Parses a JSON file and returns a list of tuples.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        List[Tuple[int, str, str, str, int]]: A list of tuples where each tuple contains
                                               an ID, name, birthday, sex, and room number
                                               from the JSON file.
    """
    logger.info("Reading students data from file: %s", file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
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
        logger.error("Error reading students file: %s", e)
        raise
