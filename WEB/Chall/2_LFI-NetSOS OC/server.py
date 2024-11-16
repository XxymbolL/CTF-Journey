from flask import Flask, request, redirect
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Check if the 'page' parameter is already in the query string
    if 'page' not in request.args:
        # Redirect to the home page inside the templates directory
        return redirect('/?page=templates/home.html')
    
    # If 'page' is already set, continue serving the requested page
    return serve_page(request.args['page'])

@app.route('/<path:page>')
def serve_page(page):
    # Construct the file path using os.path.join for safer file handling
    file_path = os.path.join(os.getcwd(), page)  # This will allow paths like 'templates/home.html'
    
    try:
        # Check if the file exists before trying to open it
        if not os.path.exists(file_path):
            return "<h1>404 Not Found</h1><p>File does not exist.</p>"
        
        # Open and read the content of the specified file
        with open(file_path, 'r') as file:
            content = file.read()

        # Render the file content as plain text
        return f"<pre>{content}</pre>"

    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run(debug=True)
