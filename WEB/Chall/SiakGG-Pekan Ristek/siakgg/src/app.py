from flask import Flask, render_template, request, url_for, make_response, redirect
import jwt
import psycopg2
import bcrypt
import os

from middlewares import authenticated

app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DATABASE'] = psycopg2.connect(os.environ.get('DATABASE_URL'))
app.config['DATABASE'].autocommit = True

@app.route('/')
@authenticated
def index():
    username = get_username(request.cookies.get('token'))
    return render_template('main.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db: psycopg2.extensions.connection = app.config['DATABASE']
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM students WHERE username = %s', (request.form['username'],))
            user = cursor.fetchone()
            if not user or not bcrypt.checkpw(request.form['password'].encode('utf-8'), user[2].encode('utf-8')):
                return render_template('login.html', error='Incorrect username or password')
            else:
                token = jwt.encode({'sub': user[1]}, app.config['SECRET_KEY'], algorithm='HS256')
                response = make_response(redirect(url_for('index')))
                response.set_cookie('token', token)
                return response
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['username'] == '' or request.form['password'] == '':
            return render_template('register.html', error='Please fill in all fields')

        db: psycopg2.extensions.connection = app.config['DATABASE']

        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM students WHERE username = %s', (request.form['username'],))
            user = cursor.fetchone()
            if user:
                return render_template('register.html', error='Username already exists')
            else:
                password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor.execute('INSERT INTO students (username, password) VALUES (%s, %s)', (request.form['username'], password))
                db.commit()

                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/irs', methods=['GET'])
@authenticated
def lihat_irs():
    db = app.config['DATABASE']
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM students WHERE username = %s', (get_username(request.cookies.get('token')),))
        student = cursor.fetchone()

        cursor.execute('SELECT courses.id, courses.full_name, courses.description FROM courses INNER JOIN student_courses ON courses.id = student_courses.course_id WHERE student_id = %s', (student[0],))
        taken = cursor.fetchall()
    return render_template('irs.html', courses=taken)

@app.route('/irs/edit', methods=['GET', 'POST'])
@authenticated
def isi_irs():
    db = app.config['DATABASE']
    if request.method == 'POST':
        course_taken = request.form.getlist('course')
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM students WHERE username = %s', (get_username(request.cookies.get('token')),))
            student = cursor.fetchone()

            cursor.execute('SELECT * FROM courses')
            courses = cursor.fetchall()
            courses = [x for x in courses if "NETSOS" not in x]

            for course in courses:
                if course[0] in course_taken:
                    cursor.execute('SELECT * FROM student_courses WHERE student_id = %s AND course_id = %s', (student[0], course[0]))
                    if cursor.fetchone():
                        continue
                    cursor.execute('INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)', (student[0], course[0]))
                else:
                    cursor.execute('DELETE FROM student_courses WHERE student_id = %s AND course_id = %s', (student[0], course[0]))
            return redirect(url_for('lihat_irs'))

    query = request.args.get('search')
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM students WHERE username = %s', (get_username(request.cookies.get('token')),))
        student = cursor.fetchone()

        if query and "description" not in query:
            cursor.execute("SELECT * FROM courses WHERE name LIKE '%%%s%%' AND is_open = TRUE" % query)
        else:
            cursor.execute('SELECT * FROM courses WHERE is_open = TRUE')

        courses = cursor.fetchall()
        courses = [x for x in courses if os.getenv('FLAG') not in x]
        cursor.execute('SELECT * FROM student_courses WHERE student_id = %s', (student[0],))

        taken = [x[2] for x in cursor.fetchall()]
    return render_template('isi_irs.html', courses=courses, taken=taken)

@app.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('token')

    return response

def get_username(token):
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.exceptions.InvalidTokenError:
        return None
    return decoded['sub']

if __name__ == '__main__':
    app.run(port=8080, debug=True)
