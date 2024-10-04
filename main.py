import argparse
import logging

from db_manager import DbManager
from json_parser import read_rooms_file, read_students_file
from runtime_handler import (
    handle_db_operation,
    handle_file_reading,
    handle_output_operation,
)


logger = logging.getLogger("main_logger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/main.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)


def main():
    parser = argparse.ArgumentParser(
        description="Parse data from rooms and students files, insert parsed data to "
        "database and return resuls of specified SQL-queries (task 1 - task "
        "4) for this data in output files."
    )
    parser.add_argument("--rooms", required=True, help="Path to the rooms file (*.json)")
    parser.add_argument(
        "--students", required=True, help="Path to the students file (*.json)"
    )
    parser.add_argument(
        "--format",
        required=True,
        choices=["xml", "json"],
        help="Output format: xml or json",
    )
    parser.add_argument(
        "--dbc",
        required=True,
        choices=["y", "n"],
        help="Does the database need to be cleaned after " "the script execution: y/n",
    )

    args = parser.parse_args()

    logger.info("Reading input files...")
    rooms = handle_file_reading(
        read_rooms_file, args.rooms, "Failed to read rooms file", logger
    )
    students = handle_file_reading(
        read_students_file, args.students, "Failed to read students file", logger
    )

    if rooms is None:
        logger.error("Rooms file is empty.")
        print("Rooms file is empty.")
        return
    elif rooms == -1:
        return
    elif students is None:
        logger.error("Students file is empty.")
        print("Students file is empty.")
        return
    elif students == -1:
        return

    logger.info("Successfully read input files.")

    db = DbManager()

    logger.info("Сlearing the Rooms and Students tables in database")
    if not handle_db_operation(db.clear_tables, "Failed to clear the database", logger):
        return

    logger.info("Inserting rooms data...")
    if not handle_db_operation(db.insert_rooms, "Failed to insert rooms", logger, rooms):
        return

    logger.info("Inserting students data...")
    if not handle_db_operation(
        db.insert_students, "Failed to insert students", logger, students
    ):
        return

    logger.info("Creating indexes...")
    if not handle_db_operation(db.create_indexes, "Failed to create indexes", logger):
        return

    try:
        logger.info("Performing tasks ...")
        task_results = [db.task1(), db.task2(), db.task3(), db.task4()]
    except Exception:
        logger.error("Failed to perform tasks.")
        print("Failed to perform tasks. Look logs/db_manager.log for details.")
        return

    if not handle_output_operation(args.format, task_results, logger):
        return

    logger.info("Сlearing the Rooms and Students tables in database")
    if not handle_db_operation(db.clear_tables, "Failed to clear the database", logger):
        return


if __name__ == "__main__":
    main()
