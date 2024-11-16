import sqlite3

# Create the SQLite database and add the users table
conn = sqlite3.connect('sqli_login_challenge.db')
cursor = conn.cursor()

# Create table for users
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY, 
                    username TEXT, 
                    password TEXT,
                    flag TEXT)''')

# Insert a couple of users (one of them will have the flag)
cursor.execute("INSERT INTO users (username, password, flag) VALUES ('admin', 'admin123', 'NETSOS{sekali_skali_sqli}')")
cursor.execute("INSERT INTO users (username, password, flag) VALUES ('user', 'user123', '')")

# Commit changes and close the connection
conn.commit()
conn.close()
