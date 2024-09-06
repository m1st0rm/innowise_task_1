FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change the start command to specify the parameters. With these parameters the script is guaranteed to run.
CMD ["python", "main.py", "--rooms", "rooms.json", "--students", "students.json", "--format", "json", "--dbc", "y"]
CMD ["python", "main.py", "--rooms", "rooms.json", "--students", "students.json", "--format", "xml", "--dbc", "y"]
