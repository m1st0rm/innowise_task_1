"""
output_manager Module

This module provides functions to convert data into JSON and XML formats and save them to files.
It includes functions for converting lists of tuples into JSON and XML files and returning the absolute file paths.
Logging is configured to track the conversion process and handle errors.

Functions:
- output_json(data: List[Tuple[Any, ...]], task_number: str) -> str:
    Converts data to JSON format, writes it to a file, and returns the absolute file path.

- output_xml(data: List[Tuple[Any, ...]], task_number: str) -> str:
    Converts data to XML format, writes it to a file, and returns the absolute file path.
"""

import json
import logging
import os
import xml.etree.ElementTree as ET
from typing import Any, List, Tuple


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/output_manager.log"),
    ],
)
logger = logging.getLogger(__name__)


def output_json(data: List[Tuple[Any, ...]], task_number: str) -> str:
    """
    Converts the tasks data into a JSON-formatted string, writes it to a file,
    and returns the absolute file path.

    Args:
        data (List[Tuple[Any, ...]]): The data to be converted to JSON format.
        task_number (str): The task number that provides the data.

    Returns:
        str: The absolute path to the written JSON file.
    """
    logger.info("Converting the %s data to JSON...", task_number)
    try:
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        file_path = f"{task_number}_output.json"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json_data)
        logger.info("Successfully converted the %s data to JSON.", task_number)
        return os.path.abspath(file_path)
    except (OSError, IOError) as e:
        logging.error("Error writing the %s data JSON to file: %s", task_number, e)
        raise
    except json.JSONDecodeError as e:
        logging.error("Error serializing the %s data to JSON: %s", task_number, e)
        raise


def output_xml(data: List[Tuple[Any, ...]], task_number: str) -> str:
    """
    Converts the tasks data into XML-formatted string, writes it to a file,
    and returns the absolute file path.

    Args:
        data (List[Tuple[Any, ...]]): The data to be converted to XML format.
        task_number (str): The task number that provides the data.

    Returns:
        str: The absolute path to the written XML file.
    """
    logger.info("Converting the %s data to XML...", task_number)

    def tuple_to_xml(tag, tpl):
        elem = ET.Element(tag)
        for i, value in enumerate(tpl):
            child = ET.SubElement(elem, f"item_{i}")
            child.text = str(value)
        return elem

    try:
        root = ET.Element("root")
        for item in data:
            root.append(tuple_to_xml("data", item))
        tree = ET.ElementTree(root)
        file_path = f"{task_number}_output.xml"
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        logger.info("Successfully converted the %s data to XML.", task_number)
        return os.path.abspath(file_path)
    except (OSError, IOError) as e:
        logging.error("Error writing the %s data XML to file: %s", task_number, e)
        raise
    except Exception as e:
        logging.error("Error writing the %s data XML to file: %s", task_number, e)
        raise
