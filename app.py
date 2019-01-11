# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request, make_response, render_template
from pymongo import MongoClient

app = Flask(__name__)

print(os.environ)
client = MongoClient('mongodb')
db = client.lucas
collection = db.estudantes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/modality-students/<modality>/<initial_date>/<final_date>')
def list_modality_students(modality, initial_date, final_date):
    students_pointer = collection.find(
        {'modalidade': modality.upper(), "data_inicio": {"$gte": initial_date, "$lte": final_date}}, {'_id': 0}).sort(
        'data_inicio', -1)
    students = []
    for student in students_pointer:
        students.append(student)

    return jsonify(students)


@app.route('/campus-courses/<campus>')
def list_campus_courses(campus):
    courses = collection.find({'campus': campus.upper()}, {'curso': 1}).distinct('curso')

    return jsonify(courses)


@app.route('/count-campus-students/<campus>/<initial_date>/<final_date>')
def count_campus_students(campus, initial_date, final_date):
    campus_students = collection.count(
        {'campus': campus.upper(), "data_inicio": {"$gte": initial_date, "$lte": final_date}})

    return jsonify(campus_students)


@app.route('/insert-student', methods=['POST'])
def insert_student():
    student = {}
    upper_fields = ['campus', 'curso', 'modalidade', 'nivel_do_curso']

    for key, value in request.form.items():
        student[key] = value if key not in upper_fields else value.upper()

    student_id = collection.insert_one(student).inserted_id

    if student_id:
        del student['_id']
        response = make_response(jsonify(student), 201)
        return response

    return 'Erro ao inserir o documento'


@app.route('/delete-student/<ra>/<campus>', methods=['DELETE'])
def delete_student(ra, campus):
    delete_result = collection.delete_one({'ra': ra, 'campus': campus})
    if delete_result.deleted_count > 0:
        return 'Documento excluido com sucesso'

    return 'Erro ao deletar documento'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
