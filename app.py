from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import os

app = Flask(__name__)

# Database connection parameters
server = 'simpleconnection.database.windows.net'
database = 'simpleconnection'
username = 'prof'
password = '#Password1'
driver = '{ODBC Driver 17 for SQL Server}'

def get_db_connection():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_course', methods=['POST'])
def add_course():
    course_name = request.form['course_name']
    course_description = request.form['course_description']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Courses (CourseName, CourseDescription)
        VALUES (?, ?)
    """, (course_name, course_description))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
