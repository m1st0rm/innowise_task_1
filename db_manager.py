"""
db_manager Module

This module provides the DBManager class for interacting with an SQLite database.
It includes methods to insert data into the 'Rooms' and 'Students' tables, and methods for specific queries.
"""

import logging
import sqlite3
from sqlite3 import Error
from typing import List, Tuple


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/db_manager.log"),
    ],
)
logger = logging.getLogger(__name__)


class DbManager:
    """
    DbManager Class

    This class manages the connection to an SQLite database and provides methods
    for inserting data into the 'Rooms' and 'Students' tables, as well as for executing
    specific queries to retrieve data.

    Attributes:
        connection (sqlite3.Connection): The SQLite database connection object.
    """

    def __init__(self) -> None:
        """
        Initializes the connection to the SQLite database.
        Establishes a connection to 'database.db'. Raises an exception if the connection fails.
        """
        self.connection = None
        try:
            self.connection = sqlite3.connect("database.db")
            logger.info("Database connection established.")
        except Error as e:
            logger.error("Error connecting to the database: %s (%s)", e, type(e).__name__)
            raise

    def __del__(self) -> None:
        """
        Closes the connection to the database upon object deletion.
        Logs an error if the connection cannot be closed properly.
        """
        if self.connection:
            try:
                self.connection.close()
                logger.info("Database connection closed.")
            except Error as e:
                logger.error(
                    "Error closing the database connection: %s (%s)", e, type(e).__name__
                )
                raise

    def insert_rooms(self, rooms: List[Tuple[int, str]]) -> None:
        """
        Inserts room data into the 'Rooms' table.

        Args:
            rooms (List[Tuple[int, str]]): A list of tuples, each containing an ID and a name of a room.

        Raises:
            Error: If an error occurs while executing the SQL query.
        """
        cursor = self.connection.cursor()
        try:
            self.connection.execute("BEGIN TRANSACTION")
            cursor.executemany("INSERT INTO Rooms (id, name) VALUES (?, ?)", rooms)
            self.connection.commit()
            logger.info("Successfully added %d room(s).", len(rooms))
        except Error as e:
            self.connection.rollback()
            logger.error("Error inserting room data: %s (%s)", e, type(e).__name__)
            raise

    def insert_students(self, students: List[Tuple[int, str, str, str, int]]) -> None:
        """
        Inserts student data into the 'Students' table.

        Args:
            students (List[Tuple[int, str, str, str, int]]): A list of tuples, each containing
            an ID, name, birthday, sex, and room number of a student.

        Raises:
            Error: If an error occurs while executing the SQL query.
        """
        cursor = self.connection.cursor()
        try:
            self.connection.execute("BEGIN TRANSACTION")
            cursor.executemany(
                "INSERT INTO Students (id, name, birthday, sex, room) VALUES (?, ?, ?, ?, ?)",
                students,
            )
            self.connection.commit()
            logger.info("Successfully added %d student(s).", len(students))
        except Error as e:
            self.connection.rollback()
            logger.error("Error inserting student data: %s (%s)", e, type(e).__name__)
            raise

    def task1(self) -> List[Tuple[str, int]]:
        """
        Retrieves a list of rooms and the count of students in each room.

        Returns:
            List[Tuple[str, int]]: A list of tuples where each tuple contains the name of the room
            and the number of students in that room.

        Raises:
            Error: If an error occurs while executing the SQL query.
        """
        cursor = self.connection.cursor()
        try:
            self.connection.execute("BEGIN TRANSACTION")
            cursor.execute(
                """
                SELECT Rooms.name, COUNT(Students.id) AS students_count
                FROM Rooms
                LEFT JOIN Students ON Rooms.id = Students.room
                GROUP BY Rooms.name
                ORDER BY students_count DESC
            """
            )
            result = cursor.fetchall()
            self.connection.commit()
            logger.info("Task1 completed successfully: Fetched %d records.", len(result))
            return result
        except Error as e:
            self.connection.rollback()
            logger.error("Error executing task 1: %s (%s)", e, type(e).__name__)
            raise

    def task2(self) -> List[Tuple[str, float]]:
        """
        Retrieves the 5 rooms with the smallest average age of students.
        The age is calculated as the difference between the current date and
        the student's birthday, converted into years. Results are ordered by ascending
        average age. Rooms with a NULL average age are excluded.

        Returns:
            List[Tuple[str, float]]: A list of tuples where each tuple contains the room name
            and the average age of students in that room, rounded to three decimal places.

        Raises:
            Error: If an error occurs while executing the SQL query.
        """
        cursor = self.connection.cursor()
        try:
            self.connection.execute("BEGIN TRANSACTION")
            cursor.execute(
                """
                SELECT Rooms.name,
                ROUND(AVG(JULIANDAY('now') - JULIANDAY(Students.birthday)) / 365.25, 3) AS avg_students_age
                FROM Rooms
                LEFT JOIN Students ON Rooms.id = Students.room
                GROUP BY Rooms.name
                HAVING avg_students_age IS NOT NULL
                ORDER BY avg_students_age
                LIMIT 5
                """
            )
            result = cursor.fetchall()
            self.connection.commit()
            logger.info("Task2 completed successfully: Fetched %d records.", len(result))
            return result
        except Error as e:
            self.connection.rollback()
            logger.error("Error executing task2: %s (%s)", e, type(e).__name__)
            raise

    def task3(self) -> List[Tuple[str, float]]:
        """
        Retrieves the 5 rooms with the largest difference in student ages.
        The age difference is calculated as the difference between the maximum and minimum
        student ages in each room. The ages are determined based on the difference between
        the current date and the students' birthdays, converted into years.

        Returns:
            List[Tuple[str, float]]: A list of tuples where each tuple contains the room name
            and the age difference of students in that room, rounded to three decimal places.

        Raises:
            Error: If an error occurs while executing the SQL query.
        """
        cursor = self.connection.cursor()
        try:
            self.connection.execute("BEGIN TRANSACTION")
            cursor.execute(
                """
                SELECT Rooms.name,
                ROUND((MAX(JULIANDAY('now') - JULIANDAY(Students.birthday)) / 365.25 -
                MIN(JULIANDAY('now') - JULIANDAY(Students.birthday)) / 365.25), 3) AS age_difference
                FROM Rooms
                JOIN Students ON Rooms.id = Students.room
                GROUP BY Rooms.name
                ORDER BY age_difference DESC
                LIMIT 5
                """
            )
            result = cursor.fetchall()
            self.connection.commit()
            logger.info("Task3 completed successfully: Fetched %d records.", len(result))
            return result
        except Error as e:
            self.connection.rollback()
            logger.error("Error executing task3: %s (%s)", e, type(e).__name__)
            raise

    def task4(self) -> List[str]:
        """
        Retrieves the names of rooms where students of different sexes reside.
        This method identifies rooms where there are students of at least two distinct sexes.
        It does this by joining the 'Rooms' and 'Students' tables, grouping the results by room name,
        and filtering for rooms with more than one distinct sex among students.

        Returns:
            List[str]: A list of room names where students of different sexes reside.

        Raises:
            Error: If an error occurs while executing the SQL query.
        """
        cursor = self.connection.cursor()
        try:
            self.connection.execute("BEGIN TRANSACTION")
            cursor.execute(
                """
                SELECT Rooms.name
                FROM Rooms
                LEFT JOIN Students ON Rooms.id = Students.room
                GROUP BY Rooms.name
                HAVING COUNT(DISTINCT Students.sex) > 1
                """
            )
            result = [row[0] for row in cursor.fetchall()]
            self.connection.commit()
            logger.info("Task4 completed successfully: Fetched %d records.", len(result))
            return result
        except Error as e:
            self.connection.rollback()
            logger.error("Error executing task4: %s (%s)", e, type(e).__name__)
            raise
