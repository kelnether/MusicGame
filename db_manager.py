# -*- coding: utf-8 -*-
import pymysql
import hashlib

# MySQL database connection configuration – update these with your actual settings
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',         # Replace with your MySQL username
    'password': '123456', # Replace with your MySQL password
    'database': 'music_game',       # Replace with your database name
    'charset': 'utf8mb4'
}

def init_db():
    """Initialize the database and create the users table (if it does not exist)."""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            ''')
        connection.commit()
        print("User table initialized successfully.")
    except Exception as e:
        print("Error initializing database:", e)
    finally:
        connection.close()

def hash_password(password):
    """Hash the password using SHA-256 to prevent plain text storage."""
    if password is None:
        raise ValueError("Password cannot be None")
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(username, password):
    """
    Register a new user by storing the username and hashed password in the database.
    Returns True if registration is successful; False if the username already exists or an error occurs.
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, hash_password(password)))
        connection.commit()
        return True
    except pymysql.err.IntegrityError:
        # Username already exists
        return False
    except Exception as e:
        print("Error registering user:", e)
        return False
    finally:
        connection.close()

def verify_user(username, password):
    """
    Verify if the given username and password match.
    Returns True if verification passes; otherwise, returns False.
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            sql = "SELECT password FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row and row[0] == hash_password(password):
                return True
            return False
    except Exception as e:
        print("Error verifying user:", e)
        return False
    finally:
        connection.close()
