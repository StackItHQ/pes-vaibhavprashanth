from flask import Flask, render_template, jsonify, request
from googleapiclient.discovery import build
from google_sync import sync_google_sheet_to_db
from db_sync import sync_db_to_google_sheet, poll_database, fetch_data_from_db
import threading
import mysql.connector
from config import cursor, db, spreadsheet_id, credentials

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sync-data', methods=['POST'])
def sync_data():
    sync_google_sheet_to_db()
    sync_db_to_google_sheet()
    return "Data synced between Google Sheets and MySQL"

@app.route('/data', methods=['GET'])
def get_data():
    # Fetch data from the MySQL database
    cursor.execute("SELECT id, name, age FROM table1")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/add-data', methods=['POST'])
def add_data():
    data = request.json
    google_data = [data['id'], data['name'], data['age']]
    
    # Insert into SQL database
    sql = "INSERT INTO table1 (id, name, age) VALUES (%s, %s, %s)"
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

@app.route('/update-data', methods=['POST'])
def update_data():
    data = request.json
    
    # Update in SQL database
    sql = "UPDATE table1 SET name = %s, age = %s WHERE id = %s"
    cursor.execute(sql, (data['name'], data['age'], data['id']))
    db.commit()
    
    # Update in Google Sheets
    service = build('sheets', 'v4', credentials=credentials)
    range_name = "table1!A1:C"  # Adjust range if necessary
    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = response.get('values', [])
    
    # Find and update the row in Google Sheets
    updated_values = []
    for row in values:
        if row[0] == data['id']:
            updated_values.append([data['id'], data['name'], data['age']])
        else:
            updated_values.append(row)
    
    body = {
        'values': updated_values
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()
    
    return jsonify({"status": "Data updated successfully"}), 200

@app.route('/delete-data', methods=['POST'])
def delete_data():
    data = request.json
    id_to_delete = data['id']
    
    # Delete from SQL database
    sql = "DELETE FROM table1 WHERE id = %s"
    cursor.execute(sql, (id_to_delete,))
    db.commit()
    
    # Delete from Google Sheets
    service = build('sheets', 'v4', credentials=credentials)
    range_name = "table1!A1:D"  # Adjust range if necessary
    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = response.get('values', [])
    
    # Filter out the row to be deleted
    updated_values = [row for row in values if row[0] != id_to_delete]
    
    # Clear existing values in the range
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    
    # Update Google Sheets with the remaining rows
    body = {
        'values': updated_values
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()
    
    return jsonify({"status": "Data deleted successfully"}), 200

if __name__ == '__main__':
    threading.Thread(target=poll_database, daemon=True).start()
    app.run(port=5000)
