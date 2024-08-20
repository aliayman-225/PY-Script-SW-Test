import unittest
import sqlite3
import os
import json
import csv
from unittest import mock
from io import StringIO
from task_script import create_database, insert_sample_data, export_to_csv, export_to_json, generate_report

class TestDatabaseFunctions(unittest.TestCase):
    records = [
        ("Ali Ayman", "aliayman225@gmail.com", "12511", "DevOps Engineer"),
        ("John Adel", "john@gmail.com", "14742", "Senior DevOps Engineer"),
        ("Nour Samir", "john@yahoo.com", "74885", "Software Engineer"),
        ("Karim Khaled", "karimkhaled@yahoo.com", "12511", "Software Engineer"),
        ("Karim Khaled", "karimkhaled@gmail.com", "78441", "Database Administrator"),
        ("Dalia Ahmed", "", "76543", "DevOps Engineer"),
        ("Mohamed Samir", "mohamedsamir@gmail.com", "", "Security Analyst"),
        ("Bahaa Ramy", "bahaaramy12@gmail.com", "12511", "Frontend Developer"),
        ("Rania Gaber", "rania_gaber@gmail.com", "", "Backend Developer"),
        ("Samy Mohamed", "samym@gmail.com", "12511", "QA Engineer")
    ]

    @classmethod
    def setUpClass(cls):
        """Set up a temporary database for testing."""
        cls.test_db_name = 'test_sample.db'
        create_database(db_name=cls.test_db_name)

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary database after tests."""
        if os.path.exists(cls.test_db_name):
            os.remove(cls.test_db_name)

    def tearDown(self):
        """Clean up the database after each test."""
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data")
        conn.commit()
        conn.close()

    def test_create_database(self):
        """Test the database creation and structure."""
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()

        # Check if the table 'data' exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists, "Table 'data' should exist after creation.")

        # Check if the table has the correct columns
        cursor.execute("PRAGMA table_info(data)")
        columns = [info[1] for info in cursor.fetchall()]
        expected_columns = ['id', 'name', 'email', 'zip_code', 'title']
        self.assertListEqual(columns, expected_columns, "Table 'data' should have the correct columns.")

        conn.close()

    def test_insert_sample_data(self):
        print("=================================================") 
        """Test inserting sample data into the database."""
        msg = insert_sample_data(self.records, db_name=self.test_db_name)
        formatted_msg = f"TEST: {msg}"
        print(formatted_msg)  # Output the formatted message

        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()

        # Check if records were inserted
        cursor.execute("SELECT COUNT(*) FROM data")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 10, "There should be 10 records in the table after insertion.")

        conn.close()

    def test_export_to_csv(self):
        print("=================================================") 
        """Test exporting data to a CSV file."""
        insert_sample_data(self.records, db_name=self.test_db_name)
        test_csv_file = 'test_data.csv'
        msg = export_to_csv(db_name=self.test_db_name, csv_file_path=test_csv_file)
        formatted_msg = f"TEST: {msg}"
        print(formatted_msg)  # Output the formatted message

        # Check if the CSV file was created
        self.assertTrue(os.path.exists(test_csv_file), "CSV file should be created.")

        # Check the contents of the CSV file
        with open(test_csv_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            rows = list(csv_reader)
            self.assertEqual(len(rows), 11, "CSV file should have 11 rows (1 header + 10 records).")

        os.remove(test_csv_file)

    def test_export_to_json(self):
        print("=================================================") 
        """Test exporting data to a JSON file."""
        insert_sample_data(self.records, db_name=self.test_db_name)
        test_json_file = 'test_data.json'
        msg = export_to_json(db_name=self.test_db_name, json_file_path=test_json_file)
        formatted_msg = f"TEST: {msg}"
        print(formatted_msg)  # Output the formatted message


        # Check if the JSON file was created
        self.assertTrue(os.path.exists(test_json_file), "JSON file should be created.")

        # Check the contents of the JSON file
        with open(test_json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 10, "JSON file should have 10 records.")

        os.remove(test_json_file)

    def test_generate_report(self):
        print("=================================================") 
        """Test the report generation."""
        insert_sample_data(self.records, db_name=self.test_db_name)
        test_csv_file = 'test_data.csv'
        test_json_file = 'test_data.json'
        export_to_csv(db_name=self.test_db_name, csv_file_path=test_csv_file)
        export_to_json(db_name=self.test_db_name, json_file_path=test_json_file)

        # Redirect stdout to capture print statements
        with StringIO() as buf, unittest.mock.patch('sys.stdout', new=buf):
            generate_report(csv_file_path=test_csv_file, json_file_path=test_json_file)
            output = buf.getvalue()
        self.assertIn("Total number of records: 10", output, "Report should correctly display the total number of records.")
        self.assertIn("DevOps Engineer: 2 occurrences", output, "Report should correctly display title frequency statistics.")
        print(f"\nReport successfully generated")

        os.remove(test_csv_file)
        os.remove(test_json_file)

if __name__ == '__main__':
    unittest.main()
