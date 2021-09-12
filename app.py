#!.venv/bin/python
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, TextField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired
from data import ACTORS
from modules import get_names, get_actor, get_id
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import speech_recognition as sr
import sys

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'ASDJALSKJDKJHQKJEFLHQEKJFHAKSADLKJSDHQKJWHD'

# Flask-Bootstrap requires this line
Bootstrap(app)
def run_recognizer(audio_filename, backend):

    r = sr.Recognizer()

    with sr.AudioFile('./uploads/' + audio_filename) as source:
        audio = r.record(source)

    if backend == 'local':
        res = r.recognize_sphinx(audio)
    elif backend == 'google':
        res = r.recognize_google(audio)

    return res

class NameForm(FlaskForm):
    audio_file = FileField(validators=[FileRequired()])
    recognizer = SelectField('Recognizer', choices=[('local','local'),('google','google')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        backend = form.recognizer.data
        filename = secure_filename(form.audio_file.data.filename)
        form.audio_file.data.save('uploads/' + filename)
        message = run_recognizer(filename, backend) 
    return render_template('index.html', form=form, message=message)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)

