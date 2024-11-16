from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <h2>Welcome to the Secret Challenge</h2>
        <p>Access the <a href="/secret">secret area</a> to begin your quest.</p>
    '''

@app.route('/secret')
def secret():
    user_agent = request.headers.get('User-Agent')
    referer = request.headers.get('Referer')
    dnt = request.headers.get('DNT')

    # Step 1: Check User-Agent
    if user_agent != 'RistekBrowser':
        # First hint
        return '''
            <h2>Access Denied</h2>
            <p>It seems you're not using the right tool for the job. Only visitors using RistekBrowser can access our site.</p>
        '''
    # Step 2: Check Referer
    if referer != 'https://trustedsite.com':
        # Second hint
        return '''
            <h2>Access Denied</h2>
            <p>Your origin is unknown to us. You must be referred by https://trustedsite.com</p>
        '''
    # Step 3: Check DNT
    if dnt != '1':
        # Third hint
        return '''
            <h2>Access Denied</h2>
            <p>Your privacy settings are not enabled. We respect user privacy, please enable Do Not Track.</p>
        '''
    return '''
        <h2>Congratulations!</h2>
        <p>Here is your flag: <strong>NETSOS{HTTP_header_modification}</strong></p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
