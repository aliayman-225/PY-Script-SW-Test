# Data Management and Reporting Script

This Python script manages a simple SQLite database, inserts sample data, exports the data to CSV and JSON formats, and generates a report based on the exported data. The script is designed to be easily runnable on any environment, with no external dependencies beyond the Python standard library.

## Features

- **Database Creation**: Creates a SQLite database with a table for storing sample data.
- **Data Insertion**: Inserts sample records into the database.
- **Data Export**: Exports the data to CSV and JSON files.
- **Report Generation**: Reads the exported files and generates a report that includes:
  - Total number of records.
  - Sample records from the CSV file.
  - Title frequency statistics from the JSON file.

## Prerequisites

- Python 3.x
    **OR**
- Docker
## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/aliayman-225/PY-Script-SW-Test
   cd <your-path>/PY-Script-SW-Test


## Install Dependencies

The script only uses standard Python libraries, so no additional dependencies are required.

## Database Creation

The SQLite database can be created in two ways:

1. **Automatically by the Script**: The script includes functionality to automatically create the SQLite database (sample.db) and the necessary table if they do not already exist. No additional steps are required on your part.

2. **Manually using DB Browser for SQLite**: Alternatively, you can create the database manually using a tool like DB Browser for SQLite. Simply create a new database named sample.db and add a table named data with the following fields:
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- name (TEXT)
- email (TEXT)
- zip_code (TEXT)
- title (TEXT)

## Input Data

The script requires an input file (`records_input.txt`) that contains the records to be inserted into the database. This file should be a text file with a list of tuples, where each tuple represents a record to be inserted into the database.

### Input Format

The records in the input file should be formatted as follows:

```plaintext
[
    ("John Doe", "john.doe@gmail.com", "12345", "Manager"),
    ("Jane Smith", "jane.smith@yahoo.com", "54321", "Engineer"),
    ...
]
```

## Output Files

After running the script, you will find the following files in the directory:
- sample.db: The SQLite database file.
- data.csv: The CSV file containing the exported data.
- data.json: The JSON file containing the exported data.
- report.txt: Text file containing the report generated by the script

## Usage

**Option 1**: Using Python Directly
To execute the script, use the following command:
```bash
python task_script.py
```
**Option 2**: Using Docker
Alternatively, you can run the script inside a Docker container without needing to install Python or any dependencies on your system.
```bash
docker build -t my-app
docker run --rm -v $(pwd):/app my-app
```

The script will perform the following tasks:
- Create a SQLite database (sample.db).
- Insert sample data into the database.
- Export the data to data.csv and data.json.
- Generate a report based on the exported data and display it in the console.

## Report Example

Also the report generated by the script will be printed to the console and includes:
- The total number of records in the database.
- Random Sample records from the CSV file.
- Title frequency statistics from the JSON file.
- Unique names statistics from the JSON file.
- Unique emails statistics from the JSON file.
- Unique zip codes statistics from the JSON file.
- Most common zip code statistics from the JSON file.
- Number of records that contains missing data.
- Email Type statistics from the JSON file.

![image](https://github.com/user-attachments/assets/4f3db1c7-aa36-490b-8981-77f315beea64)



## Running the Tests

To run the unit tests, navigate to the project directory and execute the following command:

```bash
python -m unittest test_script.py
```

This command will run all the test cases defined in test_script.py, including:
- Database creation verification
- Inserting sample data into the database
- Exporting data to CSV and JSON files
- Generating a report based on the exported data
- Output from each test, including any messages and the status of test cases, will be displayed in the console.

![image](https://github.com/user-attachments/assets/e95d91ba-5e4b-4dac-90fb-ec3b4e16fc65)
