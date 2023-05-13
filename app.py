from flask import Flask, send_file, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import os
from datetime import datetime
from . import mainmaker

UPLOAD_FOLDER = 'static/temp'

app = Flask(__name__)
csrf = CSRFProtect(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def main():
    path = 'static/temp'
    location = os.listdir(path)
    if len(location) != 0:
        for file in location:
            os.remove(f'{path}/{file}')
    return render_template('index.html')


def name_maker():
    timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    return timestamp


@app.route('/maker', methods=['GET','POST'])
def maker():
    if request.method == 'POST':
        file = request.files['file']
        secure_filename(file.filename)
        updated_filename = name_maker()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{updated_filename}.mp3'))
        mainmaker.maker(updated_filename)
        audio_file = url_for('static', filename=f'temp/sm_{updated_filename}.mp3')
        return render_template('complete.html', output=audio_file)
    return render_template('index.html')


if __name__ == ' __main__':
    app.debug = True
    csrf.init_app(app)
    app.run()
