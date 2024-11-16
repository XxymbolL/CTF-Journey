from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Function to check login and retrieve flag
def check_login(username, password):
    conn = sqlite3.connect('sqli_login_challenge.db')
    cursor = conn.cursor()

    # Vulnerable SQL query: no sanitization of user input
    query = f"SELECT flag FROM users WHERE username = '{username}' AND password = '{password}'"
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    conn.close()

    if result:
        return result[0]
    else:
        return "Invalid credentials"

@app.route('/')
def index():
    return '''
        <h1>Login</h1>
        <form action="/login" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check login and retrieve flag using the vulnerable function
    flag = check_login(username, password)
    
    return f"Result: {flag}"

if __name__ == "__main__":
    app.run(debug=True)
