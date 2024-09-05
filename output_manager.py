"""
output_manager Module

This module provides functions to convert data into JSON and XML formats and save them to files.
It includes functions for converting lists of tuples into JSON and XML files and returning the absolute file paths.
Logging is configured to track the conversion process and handle errors, including cases where the input data is empty.

Functions:
- output_json(data: List[Tuple[Any, ...]], task_number: str) -> Optional[str]:
    Converts data to JSON format, writes it to a file, and returns the absolute file path.
    If the data is empty, a warning is logged, and no file is created.

- output_xml(data: List[Tuple[Any, ...]], task_number: str) -> Optional[str]:
    Converts data to XML format, writes it to a file, and returns the absolute file path.
    If the data is empty, a warning is logged, and no file is created.
"""

import json
import logging
import os
import xml.etree.ElementTree as ET
from typing import Any, List, Optional, Tuple
from xml.dom import minidom


logger = logging.getLogger("output_manager_logger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/output_manager.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)

logger.propagate = False


def output_json(data: List[Tuple[Any, ...]], task_number: str) -> Optional[str]:
    """
    Converts the tasks data into a JSON-formatted string, writes it to a file,
    and returns the absolute file path.

    Args:
        data (List[Tuple[Any, ...]]): The data to be converted to JSON format.
        task_number (str): The task number that provides the data.

    Returns:
        Optional[str]: The absolute path to the written JSON file, or None if the data is empty.
    """
    logger.info("Converting the %s data to JSON...", task_number)
    if not data:
        logger.warning(
            "The %s data is empty. JSON file will not be created.", task_number
        )
        return None
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


def output_xml(data: List[Tuple[Any, ...]], task_number: str) -> Optional[str]:
    """
    Converts the tasks data into XML-formatted string, writes it to a file,
    and returns the absolute file path.

    Args:
        data (List[Tuple[Any, ...]]): The data to be converted to XML format.
        task_number (str): The task number that provides the data.

    Returns:
        Optional[str]: The absolute path to the written XML file, or None if the data is empty.
    """
    logger.info("Converting the %s data to XML...", task_number)
    if not data:
        logger.warning("The %s data is empty. XML file will not be created.", task_number)
        return None

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
        xml_str = ET.tostring(root, encoding="utf-8")
        parsed_xml = minidom.parseString(xml_str)
        pretty_xml_str = parsed_xml.toprettyxml(indent="    ")
        file_path = f"{task_number}_output.xml"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(pretty_xml_str)
        logger.info("Successfully converted the %s data to XML.", task_number)
        return os.path.abspath(file_path)
    except (OSError, IOError) as e:
        logging.error("Error writing the %s data XML to file: %s", task_number, e)
        raise
    except Exception as e:
        logging.error("Error writing the %s data XML to file: %s", task_number, e)
        raise
