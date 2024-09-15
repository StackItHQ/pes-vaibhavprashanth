from googleapiclient.discovery import build
from config import credentials, spreadsheet_id, cursor, db
import mysql.connector
from config import cursor, db, spreadsheet_id
import time

last_poll_time = time.time()

def fetch_changes_from_db():
    cursor.execute("SELECT * FROM change_log WHERE timestamp > %s", (last_poll_time,))
    return cursor.fetchall()

def fetch_data_from_db():
    cursor.execute("SELECT id, name, age FROM table1")
    return cursor.fetchall()

def update_google_sheet(db_data):
    service = build('sheets', 'v4', credentials=credentials)
    body = {
        'values': db_data
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range="table1!A1",
        valueInputOption="RAW", body=body).execute()

def sync_db_to_google_sheet():
    global last_poll_time
    db_changes = fetch_changes_from_db()
    db_data = fetch_data_from_db()
    update_google_sheet(db_data)
    last_poll_time = time.time()

def poll_database():
    while True:
        sync_db_to_google_sheet()
        time.sleep(10)  # Poll every 10 seconds