# config.py
import os

# Project ROOT_DIR
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

# Secret key for session management. You can generate random strings here:
SECRET_KEY = 'XVc445646cdvdgHYYYfvdvslfbiuu335'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(ROOT_DIR, 'database.db')

PARSED_JSON_FOLDER = os.path.join(ROOT_DIR, "json_files")

if os.path.exists(PARSED_JSON_FOLDER) == False:
    os.mkdir(PARSED_JSON_FOLDER)