from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

CSV_FILE = 'students.csv'

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'first_name', 'last_name', 'age'])

def read_students():
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_students(students):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'first_name', 'last_name', 'age'])
        writer.writeheader()
        writer.writerows(students)

initialize_csv()

@app.route('/students', methods=['GET'])
def get_all_students():
    students = read_students()
    return jsonify(students), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    students = read_students()
    student = next((s for s in students if int(s['id']) == student_id), None)
    if student:
        return jsonify(student), 200
    return jsonify({'error': 'Student not found'}), 404

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not all(field in data for field in ['first_name', 'last_name', 'age']):
        return jsonify({'error': 'Missing required fields'}), 400

    students = read_students()
    new_id = max([int(s['id']) for s in students], default=0) + 1
    new_student = {
        'id': new_id,
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'age': data['age']
    }
    students.append(new_student)
    write_students(students)
    return jsonify(new_student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    if not all(field in data for field in ['first_name', 'last_name', 'age']):
        return jsonify({'error': 'Missing required fields'}), 400

    students = read_students()
    student = next((s for s in students if int(s['id']) == student_id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    student.update(data)
    write_students(students)
    return jsonify(student), 200

@app.route('/students/<int:student_id>', methods=['PATCH'])
def patch_student(student_id):
    data = request.get_json()
    if 'age' not in data:
        return jsonify({'error': 'Missing age field'}), 400

    students = read_students()
    student = next((s for s in students if int(s['id']) == student_id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    student['age'] = data['age']
    write_students(students)
    return jsonify(student), 200

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    students = read_students()
    student = next((s for s in students if int(s['id']) == student_id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    students = [s for s in students if int(s['id']) != student_id]
    write_students(students)
    return jsonify({'message': 'Student deleted successfully'}), 200

if __name__ == '__main__':
    initialize_csv()
    app.run(debug=True)