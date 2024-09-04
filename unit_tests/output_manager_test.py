import json
import os
import unittest
from unittest.mock import mock_open, patch

from output_manager import output_json, output_xml


class OutputManagerTest(unittest.TestCase):

    def setUp(self):
        self.json_data = [(0, "Room #0"), (1, "Room #1")]
        self.xml_data = [(0, "Room #0"), (1, "Room #1")]
        self.task_number = "task1"
        self.json_content = json.dumps(self.json_data, indent=4, ensure_ascii=False)
        self.xml_content = (
            '<?xml version="1.0" ?>\n'
            "<root>\n"
            "    <data>\n"
            "        <item_0>0</item_0>\n"
            "        <item_1>Room #0</item_1>\n"
            "    </data>\n"
            "    <data>\n"
            "        <item_0>1</item_0>\n"
            "        <item_1>Room #1</item_1>\n"
            "    </data>\n"
            "</root>"
        )
        self.json_file_path = f"{self.task_number}_output.json"
        self.xml_file_path = f"{self.task_number}_output.xml"

    def tearDown(self):
        if os.path.exists(self.json_file_path):
            os.remove(self.json_file_path)
        if os.path.exists(self.xml_file_path):
            os.remove(self.xml_file_path)

    def test_output_json_content(self):
        result_path = output_json(self.json_data, self.task_number)
        with open(result_path, "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(content, self.json_content)

    def test_output_xml_content(self):
        result_path = output_xml(self.xml_data, self.task_number)
        with open(result_path, "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(content.strip(), self.xml_content.strip())

    @patch("builtins.open", new_callable=mock_open)
    def test_output_json_exception(self, mock_file):
        mock_file.side_effect = IOError("File not found")
        with self.assertRaises(OSError):
            output_json(self.json_data, self.task_number)

    @patch("builtins.open", new_callable=mock_open)
    def test_output_xml_exception(self, mock_file):
        mock_file.side_effect = IOError("File not found")
        with self.assertRaises(OSError):
            output_xml(self.xml_data, self.task_number)


if __name__ == "__main__":
    unittest.main()
