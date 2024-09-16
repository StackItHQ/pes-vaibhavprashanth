from googleapiclient.discovery import build
from config import credentials, spreadsheet_id, cursor, db
import time

def fetch_data_from_google_sheet():
    """
    Fetch data from Google Sheets. Assumes the Google Sheet has columns: 
    id, name, age, and last_updated timestamp.
    """
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range="table1!A1:D").execute()
    return result.get('values', [])

def update_database(google_data):
    """
    Updates the MySQL database with data from Google Sheets. 
    The data should contain id, name, age, and last_updated timestamp.
    """
    for row in google_data:
        if len(row) == 4:  # Ensure the row has id, name, age, and last_updated timestamp
            google_id, google_name, google_age, google_timestamp = row
            google_timestamp=str(' '.join(google_timestamp.split('T')))

            # Fetch the corresponding record from the database
            cursor.execute("SELECT id, name, age, last_updated FROM table1 WHERE id = %s", (google_id,))
            result = cursor.fetchone()

            if result:
                db_id, db_name, db_age, db_timestamp = result
                if google_timestamp > str(db_timestamp):  # Compare timestamps
                    print(google_timestamp > str(db_timestamp), google_timestamp, str(db_timestamp))
                    # Google data is more recent, update MySQL
                    sql = "REPLACE INTO table1 (id, name, age, last_updated) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (google_id, google_name, google_age, google_timestamp))
                    print(f"Updated record in MySQL: {row}")
                else:
                    print(f"Skipped update, MySQL record is more recent: {row}")
            else:
                # No record found, insert new record into MySQL
                sql = "INSERT INTO table1 (id, name, age, last_updated) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (google_id, google_name, google_age, google_timestamp))
                print(f"Inserted new record into MySQL: {row}")
        else:
            print(f"Skipping row due to incorrect column count: {row}")
    db.commit()

def sync_google_sheet_to_db():
    """
    Syncs data from Google Sheets to MySQL. It fetches data from Google Sheets,
    checks for conflicts, and updates the MySQL database accordingly.
    """
    google_data = fetch_data_from_google_sheet()
    update_database(google_data)

def poll_google_sheets():
    """
    Continuously polls Google Sheets for updates every 10 seconds and syncs changes to MySQL.
    """
    while True:
        sync_google_sheet_to_db()
        time.sleep(10)  # Poll every 10 seconds
