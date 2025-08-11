# import os

# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY") or "mealdonor_secret_key_2025"
#     SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root123@localhost/mealdonor_db"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "mealdonor_secret_key_2025"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'charity_db.sqlite3')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False