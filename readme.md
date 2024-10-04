# Innowise_task_1

This repository contains the implementation of Task 1 for the Innowise DE Trainee program. The task is divided into subtasks.

## Subtask List
#### Main Points
- Using a MySQL database (or another relational DBMS, such as PostgreSQL), create a data schema corresponding to the attached files (many-to-one relationship).
- Write a script that loads these two files and inserts the data into the database.
#### Required Database Queries
- List of rooms and the number of students in each room.
- 5 rooms with the lowest average age of students.
- 5 rooms with the largest age difference among students.
- List of rooms where male and female students live together.
#### Requirements and Remarks
- Suggest optimization options for queries using indexes.
- Generate an SQL query that adds the necessary indexes.
- Export the result in JSON or XML format.
- All "calculations" should be done at the database level.
- Use OOP and SOLID principles.
- No use of ORM (use SQL).
#### List of Command-Line Arguments
- students (path to the students file)
- rooms (path to the rooms file)
- format (output format: xml or json)
- dbc (whether to clear the database after the script execution) [ADDED BY INTERN]

## Installation

Copy the repository contents and run it in a virtual environment with the packages installed from `requirements.txt`.

```bash
git clone https://github.com/m1st0rm/innowise_task_1
pip install -r requirements.txt
```
## Usage
```bash
main.py [-h] --rooms ROOMS --students STUDENTS --format {xml,json} --dbc {y,n}

Parse data from rooms and students files, insert parsed data into the database, and return the results of specified SQL queries (task 1 - task 4) for this data in output files.

options:
  -h, --help           Show this help message and exit
  --rooms ROOMS        Path to the rooms file (*.json)
  --students STUDENTS  Path to the students file (*.json)
  --format {xml,json}  Output format: xml or json
  --dbc {y,n}          Does the database need to be cleaned after the script execution: y/n
```

## Author
Mikhail Bahamolau