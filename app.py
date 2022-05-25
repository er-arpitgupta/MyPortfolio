from flask import Flask, flash, redirect, request, render_template, send_from_directory
from os import listdir, remove
from flask_sqlalchemy import SQLAlchemy
from pytube import YouTube, Playlist
from zipfile import ZipFile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    mail = db.Column(db.String(100)) 
    msg = db.Column(db.String(500))

    def __init__(self, name, phone, mail, msg) -> None:
        self.name = name
        self.phone = phone
        self.mail = mail
        self.msg = msg

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.form.get('name'):
        data = Data(request.form.get('name'), request.form.get('phone'), request.form.get('mail'), request.form.get('msg'))
        db.session.add(data)
        db.session.commit()
        flash('Message sent. Thank you for contacting us! 😇')
        return render_template('index.html')
    return render_template('index.html')

@app.route('/feed_data', methods=['GET', 'POST'])
def fetch():
    return render_template('data.html', data = Data.query.all())

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory('data/', filename)

@app.route('/ytd', methods=['GET', 'POST'])
def youtube():
    if request.form.get('link'):
        if 'list=PL' in request.form.get('link'):
            try:
                urls = Playlist(request.form.get('link')).video_urls
                for url in urls: 
                    YouTube(str(url)).streams.get_lowest_resolution().download('data/')
            except: 
                flash('Playlist not found')
                return render_template('youtube.html', flag=False)
        else: 
            try: YouTube(str(request.form.get('link'))).streams.get_highest_resolution().download('data/')
            except: 
                flash('Video not found')
                return render_template('youtube.html', flag=False)
            flag1 = True
        files = listdir('data/')
        if 'videos.zip' in files: remove('data/videos.zip')
            
        with ZipFile('data/videos.zip', 'w') as f:
            for file in files: 
                if file!='videos.zip' and file!='Arpit_CV.pdf': f.write('data/'+file)

        for file in files: 
            if file!='Arpit_CV.pdf' and file!='videos.zip': remove('data/'+str(file))

        return render_template('youtube.html', flag=True)
    return redirect('/')

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)