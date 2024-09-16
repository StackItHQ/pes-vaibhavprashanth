from googleapiclient.discovery import build
from config import credentials, spreadsheet_id, cursor, db
import time
from datetime import datetime

last_poll_time = time.time()

def fetch_changes_from_db():
    """
    Fetch changes from the database where the last_updated timestamp is greater than the last_poll_time.
    """
    cursor.execute("SELECT id, name, age, last_updated FROM table1 WHERE last_updated > %s", (last_poll_time,))
    return cursor.fetchall()

def fetch_data_from_db():
    """
    Fetch all data from the database table.
    """
    cursor.execute("SELECT id, name, age, last_updated FROM table1")
    return cursor.fetchall()

def convert_datetime_to_string(db_data):
    """
    Converts datetime fields in db_data to a string format (ISO 8601) for JSON serialization.
    """
    formatted_data = []
    for row in db_data:
        id, name, age, last_updated = row
        formatted_row = [id, name, age, last_updated.isoformat() if isinstance(last_updated, datetime) else last_updated]
        formatted_data.append(formatted_row)
    return formatted_data

def update_google_sheet(db_data):
    """
    Update Google Sheets with data from MySQL. Assumes the Google Sheet has columns for id, name, age, and last_updated.
    """
    service = build('sheets', 'v4', credentials=credentials)
    
    # Convert datetime to string before sending data
    db_data = convert_datetime_to_string(db_data)
    
    body = {
        'values': db_data
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range="table1!A1",
        valueInputOption="RAW", body=body).execute()

def sync_db_to_google_sheet():
    """
    Sync data from MySQL to Google Sheets. Fetches the most recent changes or the entire dataset if no changes are found.
    """
    global last_poll_time
    db_changes = fetch_changes_from_db()  # Get changes after the last poll time

    if db_changes:
        print(f"Updating Google Sheets with {len(db_changes)} changes from MySQL.")
        update_google_sheet(db_changes)
    else:
        print("No new changes found in the database.")

    last_poll_time = time.time()  # Update last poll time

def poll_database():
    """
    Poll the MySQL database for changes every 10 seconds and sync them with Google Sheets.
    """
    while True:
        sync_db_to_google_sheet()
        time.sleep(10)  # Poll every 10 seconds
