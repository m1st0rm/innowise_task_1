import json
import unittest
from unittest.mock import mock_open, patch

from json_parser import read_rooms_file, read_students_file


class JsonParserTest(unittest.TestCase):

    def setUp(self):
        self.rooms_data = json.dumps(
            [{"id": 0, "name": "Room #0"}, {"id": 1, "name": "Room #1"}]
        )

        self.students_data = json.dumps(
            [
                {
                    "id": 0,
                    "name": "Peggy Ryan",
                    "birthday": "2011-08-22T00:00:00.000000",
                    "room": 473,
                    "sex": "M",
                },
                {
                    "id": 1,
                    "name": "John Doe",
                    "birthday": "2010-05-15T00:00:00.000000",
                    "room": 474,
                    "sex": "F",
                },
            ]
        )

        self.empty_data = json.dumps([])

    @patch("builtins.open", new_callable=mock_open)
    def test_read_rooms_file(self, mock_file):
        mock_file.return_value.read.return_value = self.rooms_data
        expected = [(0, "Room #0"), (1, "Room #1")]
        result = read_rooms_file("fake_path")
        self.assertEqual(result, expected)

    @patch("builtins.open", new_callable=mock_open)
    def test_read_students_file(self, mock_file):
        mock_file.return_value.read.return_value = self.students_data
        expected = [
            (0, "Peggy Ryan", "2011-08-22T00:00:00.000000", "M", 473),
            (1, "John Doe", "2010-05-15T00:00:00.000000", "F", 474),
        ]
        result = read_students_file("fake_path")
        self.assertEqual(result, expected)

    @patch("builtins.open", new_callable=mock_open)
    def test_read_rooms_file_exception(self, mock_file):
        mock_file.side_effect = IOError("File not found")
        with self.assertRaises(IOError):
            read_rooms_file("fake_path")

    @patch("builtins.open", new_callable=mock_open)
    def test_read_students_file_exception(self, mock_file):
        mock_file.side_effect = IOError("File not found")
        with self.assertRaises(IOError):
            read_students_file("fake_path")

    @patch("builtins.open", new_callable=mock_open)
    def test_read_rooms_file_empty(self, mock_file):
        mock_file.return_value.read.return_value = self.empty_data
        result = read_rooms_file("fake_path")
        self.assertIsNone(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_read_students_file_empty(self, mock_file):
        mock_file.return_value.read.return_value = self.empty_data
        result = read_students_file("fake_path")
        self.assertIsNone(result)

    @patch("builtins.open", new_callable=mock_open, read_data="Not a JSON")
    def test_read_rooms_file_invalid_json(self, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            read_rooms_file("fake_path")

    @patch("builtins.open", new_callable=mock_open, read_data="Not a JSON")
    def test_read_students_file_invalid_json(self, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            read_students_file("fake_path")


if __name__ == "__main__":
    unittest.main()
