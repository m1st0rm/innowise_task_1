import unittest
from sqlite3 import Error

from db_manager import DbManager


class TestDbManager(unittest.TestCase):
    db_path = "test_database.db"
    db_manager = None

    @classmethod
    def setUpClass(cls):
        cls.db_manager = DbManager(db_path=cls.db_path)

    def setUp(self):
        self.insert_test_data()

    def tearDown(self):
        self.db_manager.clear_tables()

    @classmethod
    def tearDownClass(cls):
        cls.db_manager = None

    def insert_test_data(self):
        self.db_manager.execute_query("INSERT INTO Rooms (id, name) VALUES (1, 'Room A')")
        self.db_manager.execute_query("INSERT INTO Rooms (id, name) VALUES (2, 'Room B')")
        self.db_manager.execute_query("INSERT INTO Rooms (id, name) VALUES (3, 'Room C')")
        self.db_manager.execute_query(
            "INSERT INTO Students (id, name, birthday, sex, room) VALUES (1, 'Alice', '2000-01-01T00:00:00.000000', 'F', 1)"
        )
        self.db_manager.execute_query(
            "INSERT INTO Students (id, name, birthday, sex, room) VALUES (2, 'Bob', '2001-02-02T00:00:00.000000', 'M', 1)"
        )
        self.db_manager.execute_query(
            "INSERT INTO Students (id, name, birthday, sex, room) VALUES (3, 'Charlie', '1999-03-03T00:00:00.000000', 'M', 2)"
        )
        self.db_manager.execute_query(
            "INSERT INTO Students (id, name, birthday, sex, room) VALUES (4, 'Diana', '2002-04-04T00:00:00.000000', 'F', 2)"
        )
        self.db_manager.execute_query(
            "INSERT INTO Students (id, name, birthday, sex, room) VALUES (5, 'Eve', '2001-05-05T00:00:00.000000', 'F', 3)"
        )

    def test_task1(self):
        result = self.db_manager.task1()
        expected = [("Room A", 2), ("Room B", 2), ("Room C", 1)]
        result.sort(key=lambda x: x[0])
        self.assertEqual(result, expected)

    def test_task2(self):
        result = self.db_manager.task2()
        expected = [("Room C", 23.333), ("Room B", 23.963), ("Room A", 24.130)]
        self.assertEqual(result, expected)

    def test_task3(self):
        result = self.db_manager.task3()
        expected = [("Room B", 3.088), ("Room A", 1.090), ("Room C", 0.000)]
        self.assertEqual(result, expected)

    def test_task4(self):
        result = self.db_manager.task4()
        expected = ["Room A", "Room B"]
        self.assertEqual(result, expected)

    def test_insert_rooms(self):
        self.db_manager.clear_tables()
        rooms = [(4, "Room D"), (5, "Room E")]
        self.db_manager.insert_rooms(rooms)
        result = self.db_manager.fetch_all("SELECT * FROM Rooms")
        expected = [(4, "Room D"), (5, "Room E")]
        self.assertEqual(result, expected)

    def test_insert_students(self):
        self.db_manager.clear_tables()
        rooms = [(1, "Room F")]
        self.db_manager.insert_rooms(rooms)
        students = [
            (6, "Frank", "1998-06-06T00:00:00.000000", "M", 1),
            (7, "Grace", "2000-07-07T00:00:00.000000", "F", 1),
        ]
        self.db_manager.insert_students(students)
        result = self.db_manager.fetch_all("SELECT * FROM Students")
        expected = [
            (6, "Frank", "1998-06-06T00:00:00.000000", "M", 1),
            (7, "Grace", "2000-07-07T00:00:00.000000", "F", 1),
        ]
        self.assertEqual(result, expected)

    def test_insert_rooms_with_duplicate_id(self):
        self.db_manager.clear_tables()
        self.db_manager.insert_rooms([(1, "Room D")])
        with self.assertRaises(Error):
            self.db_manager.insert_rooms([(1, "Room E")])

    def test_insert_students_with_duplicate_id(self):
        self.db_manager.clear_tables()
        rooms = [(1, "Room F")]
        self.db_manager.insert_rooms(rooms)
        students = [
            (6, "Frank", "1998-06-06T00:00:00.000000", "M", 1),
            (6, "Grace", "2000-07-07T00:00:00.000000", "F", 1),
        ]
        with self.assertRaises(Error):
            self.db_manager.insert_students(students)

    def test_execute_invalid_query(self):
        with self.assertRaises(Error):
            self.db_manager.execute_query("INVALID SQL QUERY")

    def test_fetch_all_invalid_query(self):
        with self.assertRaises(Error):
            self.db_manager.fetch_all("INVALID SQL QUERY")


if __name__ == "__main__":
    unittest.main()
