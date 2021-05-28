print('Hello world')
from flask import Flask
app = Flask(__name__)

# decorator dlya vivoda stranitcy po umolchaniu

from flask import render_template

@app.route("/data_to")
def data_to():
  some_pars = {'user':'Ivan', 'color':'red'}
  some_str = 'Hello my dear friends!'
  some_value = 10
  
  return render_template('simple.html', some_str = some_str, some_value = some_value,
                          some_pars = some_pars)

@app.route("/")
def hello():
  return "<html><title>Some title</title><body><h1>Some text<h1></body></html>"

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'PLACE KEY FROM GOOGLE HERE'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'PLACE SECRET KEY FROM GOOGLE HERE'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

class NetForm(FlaskForm):
  openid = StringField('openid', validators = [DataRequired()])
  upload = FileField('Load image', validators = [
                      FileRequired(),
                      FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
  recaptcha = RecaptchaField()
  submit = SubmitField('send')
  
from werkzeug.utils import secure_filename
import os
import clr as neuronet

@app.route("/net", methods=['GET', 'POST'])
def net():
  form = NetForm()
  filename = None
  neurodic = {}
  
  if form.validate_on_submit():
    filename = os.path.join('./static', secure_filename(form.upload.data.filename))
    fcount, fimage = neuronet.read_image_files(10, './static')
    
    decode = neuronet.getresult(fimage)

    for elem in decode:
      neurodic[elem[0][1]] = elem[0][2]
    form.upload.data.save(filename)
  return render_template('net.html',form = form, image_name = filename, neurodic = neurodic)
    
if __name__ == "__main__":
  app.run(host='127.0.0.1', port=5000)
