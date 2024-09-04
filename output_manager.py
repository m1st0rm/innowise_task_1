import json
import logging
import os
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
