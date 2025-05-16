# importing the flask libraries
from flask import Flask, request, jsonify
app = Flask(__name__)

task = []

task_id_counter = 1


@app.route('/tasks',methods=['GET'])

def get_tasks():
    return jsonify(task), 200


if __name__ == '__main__':
    app.run(debug=True)

