from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def db_conect():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='sprint2'
    )

@app.route('/exercise', methods=['GET'])
def get_exercises():
    conn = db_conect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM exercise')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)

@app.route('/exercise/enter', methods=['POST'])
def enter_exercise():
    new_exercise = request.json
    conn = db_conect()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO exercise (name, principle_muscle) VALUES (%s, %s)',
        (new_exercise['name'], new_exercise['principle_muscle'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(new_exercise), 201

@app.route('/exercise/<int:id>', methods=['PUT'])
def update_exercise(id):
    update_exercise = request.json
    conn = db_conect()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE exercise SET name = %s, principle_muscle = %s WHERE id = %s',
        (update_exercise['name'], update_exercise['principle_muscle'], id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(update_exercise)

@app.route('/exercise/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    conn = db_conect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM exercise WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)