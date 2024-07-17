from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

HOMEWORK_FILE = 'homework.csv'
STUDENTS_FILE = 'students.csv'

def load_homework():
    try:
        with open(HOMEWORK_FILE, newline='') as f:
            reader = csv.reader(f)
            return [row for row in reader]
    except FileNotFoundError:
        return []

def save_homework(homeworks):
    with open(HOMEWORK_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(homeworks)

def load_students():
    try:
        with open(STUDENTS_FILE, newline='') as f:
            reader = csv.reader(f)
            return [row for row in reader]
    except FileNotFoundError:
        return []

def save_students(students):
    with open(STUDENTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(students)

@app.route('/')
def index():
    homeworks = load_homework()
    students = load_students()
    return render_template('index.html', homeworks=homeworks, students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_homework():
    if request.method == 'POST':
        title = request.form['title']
        due_date = request.form['due_date']
        student_ids = request.form.getlist('student_ids')

        homeworks = load_homework()
        for student_id in student_ids:
            homeworks.append([title, due_date, 'Pending', student_id])
        save_homework(homeworks)

        return redirect(url_for('index'))

    students = load_students()
    return render_template('add_homework.html', students=students)

@app.route('/import_students', methods=['GET', 'POST'])
def import_students():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join('/tmp', file.filename)
            file.save(filepath)
            with open(filepath, newline='') as f:
                reader = csv.reader(f)
                students = [row for row in reader]
                save_students(students)
            os.remove(filepath)
            return redirect(url_for('index'))
    return render_template('import_students.html')

@app.route('/view/<int:index>')
def view_homework(index):
    homeworks = load_homework()
    homework = homeworks[index]
    return render_template('view_homework.html', homework=homework, index=index)

@app.route('/submit/<int:index>')
def submit_homework(index):
    homeworks = load_homework()
    homeworks[index][2] = 'Submitted'
    save_homework(homeworks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
