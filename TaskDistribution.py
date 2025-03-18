from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def distribute_tasks(tasks, workers):
    task_distribution = {worker: [] for worker in workers}

    for i, task in enumerate(tasks):
        worker = workers[i % len(workers)]
        task_distribution[worker].append(task)

    return task_distribution


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/distribute', methods=['POST'])
def distribute():
    tasks = []
    workers = request.form.get('workers', '').split(',')

    if 'tasks_file' in request.files:
        file = request.files['tasks_file']
        if file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            with open(filepath, 'r') as f:
                tasks = f.read().splitlines()

    if not tasks or not workers:
        return jsonify({"error": "Tasks and workers are required."}), 400

    distribution = distribute_tasks(tasks, workers)
    return jsonify(distribution)


if __name__ == '__main__':
    app.run(debug=True)