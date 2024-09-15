from flask import Flask, render_template, jsonify, request
from googleapiclient.discovery import build
from google_sync import sync_google_sheet_to_db
from db_sync import sync_db_to_google_sheet, fetch_data_from_db, poll_database
import threading
import mysql.connector
from config import cursor, db, spreadsheet_id, credentials
import logging

app = Flask(__name__)

# Landing page
@app.route('/')
def home():
    return render_template('index.html')

# View Data Page
@app.route('/view-data', methods=['GET'])
def view_data():
    cursor.execute("SELECT id, name, age FROM table1")
    data = cursor.fetchall()
    return render_template('view_data.html', data=data)

# Add Data Page
@app.route('/add-data-page', methods=['GET'])
def add_data_page():
    return render_template('add_data.html')

# Add Data Functionality
@app.route('/add-data', methods=['POST'])
def add_data():
    data = request.json
    google_data = [data['id'], data['name'], data['age']]
    
    # Insert into SQL database
    sql = "INSERT INTO table1 (id, name, age, last_updated) VALUES (%s, %s, %s, NOW())"
    cursor.execute(sql, (data['id'], data['name'], data['age']))
    db.commit()
    
    # Insert into Google Sheets
    service = build('sheets', 'v4', credentials=credentials)
    body = {
        'values': [google_data]
    }
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range="table1!A1",
        valueInputOption="RAW", body=body).execute()
    
    return jsonify({"status": "Data added successfully"}), 200

# Update Data Page
@app.route('/update-data-page', methods=['GET'])
def update_data_page():
    return render_template('update_data.html')

# Update Data Functionality
@app.route('/update-data', methods=['POST'])
def update_data():
    data = request.json
    google_data = [data['id'], data['name'], data['age']]
    
    # Update SQL database
    sql = "REPLACE INTO table1 (id, name, age, last_updated) VALUES (%s, %s, %s, NOW())"
    cursor.execute(sql, (data['id'], data['name'], data['age']))
    db.commit()
    
    # Trigger sync to Google Sheets
    sync_db_to_google_sheet()
    
    return jsonify({"status": "Data updated successfully"}), 200

# Delete Data Page
@app.route('/delete-data-page', methods=['GET'])
def delete_data_page():
    return render_template('delete_data.html')

# Delete Data Functionality
@app.route('/delete-data', methods=['POST'])
def delete_data():
    data = request.json
    row_id = data['id']
    
    # Delete from SQL database
    cursor.execute("DELETE FROM table1 WHERE id = %s", (row_id,))
    db.commit()
    
    # Delete from Google Sheets
    service = build('sheets', 'v4', credentials=credentials)
    range_name = f"table1!A{row_id}:D{row_id}"
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    
    return jsonify({"status": "Data deleted successfully"}), 200

# Sync Data between Google Sheets and MySQL
@app.route('/sync-data', methods=['POST'])
def sync_data():
    try:
        sync_google_sheet_to_db()
        sync_db_to_google_sheet()
        return jsonify({"status": "Data synced between Google Sheets and MySQL"}), 200
    except Exception as e:
        logging.error(f"Error syncing data: {e}")
        return jsonify({"status": "Error syncing data"}), 500

if __name__ == '__main__':
    threading.Thread(target=poll_database, daemon=True).start()
    app.run(port=5000)