import os
from flask import Flask
from flask import render_template

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def main():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3306, debug=True)
