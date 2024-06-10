import sqlite3

def initialize_database():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('student_info_system.db')
        cursor = conn.cursor()

        # Create the users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                student_id TEXT NOT NULL,
                gender TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Database initialization completed successfully.")
    except sqlite3.Error as e:
        print("Database initialization failed:", e)

if __name__ == "__main__":
    initialize_database()
