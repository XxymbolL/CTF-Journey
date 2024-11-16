from flask import Flask, request, make_response

app = Flask(__name__)

FLAG = "NETSOS{dicelupin_dijilat_diputar}"

@app.route('/')
def index():
    # Check if the 'role' cookie is set; if not, set it to 'user'
    role = request.cookies.get('role')
    response = make_response('''
        <h2>Welcome to the CTF Cookie Challenge!</h2>
        <p>Try to access the admin panel to get the flag.</p>
        <a href="/admin">Go to Admin Panel</a>
    ''')
    
    if not role:
        response.set_cookie('role', 'dXNlcg==')
    
    return response

@app.route('/admin')
def admin_panel():
    role = request.cookies.get('role')
    
    if role == "YWRtaW4=":
        return f"<h1>Welcome, Admin!</h1><p>Here is your flag: {FLAG}</p>"
    else:
        return "<h1>Access Denied</h1><p>You must be an admin to see the flag.</p>"

if __name__ == "__main__":
    app.run(debug=False)
