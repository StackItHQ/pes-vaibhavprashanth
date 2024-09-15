from googleapiclient.discovery import build
from config import credentials, spreadsheet_id, cursor, db
import time

def fetch_data_from_google_sheet():
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range="table1!A1:C").execute()
    return result.get('values', [])

def update_database(google_data):
    for row in google_data:
        # Debugging: Print the row being inserted to track the values
        print(f"Updating row: {row}")
        sql = "REPLACE INTO table1 (id, name, age) VALUES (%s, %s, %s)"
        # Ensure each row has exactly 3 elements (id, name, age)
        if len(row) == 3:
            cursor.execute(sql, row)
        else:
            print(f"Skipping row due to incorrect column count: {row}")
    db.commit()

def sync_google_sheet_to_db():
    google_data = fetch_data_from_google_sheet()
    update_database(google_data)
    last_update_time = time.time()

def poll_google_sheets():
    while True:
        sync_google_sheet_to_db()
        time.sleep(10)
