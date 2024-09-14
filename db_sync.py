from googleapiclient.discovery import build
from config import credentials, spreadsheet_id, cursor, db

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
    db_data = fetch_data_from_db()
    update_google_sheet(db_data)