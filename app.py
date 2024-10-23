from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv

connection_string = 'mongodb+srv://test:sparta@hanif.gvakc.mongodb.net/'
client = MongoClient(connection_string)
db = client.dbsparta 

app = Flask(__name__)

# Tentukan path untuk menyimpan gambar di dalam folder static
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    # Validasi apakah title atau content kosong
    if not title_receive or not content_receive:
        return jsonify({'msg': 'Title and content cannot be empty!'}), 400

    # Mendapatkan file yang diunggah dari request
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f"{app.config['UPLOAD_FOLDER']}/post-{mytime}.{extension}"
    file.save(filename)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f"{app.config['UPLOAD_FOLDER']}/profile-{mytime}.{extension}"
    profile.save(profilename)  # Mengubah file.save menjadi profile.save

    time = today.strftime('%Y.%m.%d')

    # Simpan data title, content, dan path file ke MongoDB
    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time': time,    
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
