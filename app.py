import json
import random
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_DIR = '/data'
MEMES_FILE = os.path.join(DATA_DIR, 'memes.json')
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.json')


def load_memes():
    with open(MEMES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    tasks = load_tasks()
    meme = random.choice(load_memes())
    return render_template('index.html', tasks=tasks, meme=meme)


@app.route('/add', methods=['POST'])
def add():
    task_text = request.form.get('task', '').strip()
    if task_text:
        tasks = load_tasks()
        tasks.append({'id': len(tasks) + 1, 'text': task_text, 'done': False})
        save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['done'] = not t['done']
    save_tasks(tasks)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
