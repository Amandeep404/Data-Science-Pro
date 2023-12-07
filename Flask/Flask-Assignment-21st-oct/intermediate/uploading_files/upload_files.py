from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, SubmitField
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath('Flask/Flask-Assignment-21st-oct/intermediate/uploading_files/static/uploads')
app.config['SECRET_KEY'] = 'hey'
app.config['UPLOAD_PHOTOS_DIR'] = UPLOAD_FOLDER

photos = UploadSet('photos', IMAGES, default_dest=lambda app: app.config['UPLOAD_PHOTOS_DIR'])
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField("cover",
        validators=[
            FileAllowed(photos, 'Only images are allowed!!'),
            FileRequired('File should not be empty!')
        ]
    )
    submit = SubmitField('Upload')

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        file_name = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=file_name)
        print("File URL:", file_url) 
    else:
        file_url = None
    return render_template('upload.html', form=form, file_url=file_url)

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PHOTOS_DIR'], filename)

if __name__ == '__main__':
    app.run(debug=True)
