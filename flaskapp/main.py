# -*- coding: utf-8 -*-
print('Hello world')
from flask import Flask
from PIL import Image
app = Flask(__name__)
from flask import render_template, request

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, TextField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

# from flask_bootstrap import Bootstrap
# bootstrap = Bootstrap(app)


# class NetForm(FlaskForm):
#  openid = StringField('openid', validators = [DataRequired()])
#  upload = FileField('Load image', validators = [
#                      FileRequired(),
#                      FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
#  recaptcha = RecaptchaField()
#  submit = SubmitField('send')
app.config['SECRET_KEY'] = "12345"

#  ключи recaptcha от google
app.config['RECAPTCHA_PUBLIC_KEY'] = "6Ld74-oUAAAAAJC0UOY6PtrOrNcxQ2VQCfGAqBOC"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6Ld74-oUAAAAAD2_Jl2IVKh2uCCI9OPX_7oTdLz4"
app.config['RECAPTCHA_DISABLE'] = True  # будет капча или нет

class ContactForm(FlaskForm):
    text = TextField('Введите что-нибудь, чтобы доказать, что Вы не робот:', validators=[DataRequired()])



UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def create_chart(path, root):
    from skimage import io
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    image = io.imread(path)

    _ = plt.hist(image.ravel(), bins=64, color='orange', )
    _ = plt.hist(image[:, :, 0].ravel(), bins=64, color='red', alpha = 0.5)
    _ = plt.hist(image[:, :, 1].ravel(), bins=64, color='Green', alpha = 0.5)
    _ = plt.hist(image[:, :, 2].ravel(), bins=64, color='Blue', alpha = 0.5)
    _ = plt.xlabel('Intensity Value')
    _ = plt.ylabel('Count')
    _ = plt.legend(['Total', 'Red Channel', 'Green Channel', 'Blue Channel'])

    plt.savefig(root)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global form
    form = ContactForm()
    global msg
    msg = ""
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                msg = "Успех!"
            else:
                msg = "Ошибка валидации"
                return render_template('mainPage.html',
                                       a = 1, b = 1, form = form, msg = msg)
            global file
            file = request.files['file']
            if file and (file.content_type.rsplit('/', 1)[1] in ALLOWED_EXTENSIONS).__bool__():
                global filename
                filename = secure_filename(file.filename)
                print(filename)
                file.save(app.config['UPLOAD_FOLDER'] + filename)
                return render_template('mainPage.html', picture = app.config['UPLOAD_FOLDER'] + filename,
                                       a = 1, b = 1, form = form, msg = msg)
        except Exception:
            print("Зашли в except")
            coeff = request.form.get('rescaleInputField')
            if (float(coeff) > 0):
                r_picture = Image.open(app.config['UPLOAD_FOLDER'] + filename)
                r_picture.load()
                coeff = float(coeff) / 100
                width, height = r_picture.size
                width = int(width*coeff)
                height = int(height*coeff)
                r_picture = r_picture.resize((width, height), Image.ANTIALIAS)
                r_picture.save(app.config['UPLOAD_FOLDER'] + 'resized' + filename)
                create_chart(app.config['UPLOAD_FOLDER'] + filename, app.config['UPLOAD_FOLDER'] + 'graph' + filename)
                create_chart(app.config['UPLOAD_FOLDER'] + 'resized' + filename, app.config['UPLOAD_FOLDER'] + 'graphresized' + filename)
                return render_template('mainPage.html', picture = app.config['UPLOAD_FOLDER'] + filename,
                                    picture_new = app.config['UPLOAD_FOLDER'] + 'resized' + filename,
                                    a = width, b = height,
                                    chart = app.config['UPLOAD_FOLDER'] + 'graph' + filename,
                                    chart_resized = app.config['UPLOAD_FOLDER'] + 'graphresized' + filename)

            return render_template('mainPage.html', picture = app.config['UPLOAD_FOLDER'] + filename, form = form, msg = msg) + "<p>Введено неверное значение!"

    return render_template('mainPage.html', picture = "", a = 1, b = 1, form = form, msg = msg)


# @app.route('/<path:filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)
  
from werkzeug.utils import secure_filename
import os
# import clr as neuronet

# '''@app.route("/net", methods=['GET', 'POST'])
# def net():
#   form = NetForm()
#   filename = None
#   neurodic = {}
#
#   if form.validate_on_submit():
#     filename = os.path.join('./static', secure_filename(form.upload.data.filename))
#     fcount, fimage = neuronet.read_image_files(10, './static')
#
#     decode = neuronet.getresult(fimage)
#
#     for elem in decode:
#       neurodic[elem[0][1]] = elem[0][2]
#     form.upload.data.save(filename)
#   return render_template('net.html',form = form, image_name = filename, neurodic = neurodic)
#     '''
if __name__ == "__main__":
  app.run(debug=True)
