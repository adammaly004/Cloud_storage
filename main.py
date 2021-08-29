from flask import Flask, flash, request, redirect, send_file, render_template, url_for
import os
from werkzeug.utils import secure_filename
import shutil

# Defining constants
IPv4 = "your_IPv4"
PORT = 1111

UPLOAD_FOLDER = 'your_path/Cloud_storage/static/server/'
FOLDER = os.listdir(UPLOAD_FOLDER)
LOWER_FOLDER = len(UPLOAD_FOLDER.split("/"))
WORKSPACE = UPLOAD_FOLDER.split("/")[-2] + "/"

# Starting flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.static_folder = 'static'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Uploading files


@ app.route('/', methods=['GET', 'POST'])
def files():
    FOLDER = os.listdir(app.config['UPLOAD_FOLDER'])
    p = app.config['UPLOAD_FOLDER'].rsplit('/', 2)
    flash(p[1])
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            FOLDER.append(filename)

    return render_template('file.html', value=FOLDER, only_folder="False", file_to_move=None, actual_path=app.config['UPLOAD_FOLDER'].replace("/", " "))


# Downloading files


@ app.route('/return-files/<filename>', methods=['GET', 'POST'])
def download_file(filename):
    file_path = app.config['UPLOAD_FOLDER'] + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


# Going through the folders


@ app.route('/directory/<folder>/<only_folder>/<file_to_move>', methods=['GET', 'POST'])
def directory(folder, only_folder, file_to_move):
    if folder not in app.config['UPLOAD_FOLDER']:
        app.config['UPLOAD_FOLDER'] = app.config['UPLOAD_FOLDER'] + folder + "/"
    else:
        return redirect("/")
    if only_folder == "True":
        return redirect(f"/move-mode/{file_to_move}")
    return redirect("/")


# Going back in folders


@ app.route('/back/<only_folder>/<file_to_move>', methods=['GET', 'POST'])
def back(only_folder, file_to_move):
    rout = app.config['UPLOAD_FOLDER'].split('/')
    length = len(rout)

    if length > LOWER_FOLDER:
        route = app.config['UPLOAD_FOLDER'].rsplit('/', 2)
        r = route[0] + '/'
    else:
        r = app.config['UPLOAD_FOLDER']

    app.config['UPLOAD_FOLDER'] = r
    if only_folder == "True":
        return redirect(f"/move-mode/{file_to_move}")
    return redirect("/")


# Creating a folders


@ app.route('/new-folder', methods=['GET', 'POST'])
def new_folder():
    if request.method == 'POST':
        if 'folder' not in request.form:
            return redirect("/")
        else:
            folder_name = request.form.get('folder')
            path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
            try:
                os.mkdir(path)
            except Exception:
                flash("Write the name")
            return redirect("/")
    return redirect("/")


# Deleting files and empty folders


@ app.route('/delete/<file>', methods=['GET', 'POST'])
def delete(file):
    try:
        if "." in file:
            os.remove(app.config['UPLOAD_FOLDER'] + file)
        else:
            os.rmdir(app.config['UPLOAD_FOLDER'] + file + "/")
    except Exception:
        flash("The directory is not empty")

    return redirect("/")


# Moving mode


@ app.route('/move-mode/<file>', methods=['GET', 'POST'])
def move_mode(file):
    FOLDER = os.listdir(app.config['UPLOAD_FOLDER'])
    p = app.config['UPLOAD_FOLDER'].rsplit('/', 2)
    flash(p[1])
    return render_template('file.html', value=FOLDER, only_folder="True", file_to_move=file, actual_path=app.config['UPLOAD_FOLDER'].replace("/", " "))


# Moving files


@ app.route('/move/<file>', methods=['GET', 'POST'])
def move(file):
    start_pos = file.replace(" ", "/")
    try:
        shutil.move(start_pos, app.config["UPLOAD_FOLDER"])
    except Exception:
        flash("Destination path already exists")
    return redirect("/")


# Preview


@ app.route('/preview/<file>', methods=['GET', 'POST'])
def preview(file):
    path = app.config['UPLOAD_FOLDER']

    if ".txt" in file:
        with open(path + file, 'r', encoding="utf-8") as file:
            file = file.read().replace('\n', '')

    elif ".png" in file or ".jpg" in file or ".jpeg" in file or ".jfif" in file or ".gif" in file or ".ico" in file or ".svg" in file or ".mp4" in file:
        path = path.replace(UPLOAD_FOLDER, "") + WORKSPACE
        file = path + file

    else:
        pass

    return render_template('preview.html', file=file)


# Restarting main route -> app.config['UPLOAD_FOLDER']


@ app.route("/restart")
def restart():
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    return redirect("/")


# Run flask app
if __name__ == "__main__":
    app.run(debug=True, host=IPv4, port=PORT)
