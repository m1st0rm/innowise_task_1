import argparse
import logging

from db_manager import DbManager
from json_parser import read_rooms_file, read_students_file
from output_manager import output_json, output_xml


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

    try:
        logger.info("Reading input files...")
        rooms = read_rooms_file(args.rooms)
        students = read_students_file(args.students)
    except Exception:
        logger.error("Failed to read input files.")
        print("Failed to read input files. Look logs/json_parser.log for details.")
        return

    if rooms is None:
        logger.error("Rooms file is empty.")
        print("Rooms file is empty.")
        return
    if students is None:
        logger.error("Students file is empty.")
        print("Students file is empty.")
        return

    logger.info("Successfully read input files.")

    db = DbManager()

    try:
        logger.info("Сlearing the Rooms and Students tables in database")
        db.clear_tables()
    except Exception:
        logger.error("Failed to clear the database.")
        print("Failed to clear the database. Look logs/db_manager.log for details.")
        return

    try:
        logger.info("Inserting rooms data...")
        db.insert_rooms(rooms)
        logger.info("Inserting students data...")
        db.insert_students(students)
    except Exception:
        logger.error("Failed to insert data in database.")
        print("Failed to insert data in database. Look logs/db_manager.log for details.")
        return

    try:
        logger.info("Creating indexes...")
        db.create_indexes()
    except Exception:
        logger.error("Failed to create indexes.")
        print("Failed to create indexes. Look logs/db_manager.log for details.")
        return

    try:
        logger.info("Performing tasks ...")
        task1_result = db.task1()
        task2_result = db.task2()
        task3_result = db.task3()
        task4_result = db.task4()
    except Exception:
        logger.error("Failed to perform tasks.")
        print("Failed to perform tasks. Look logs/db_manager.log for details.")
        return

    tasks_result = []

    if args.format == "xml":
        try:
            logger.info("Writing results to XML file...")
            tasks_result.append(output_xml(task1_result, "task1"))
            tasks_result.append(output_xml(task2_result, "task2"))
            tasks_result.append(output_xml(task3_result, "task3"))
            tasks_result.append(output_xml(task4_result, "task4"))
        except Exception:
            logger.error("Failed to write results to XML file.")
            print(
                "Failed to write results to XML file. Look logs/output_manager.log for details."
            )
            return
    else:
        try:
            logger.info("Writing results to JSON file...")
            tasks_result.append(output_json(task1_result, "task1"))
            tasks_result.append(output_json(task2_result, "task2"))
            tasks_result.append(output_json(task3_result, "task3"))
            tasks_result.append(output_json(task4_result, "task4"))
        except Exception:
            logger.error("Failed to write results to JSON file.")
            print(
                "Failed to write results to JSON file. Look logs/output_manager.log for details."
            )
            return

    for i, task_result in enumerate(tasks_result):
        if task_result is None:
            print(
                f"Task {i + 1} data is empty. Output file for this task will not be created."
            )
        else:
            print(f"Task {i + 1} output file path: {task_result}.")

    if args.dbc == "y":
        try:
            logger.info("Сlearing the Rooms and Students tables in database")
            db.clear_tables()
        except Exception:
            logger.error("Failed to clear the database.")
            print("Failed to clear the database. Look logs/db_manager.log for details.")
            return


if __name__ == "__main__":
    main()
