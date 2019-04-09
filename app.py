#!/usr/bin/python3.6
import os
import pickle

from base64 import b64decode
from flask import Flask, request, render_template, session

app = Flask(__name__)

User = type('User', (object,), {
    'uname': 'test',
    'is_admin': 0,
    '__repr__': lambda o: o.uname,
})


@app.route('/', methods=('GET',))
def index_handler():
    if not session.get('u'):
        u = pickle.dumps(User())
        session['u'] = u
    return render_template('index.html')


@app.route('/file', methods=('GET',))
def file_handler():
    path = request.args.get('file')
    path = os.path.join('static', path)
    if not os.path.exists(path) or '.py' in path \
            or '.sh' in path or '..' in path:
        return 'disallowed'
        
    with open(path, 'r') as fp:
        content = fp.read()
    return content


if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=False)
