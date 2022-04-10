from flask import Flask, render_template, request

from rq import Queue
from redis import Redis

from utils import find_path
import storage

app = Flask(__name__)
app.debug = True

conn = Redis('127.0.0.1', 6379)
q = Queue("Queue", connection=conn)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_page = request.form["start_page"]
        end_page = request.form["end_page"]
        q.enqueue(find_path, start_page, end_page)

    return render_template('index.html')


@app.route('/tasks', methods=['GET'])
def tasks():
    results = storage.read()
    return render_template('tasks.html', results=results)


if __name__ == '__main__':
    app.run()
