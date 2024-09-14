from flask import Flask, jsonify
from google_sync import sync_google_sheet_to_db
from db_sync import sync_db_to_google_sheet

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Google Sheets - MySQL Sync App"

@app.route('/sync-google-to-db', methods=['POST'])
def sync_google_to_db():
    sync_google_sheet_to_db()
    return "Google Sheets synced to MySQL"

@app.route('/sync-db-to-google', methods=['POST'])
def sync_db_to_google():
    sync_db_to_google_sheet()
    return "MySQL synced to Google Sheets"

if __name__ == '__main__':
    app.run(port=5000)