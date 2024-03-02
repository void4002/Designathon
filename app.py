from flask import Flask, render_template, request, redirect, url_for,session,jsonify
from generate_certificate import generate_certificate
import csv

app = Flask(__name__)

app.secret_key = "void"

def write_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data) 
def write_students(filename, students):
    fieldnames = ['name', 'address', 'age', 'roll_number', 'username', 'password', 'class', 'section', 
                  'timetable_id', 'attendance', 'pending_fee', 'subject_Math_grade', 
                  'subject_English_grade', 'subject_Science_Grade']
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
# Function to check if username and password match in a CSV file
def check_credentials(filename, username, password):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False
def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data
# Route for login page
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if username and password match in admins.csv
    if check_credentials('admins.csv', username, password):
        session['username'] = username  # Store the username in session
        return redirect(url_for('admin_dashboard'))

    # Check if username and password match in teachers.csv
    elif check_credentials('teachers.csv', username, password):
        session['username'] = username  # Store the username in session
        return redirect(url_for('teacher_dashboard'))

    # Check if username and password match in students.csv
    elif check_credentials('students.csv', username, password):
        session['username'] = username  # Store the username in session
        return redirect(url_for('student_dashboard'))

    else:
        return 'Login failed. Invalid username or password.'

# Admin dashboard route
@app.route('/admin')
def admin_dashboard():
    teachers_data = read_csv('teachers.csv')
    students_data = read_csv('students.csv')
    return render_template('admin.html', teachers=teachers_data, students=students_data)
    

# Route for adding a new teacher
@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    username = request.form['teacher_username']
    password = request.form['teacher_password']
    teacher_tid = request.form['teacher_ttid']
    with open('teachers.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password,teacher_tid])
    return redirect(url_for('admin_dashboard'))

# Route for adding a new student
@app.route('/add_student', methods=['POST'])
def add_student():
    # Retrieve all form fields from the request
    name = request.form['name']
    address = request.form['address']
    age = request.form['age']
    roll_number = request.form['roll_number']
    username = request.form['username']
    password = request.form['password']
    class_ = request.form['class']  # Using class_ instead of class to avoid conflict with Python keyword
    section = request.form['section']
    timetable_id = request.form['timetable_id']
    attendance = request.form['attendance']
    pending_fee = request.form['pending_fee']
    math_grade = request.form['subject_Math_grade']
    english_grade = request.form['subject_English_grade']
    science_grade = request.form['subject_Science_Grade']
    parent_key = request.form['parent_key']


    # Write the student data to the CSV file
    with open('students.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, address, age, roll_number, username, password, class_, section, timetable_id,
                         attendance, pending_fee, math_grade, english_grade, science_grade,0,parent_key])

    return redirect(url_for('admin_dashboard'))

@app.route('/remove_teacher', methods=['POST'])
def remove_teacher():
    teacher_username = request.form['teacher_username_remove']
    teachers = []

    # Read existing teachers from the CSV file
    with open('teachers.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != teacher_username:  # Skip the teacher to be removed
                teachers.append(row)

    # Write updated teachers to the CSV file
    with open('teachers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(teachers)

    return redirect(url_for('admin_dashboard'))

@app.route('/remove_student', methods=['POST'])
def remove_student():
    student_username = request.form['student_username_remove']
    students = []

    # Read existing students from the CSV file
    with open('students.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] != student_username:  # Skip the student to be removed
                students.append(row)

    # Write updated students to the CSV file
    write_students('students.csv', students)

    return redirect(url_for('admin_dashboard'))
# Teacher dashboard route
@app.route('/teacher')
def teacher_dashboard():
    students = read_csv('students.csv')
    return render_template('teacher.html',students=students)

@app.route('/change_student_attendance')
def change_student_attendance():
    students = read_csv('students.csv')
    return render_template('change_student_attendance.html', students=students)

@app.route('/update_attendance', methods=['POST'])
def update_attendance():
    # Get form data
    student_username = request.form['student_username']
    attendance = request.form['attendance']

    # Read data from students.csv
    students = read_csv('students.csv')

    # Update attendance for the corresponding student
    for student in students:
        if student['username'] == student_username:
            student['today_attendance'] = attendance

    # Write updated data back to students.csv
    write_csv('students.csv', students)

    return redirect(url_for('change_student_attendance'))

# Route for adding assignment
@app.route('/add_assignment')
def add_assignment():
    return render_template('add_assignment.html')

@app.route('/submit_assignment', methods=['POST'])
def submit_assignment():
    assignment_description=request.form['assignment_description']
    # Logic to handle assignment submission
    return redirect(url_for('teacher_dashboard'))

# Route for applying for leave
@app.route('/apply_leave')
def apply_leave():
    return render_template('apply_leave.html')

@app.route('/submit_leave', methods=['POST'])
def submit_leave():
    leave_reason = request.form['leave_reason']
    leave_dates = request.form['leave_dates']
    # Logic to handle leave application
    return redirect(url_for('teacher_dashboard'))

def get_pending_fee(username):
    with open('students.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return row['pending_fee']
    # Return None if username is not found
    return None

def get_parent_key(username):
    with open('students.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return row['parent_key']
    # Return None if username is not found
    return None

# Student dashboard route
@app.route('/student')
def student_dashboard():
    username = session.get('username') 
    pending_fee = get_pending_fee(username)
    parent_key = get_parent_key(username)
    time_table=read_csv('./output.csv')
    teachers=read_csv('./teachers.csv')
    if username:
        return render_template('student.html',parent_key=parent_key,username=username,pending_fee=pending_fee,tt=time_table,tch=teachers)
    else:
        return redirect(url_for('index')) 

@app.route('/payment')
def payment_form():
    return render_template('payment.html')

@app.route('/update')
def update_form():
    return render_template('update.html')

@app.route('/update_details',methods=['POST'])
def update_student():
    # Retrieve form data
    name = request.form['name']
    address = request.form['address']
    age = request.form['age']
    roll_number = request.form['roll_number']
    username = request.form['username']
    password = request.form['password']
    class_ = request.form['class']
    section = request.form['section']
    timetable_id = request.form['timetable_id']
    attendance = request.form['attendance']
    pending_fee = request.form['pending_fee']
    subject_Math_grade = request.form['subject_Math_grade']
    subject_English_grade = request.form['subject_English_grade']
    subject_Science_Grade = request.form['subject_Science_Grade']
    parent_key = request.form['parent_key']

    # Update CSV file
    with open('./students.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row['name'] == name:  # Assuming name is unique identifier
                row['address'] = address
                row['age'] = age
                row['roll_number'] = roll_number
                row['username'] = username
                row['password'] = password
                row['class'] = class_
                row['section'] = section
                row['timetable_id'] = timetable_id
                row['attendance'] = attendance
                row['pending_fee'] = pending_fee
                row['subject_Math_grade'] = subject_Math_grade
                row['subject_English_grade'] = subject_English_grade
                row['subject_Science_Grade'] = subject_Science_Grade
                row['parent_key'] = parent_key

    with open('./students.csv', mode='w', newline='') as file:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return redirect('/student')

@app.route("/certificate")
def certicate_gen():
    return render_template("certificate.html")

@app.route("/generate", methods=["POST"])
def generate():
    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")
        school_name = request.form.get("school_name")
        reason_for_transfer = request.form.get("reason_for_transfer")
        
        try:
            generate_certificate(name, date, school_name, reason_for_transfer)
            return jsonify({"success": True, "download_url": "./static/certificate.pdf"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
