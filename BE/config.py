import urllib.parse

class Config:
    SECRET_KEY = '123456789'

    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=ANHBAHUNG;"
        "DATABASE=QUANLYSUCKHOE;"
        "UID=sa;"
        "PWD=123456789;"
        "TrustServerCertificate=yes;"
        "MARS_Connection=Yes;"
    )

    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"

    SQLALCHEMY_BINDS = {
        'backup': 'sqlite:///backup_vaccine.db?check_same_thread=False'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
