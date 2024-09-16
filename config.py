import mysql.connector
from google.oauth2 import service_account

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
spreadsheet_id = '1PxsBTwIDxCTX1ko6UGyreZeidQIwALAeM2HJ_5coxds'

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="retracted",
    database="Superjoin_Assignment"
)
cursor = db.cursor()
