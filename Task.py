import sys
import subprocess
import sqlite3
import csv
import json
import os
import ast
import random
from collections import Counter



# No dependencies need to check as we're using only standard libraries


# Function to create the SQLite database and table
def create_database(db_name='sample.db'):
    """
    Creates a SQLite database and a table named 'data' if they do not exist.
    Parameters:
    db_name (str): The name of the SQLite database file.
    """

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            title TEXT NOT NULL
        )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
    finally:
        if conn:
            conn.close()


# Function to insert sample data into the database
def insert_sample_data(file_path, db_name='sample.db'):

    """
    Inserts data from a text file into the 'data' table in the SQLite database.
    Parameters:
    file_path (str): The path to the text file containing the records.
    db_name (str): The name of the SQLite database file.
    """

    try:
        # Read the contents of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Convert the content string to a list of tuples
        records = ast.literal_eval(content.strip())

        # Insert the records into the database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.executemany('''
        INSERT INTO data (name, email, zip_code, title)
        VALUES (?, ?, ?, ?)
        ''', records)
        conn.commit()
        
        return f"Inserted {cursor.rowcount} records into the 'data' table."
    
    except sqlite3.Error as e:
        return f"Error inserting sample data: {e}"
    except (SyntaxError, ValueError) as e:
        return f"Error parsing the records: {e}"
    finally:
        if conn:
            conn.close()



# Function to export data from the database to a CSV file
def export_to_csv(db_name='sample.db', csv_file_path='data.csv'):
    """
    Exports data from the 'data' table in the SQLite database to a CSV file.
    Parameters:
    db_name (str): The name of the SQLite database file.
    csv_file_path (str): The file path and name where the CSV file will be saved.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM data')
        rows = cursor.fetchall()

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header
            writer.writerow([i[0] for i in cursor.description])
            # Write the data rows
            writer.writerows(rows)
        print(f"Data successfully exported to {csv_file_path}")
    except (sqlite3.Error, IOError) as e:
        print(f"Error exporting data to CSV: {e}")
    finally:
        if conn:
            conn.close()
    return f"Data successfully exported to {csv_file_path}"

# Function to export data from the database to a JSON file
def export_to_json(db_name='sample.db', json_file_path='data.json'):
    """
    Exports data from the 'data' table in the SQLite database to a JSON file.
    Parameters:
    db_name (str): The name of the SQLite database file.
    json_file_path (str): The file path and name where the JSON file will be saved.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM data')
        rows = cursor.fetchall()
        # Convert rows into a list of dictionaries
        data = [{"id": row[0], "name": row[1], "email": row[2], "zip_code": row[3], "title": row[4]} for row in rows]

        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully exported to {json_file_path}")
    except (sqlite3.Error, IOError) as e:
        print(f"Error exporting data to JSON: {e}")
    finally:
        if conn:
            conn.close()
    return f"Data successfully exported to {json_file_path}"

# Function to read CSV and JSON files and generate a report
def generate_report(csv_file_path='data.csv', json_file_path='data.json', report_file_path='report.txt'):
    """
    Reads data from the CSV and JSON files and generates a report that includes:
    - Total number of records.
    - Sample records from the CSV file.
    - Title frequency statistics from the JSON file.
    - Additional statistics including unique counts and email provider percentages.
    
    Parameters:
    csv_file_path (str): The file path to the CSV file.
    json_file_path (str): The file path to the JSON file.
    report_file_path (str): The file path where the report will be saved.
    """
    try:
        if not os.path.exists(csv_file_path) or not os.path.exists(json_file_path):
            raise FileNotFoundError("CSV or JSON file not found. Please export the data first.")

        # Read and process the CSV file
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            rows = list(csv_reader)
            num_records = len(rows) - 1  # Subtract 1 for header row

        # Ensure there are enough records to sample
        sample_size = min(5, num_records)
        random_sample = random.sample(rows[1:], sample_size)  # Skip header row

        # Read and process the JSON file
        with open(json_file_path, mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        titles = [entry['title'] for entry in data]
        title_count = {title: titles.count(title) for title in set(titles)}

        # Additional statistics
        unique_names = len(set(entry['name'] for entry in data))
        unique_emails = len(set(entry['email'] for entry in data))
        unique_zip_codes = len(set(entry['zip_code'] for entry in data))
        most_common_zip_code = Counter(entry['zip_code'] for entry in data).most_common(1)[0]
        missing_name_count = sum(1 for entry in data if not entry['name'])
        missing_email_count = sum(1 for entry in data if not entry['email'])
        missing_zip_code_count = sum(1 for entry in data if not entry['zip_code'])
        missing_title_count = sum(1 for entry in data if not entry['title'])

        # Calculate email provider percentages
        total_emails = len([entry['email'] for entry in data if entry['email']])
        gmail_count = sum(1 for entry in data if entry['email'].endswith('@gmail.com'))
        yahoo_count = sum(1 for entry in data if entry['email'].endswith('@yahoo.com'))
        gmail_percentage = (gmail_count / total_emails) * 100 if total_emails else 0
        yahoo_percentage = (yahoo_count / total_emails) * 100 if total_emails else 0

        # Prepare the report content
        report_content = [

            f"\n------------------------------------------------------------------------------------------------",
            f"                             Total number of records: {num_records}",
            f"------------------------------------------------------------------------------------------------",

            f"\n====================================Sample records from CSV:====================================",
            *[str(row) for row in random_sample],  # Display the first 5 records
            f"================================================================================================",

            f"\n====================================Occurrences==================================================",
            *[f"{title}: {count} occurrences" for title, count in title_count.items()],
            f"\nUnique names: {unique_names} out of {num_records} names",
            f"Unique emails: {unique_emails} out of {num_records} emails",
            f"Unique zip codes: {unique_zip_codes} out of {num_records} zip codes",
            f"Most common zip code: {most_common_zip_code[0]} with {most_common_zip_code[1]} occurrences",
            f"================================================================================================",

            f"\n**************************Missings************************************************",
            f"* Missing name count: {missing_name_count} out of {num_records} names                                          *",
            f"* Missing email count: {missing_email_count} out of {num_records} emails                                        *",
            f"* Missing zip code count: {missing_zip_code_count} out of {num_records} zip codes                                  *",
            f"* Missing title count: {missing_title_count} out of {num_records} titles                                        *",
            f"**********************************************************************************",

            f"\n***********************Emails stats***********************",
            f"* Percentage of Gmail emails: {gmail_percentage:.2f}%                     *",
            f"* Percentage of Yahoo emails: {yahoo_percentage:.2f}%                     *"
            f"\n**********************************************************",
        ]

        # Print and save the report content
        with open(report_file_path, mode='w', encoding='utf-8') as report_file:
            for line in report_content:
                print(line)
                report_file.write(line + "\n")

        print(f"\nReport successfully saved to {report_file_path}")

    except (IOError, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error generating report: {e}")


# Main function to orchestrate the execution of all tasks
def main():
    """
    Main function that orchestrates the execution of:
    - Database creation
    - Insertion of sample data
    - Data export to CSV and JSON
    - Report generation
    """

    create_database()
    insert_sample_data("records_input.txt")
    export_to_csv()
    export_to_json()
    generate_report()

# Run the main function if this script is executed
if __name__ == '__main__':
    main()
