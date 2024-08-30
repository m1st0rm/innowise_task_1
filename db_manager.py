"""
db_manager Module

This module provides the DBManager class for interacting with an SQLite database.
It includes methods to insert data into the 'Rooms' and 'Students' tables.
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
    for inserting data into the 'Rooms' and 'Students' tables.

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
