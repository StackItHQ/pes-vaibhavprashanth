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
        sql = "REPLACE INTO table1 (id, name, age) VALUES (%s, %s, %s)"
        cursor.execute(sql, row)
    db.commit()

def sync_google_sheet_to_db():
    google_data = fetch_data_from_google_sheet()
    update_database(google_data)