import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    BOX_CLIENT_ID = os.environ.get('BOX_CLIENT_ID')
    BOX_CLIENT_SECRET = os.environ.get('BOX_CLIENT_SECRET')
    BOX_REDIRECT_URI = os.environ.get('BOX_REDIRECT_URI')
    TEMP_FOLDER = os.environ.get('TEMP_FOLDER') or 'temp_files'
    FILE_RETENTION_HOURS = int(os.environ.get('FILE_RETENTION_HOURS') or 24)
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'

