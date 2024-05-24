import calendar
import csv
from datetime import datetime, timedelta
import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from celery import Celery, Task
from celery.schedules import crontab
from jinja2 import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import *
from weasyprint import HTML
from flask_caching import Cache
from time import perf_counter_ns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'Aditya'
app.config['SECRET_KEY'] = 'Aditya'

current_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
    os.path.join(current_dir, "testdb.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/1",
        result_backend="redis://localhost:6379/2",
        enable_utc=False,
        timezone="Asia/Kolkata"
    ),
)
celery_app = celery_init_app(app)


def make_cache():
    cache_mapping = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": "localhost",
        "CACHE_REDIS_PORT": 6379
    }

    app.config.from_mapping(cache_mapping) 

    cache = Cache(app) 
    app.app_context().push()

    return cache


current_cache_inst = make_cache()


blocked_tokens = set()

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return str(jti) in blocked_tokens

@jwt.revoked_token_loader
def token_logout(jwt_header, jwt_payload):
    return ({"description": "User Logged out"}), 401  

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT =1025
SENDER_ADDRESS ="no-reply@ticketsforyou.com"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message, content = "text", attachment_file =None):
    mail = MIMEMultipart()
    mail["From"] = SENDER_ADDRESS
    mail["To"] = to_address
    mail["Subject"] = subject
    

    if content == "html":
        mail.attach(MIMEText(message, "html"))
    else:
        mail.attach(MIMEText(message, "plain"))

    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encode_base64(part)

        part.add_header(
            "Content-Disposition", f"attachment; filename={attachment_file}")
        mail.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()

    return True   



class User(db.Model):
    __tablename__ = 'user'
    User_id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String, nullable=False)
    UserName = db.Column(db.String, unique=True, nullable=False)
    Name = db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)
    Status = db.Column(db.String, default='User')
    Visit = db.Column(db.String, nullable = False)
    PlaylistR = db.relationship('Playlist', backref='user', lazy=True)
    RatingR = db.relationship('Rating', backref='user', lazy=True)
    AlbumR = db.relationship('Album', backref='user', lazy=True)
    SongR = db.relationship('Song', backref='user', lazy=True)

class Album(db.Model):
    __tablename__ = 'album'
    Album_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    Name = db.Column(db.String, nullable=False)
    Artist = db.Column(db.String, nullable=False)
    Genre =  db.Column(db.String, nullable=False)
    User_id = db.Column(db.Integer,db.ForeignKey('user.User_id'), nullable=False)
    SongR = db.relationship('Song', backref='album', lazy=True)


class Song(db.Model):
    __tablename__ = 'song'
    Song_id = db.Column(db.Integer, primary_key=True, autoincrement =True)
    Name = db.Column(db.String, nullable=False)
    Lyrics = db.Column(db.String, nullable=False)
    Artist = db.Column(db.String, nullable=False)
    Genre = db.Column(db.String, nullable=False)
    Song_path = db.Column(db.String, nullable=False)
    Rating = db.Column(db.Integer, default=0)
    User_id = db.Column(db.Integer,db.ForeignKey('user.User_id'), nullable=False)
    Album_id = db.Column(db.Integer, db.ForeignKey('album.Album_id'), nullable=False)
    Rating_relationship = db.relationship('Rating', backref='song', lazy=True)

class Playlist(db.Model):
    __tablename__ = 'playlist'
    Playlist_id = db.Column(db.Integer,primary_key = True)
    Name = db.Column(db.String, nullable=False)
    User_id = db.Column(db.Integer,db.ForeignKey('user.User_id'), nullable=False)
    Songs_list = db.Column(db.String, nullable=False)

class Rating(db.Model):
    __tablename__ = 'rating'
    Rating_id = db.Column(db.Integer,primary_key = True)
    User_id = db.Column(db.Integer, db.ForeignKey('user.User_id'))
    Song_id = db.Column(db.Integer, db.ForeignKey('song.Song_id'))
    Rating = db.Column(db.Integer)

user_signup_args = reqparse.RequestParser()
user_signup_args.add_argument("UserName", type=str, help="UserName required", required=True)
user_signup_args.add_argument("Name", type=str, help="Name required", required=True)
user_signup_args.add_argument("Email", type=str, help="Email required")
user_signup_args.add_argument("Password", type=str, help="Password required", required=True)


user_login_args = reqparse.RequestParser()
user_login_args.add_argument("UserName", type=str, help="UserName required", required=True)
user_login_args.add_argument("Password", type=str, help="Password required", required=True)

album_args = reqparse.RequestParser()
album_args.add_argument("Name", type=str, help="Album Name required", required=True)
album_args.add_argument("Artist", type=str, help="Album Artist required", required=True)
album_args.add_argument("Genre", type=str, help="Song Genre required", required=True)

song_args = reqparse.RequestParser()
song_args.add_argument("Name", type=str, help="SOng Name required", required=True)
song_args.add_argument("Lyrics", type=str, help="Song Lyrics required", required=True)
song_args.add_argument("Artist", type=str, help="Song Artist required", required=True)
song_args.add_argument("Song_path", type=FileStorage, help="Song File required", required=True)
song_args.add_argument("Genre", type=str, help="Song Genre required", required=True)

playlist_args = reqparse.RequestParser()
playlist_args.add_argument("Name", type=str, help="Playlist Name required", required=True)
playlist_args.add_argument("Songs_list", type=str, help="Song List required", required=True)

search_args = reqparse.RequestParser()
search_args.add_argument("SearchField", type=str, help="Search Field required", required=True)

resourse_fields_album = {
    "Album_id": fields.Integer,
    "Name":  fields.String,
    "Artist": fields.String,
    "Genre": fields.String,
    "User_id":fields.Integer
}

resourse_fields_song = {
    "Song_id": fields.Integer,
    "Name":  fields.String,
    "Artist": fields.String,
    "Lyrics": fields.String,
    "Song_path": fields.String,
    "Genre": fields.String,
    "Rating":fields.Integer,
    "Album_id":fields.Integer,
    "User_id":fields.Integer,
}

resourse_fields_search = {
    "Album_id": fields.Integer,
    "Name":  fields.String,
    "Artist": fields.String,
    "Genre": fields.String,
    "User_id":fields.Integer,
    "Song_id": fields.Integer,
    "Lyrics": fields.String,
    "Song_path": fields.String,
    "Rating":fields.Integer,
    "Songs_list":fields.String
}

resourse_fields_creatordashboard = {
    "Allalbums": fields.String,
    "Totalsongs":  fields.Integer,
    "AverageRatings": fields.Integer,
    "TotalAlbums": fields.Integer,
}

resourse_fields_playlist = {
    "Playlist_id": fields.Integer,
    "Name":  fields.String,
    "User_id": fields.Integer,
    "Songs_list": fields.String,
}

class UserSignup(Resource):
    def post(self):  
        args = user_signup_args.parse_args()
        UserName=args['UserName']
        user = User.query.filter_by(UserName=UserName).first()
        if user:
            abort(409)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        user =User(UserName=args['UserName'], 
                    Email=args['Email'], 
                    Name =args['Name'],
                    Password = args['Password'],
                    Visit = dt_string,
                     )
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.User_id)
        return {'token': token, 'UserName':args['UserName'] , 'User': user.Status}, 200


class UserLogin(Resource):
    def post(self):
        args = user_login_args.parse_args()
        UserName=args['UserName']
        Password=args['Password']
        
        user = User.query.filter_by(UserName=UserName, Password=Password).first()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if user != None and user.Status != "Admin":
            token = create_access_token(identity=user.User_id)
            user.Visit = dt_string
            db.session.commit()
            return {'token': token, 'UserName':UserName, 'User': user.Status}, 200
        elif user != None and user.Status == "Admin":
            return 201
        else:
            return 401

    @jwt_required()  
    def put(self):
        args = user_login_args.parse_args()
        UserName=args['UserName']
        Password=args['Password']
        
        user = User.query.filter_by(UserName=UserName, Password=Password).first()
        if get_jwt()["sub"] == user.User_id:
            user.Status = "Creator"
            db.session.commit()
            return 200
        return 401


@marshal_with(resourse_fields_song)
def getsongdata(genre):
    songs= Song.query.filter_by(Genre=genre).all()
    return songs


class AdminLogin(Resource):  
      def get(self, FlagSong=None):
        if FlagSong is None:
            user_count = User.query.filter_by(Status='User').count()
            creator_count = User.query.filter_by(Status='Creator').count()
            song_count = Song.query.count()
            album_count = Album.query.count()
            genres_count = db.session.query(Song.Genre).distinct().count()

            songs = Song.query.all()
            song_names = [song.Name for song in songs]
            ratings = [song.Rating for song in songs]

            plt.figure(figsize=(10, 6))
            plt.bar(song_names, ratings, color='blue')
            plt.xlabel('Songs')
            plt.ylabel('Ratings')
            plt.title('Songs and Ratings')
            plt.xticks(rotation=45, ha='right')

            img_bar = BytesIO()
            plt.savefig(img_bar, format='png')
            img_bar.seek(0)

            graph_html = base64.b64encode(img_bar.getvalue()).decode()

            labels = ['Creator', 'User']
            sizes = [creator_count, user_count]
            colors = ['blue', 'skyblue']

            plt.figure(figsize=(6, 6))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
            plt.axis('equal')

            img_pie = BytesIO()
            plt.savefig(img_pie, format='png')
            img_pie.seek(0)

            pie_chart_html = base64.b64encode(img_pie.getvalue()).decode()

            data = {"creator_count":creator_count, 
                    "user_count":user_count,
                    "song_count":song_count, 
                    "album_count":album_count, 
                    "genre_count":genres_count,
                    "graph_html":graph_html, 
                    "pie_chart_html":pie_chart_html}
            return data
        else:
            genres = db.session.query(Song.Genre).distinct().all()
            songs = []
            for g in genres:
                s=getsongdata(g[0])
                obj = {"genre":g[0], "songs":s}
                songs.append(obj)
            return songs


      def post(self): 
        args = user_login_args.parse_args()
        UserName=args['UserName']
        Password=args['Password']
        user = User.query.filter_by(UserName=UserName, Password=Password).first()
        if user != None and user.Status == "Admin":
            token = create_access_token(identity=user.User_id)
            return {'token': token, 'UserName':UserName, 'User': user.Status}, 200
        else:
            return 401
        
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = str(get_jwt()["jti"])
        UserName = str(get_jwt()["sub"])
        user = User.query.filter_by(UserName=UserName).first()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        user.Visit = dt_string
        db.session.commit()
        blocked_tokens.add(jti)
        return {"msg": "Succesfully logged out"}

class AlbumAPI(Resource): 
    @jwt_required()
    @marshal_with(resourse_fields_album)
    def get(self, Album_id=None, All=None):
        if Album_id is None and All is None:
            User_id = get_jwt()["sub"]
            albums = Album.query.filter_by(User_id=User_id).all()
            return albums
        elif Album_id and All is None:
            album = Album.query.filter_by(Album_id=Album_id).first()
            return album
        else:
            album = Album.query.all()
            return album
        
    @jwt_required()
    def post(self): 
        args = album_args.parse_args()
        user = get_jwt()["sub"]
        album = Album(Name=args['Name'], 
                    Artist=args['Artist'],
                    Genre = args['Genre'],
                    User_id=user
                    )
        db.session.add(album)
        db.session.commit()

        return 200
    
    @jwt_required()
    def put(self, Album_id):
        args = album_args.parse_args()
        album = Album.query.filter_by(Album_id=Album_id).first()
        if  get_jwt()["sub"] == album.User_id:
            album.Name = args['Name'] 
            album.Artist=args['Artist']
            album.Genre= args['Genre']

            db.session.commit()
            return 200
        return 401
    
    @jwt_required()
    def delete(self, Album_id):
        album = Album.query.filter_by(Album_id=Album_id).first()
        songs = Song.query.filter_by(Album_id=Album_id).all()
        song_api_instance = SongAPI()
        for s in songs:
            song_api_instance.delete(s.Song_id)

        db.session.delete(album)
        db.session.commit()
        return 200


class SongAPI(Resource): 
    @jwt_required()
    @marshal_with(resourse_fields_song)
    def get(self, Album_id=None, Song_id=None):
        if Album_id is None and Song_id:
            song = Song.query.filter_by(Song_id=Song_id).first()
            return song
        elif Album_id is None and Song_id is None:
            songs = Song.query.all()
            return songs
        else:
            songs = Song.query.filter_by(Album_id=Album_id).all()
            return songs
        

    @jwt_required()
    def post(self, Album_id): 
        user = str(get_jwt()["sub"])
        if 'Song_file' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 400

        file = request.files['Song_file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        upload_folder = '../client/src/assets'

        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        song = Song(
            Name=request.form['Name'], 
            Artist=request.form['Artist'],
            Lyrics=request.form['Lyrics'],
            Song_path=filename,
            Genre=request.form['Genre'],
            User_id=user,
            Album_id=Album_id
        )
        db.session.add(song)
        db.session.commit()
        return 200
    
    @jwt_required()
    def put(self, Song_id): 
        song = Song.query.filter_by(Song_id=Song_id).first()
        if  get_jwt()["sub"] == song.User_id:
            song.Name=request.form['Name']
            song.Artist=request.form['Artist']
            song.Lyrics=request.form['Lyrics']
            song.Genre=request.form['Genre']
            if 'Song_file' in request.files:
                file = request.files['Song_file']

                upload_folder = '../client/src/assets'

                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)

                song.Song_path = filename
            db.session.commit()
            return 200
        return 401
    
    @jwt_required()
    def delete(self, Song_id):
        song = Song.query.filter_by(Song_id=Song_id).first()
        ratings = Rating.query.filter_by(Song_id=Song_id).all()
        for r in ratings:
            db.session.delete(r)
            db.session.commit()

        db.session.delete(song)
        db.session.commit()
        return 200
        
class Rate(Resource):
    @jwt_required()
    def put(self, rate, Song_id): 
        User_id = get_jwt()["sub"]
        rating = Rating.query.filter_by(User_id=User_id, Song_id=Song_id).first()

        if rating:
            rating.Rating = rate
        else:
            r = Rating(User_id=User_id, Song_id=Song_id, Rating=rate)
            db.session.add(r)
            db.session.commit()
        
        ratings = Rating.query.filter_by(Song_id=Song_id).all()
        sum = 0
        for a in ratings:
            sum+= int(a.Rating)
        
        avg = sum/len(ratings)
        song = Song.query.filter_by(Song_id=Song_id).first()
        song.Rating = round(avg,2)
        db.session.commit()

        return 200
    
@marshal_with(resourse_fields_playlist)
def getplaylistdata(Playlist_id=None):
    if Playlist_id is None:
        User_id = get_jwt()["sub"]
        playlist =Playlist.query.filter_by(User_id=User_id).all()
        return playlist
    else:
        playlist = Playlist.query.filter_by(Playlist_id=Playlist_id).first()
        return playlist

class PlaylistAPI(Resource): 
    @jwt_required()
    def get(self, Playlist_id=None):
        song_api_instance = SongAPI()
        if Playlist_id is None:
            playlist = getplaylistdata()
            data = []
            for i in playlist:
                songs = {'playlist':i, 'songs':[]}
                for p in eval(i['Songs_list']):
                    song = song_api_instance.get(Song_id = p)
                    songs['songs'].append(song)
                data.append(songs)
            return data
        else:
            playlist = getplaylistdata(Playlist_id)
            print(playlist['Songs_list'])
            songs = {'playlist':playlist, 'songs':[]}
            for p in eval(playlist['Songs_list']):
                song = song_api_instance.get(Song_id = p)
                songs['songs'].append(song)
            return songs


    @jwt_required()
    def post(self): 
        args = playlist_args.parse_args()
        User_id = get_jwt()["sub"]
        Name = args['Name']
        Songs_list = args['Songs_list']
        print(Songs_list, Name)
        playlist = Playlist.query.filter_by(User_id=User_id, Name=Name).first()

        if playlist:
            playlist.Songs_list = str(list(set(eval(playlist.Songs_list) + [int(Songs_list)])))
            db.session.commit()

            return {'ID':playlist.Playlist_id}
        else:  
            p = Playlist(User_id=User_id, Name=Name, Songs_list = str([int(Songs_list)]))
            db.session.add(p)
            db.session.commit()

            return {'ID':p.Playlist_id}
        
    @jwt_required()
    def delete(self,Playlist_id=None, Song_id=None):
        playlist = Playlist.query.filter_by(Playlist_id=Playlist_id).first()
        if Song_id is None:
            db.session.delete(playlist)
            db.session.commit()
            return 200
        else:
            Songs_list = eval(playlist.Songs_list)
            if int(Song_id) in Songs_list:
                Songs_list.remove(int(Song_id))
                playlist.Songs_list= str(Songs_list)
                db.session.commit()
                return 200
            return 500
        
class Search(Resource): 
    @jwt_required()
    @marshal_with(resourse_fields_search)
    def post(self):
        args = search_args.parse_args()
        search_field = args['SearchField']
        songs_g = Song.query.filter(Song.Genre.ilike(search_field)).all()
        songs_n = Song.query.filter(Song.Name.ilike(search_field)).all()
        album_g = Album.query.filter(Album.Genre.ilike(search_field)).all()
        album_n = Album.query.filter(Album.Name.ilike(search_field)).all()
        song_api_instance = SongAPI()
        for a in album_g:
            a.Songs_list = song_api_instance.get(Album_id=a.Album_id)
        for n in album_n:
            n.Songs_list = song_api_instance.get(Album_id=n.Album_id)
        return [songs_g,songs_n, album_g, album_n]
    
class CreatorDashboard(Resource):
    @jwt_required()
    def get(self):
        User_id = get_jwt()["sub"]
        album_api_instance = AlbumAPI()
        allalbums =album_api_instance.get()
        songs = Song.query.filter_by(User_id=User_id).all()
        sum = 0
        for s in songs:
            sum+= int(s.Rating)
        if len(songs)==0:
            averageratings =0
        else:
            averageratings = round(sum/len(songs),2)

      
        data = {"allalbums": allalbums, 
        "totalsongs": len(songs),
        "averageratings": averageratings,
        "totalalbums": len(allalbums)}

        return data

@celery_app.on_after_finalize.connect
def setup_intervalTASK(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=28, hour=22), 
        send_reminder.s(), name="send_reminder"
    ),
    sender.add_periodic_task(
        crontab(minute=25, hour=23, day_of_month=7),
        monthly_report(), name="Monthly Report"
    )


@celery_app.task()
def send_reminder():
    users = User.query.filter_by().all() 
    now =  datetime.now()
    date_format = "%d/%m/%Y %H:%M:%S"
    send_reminder_to = []
    for user in users:
        lastvisit = datetime.strptime(user.Visit, date_format)
        if (now - lastvisit).total_seconds() >= 6400:
            send_reminder_to.append(user)
            

    with open(r"templates/reminder_mail.html") as file:  
        temp = Template(file.read())

    for user in send_reminder_to:
        message = temp.render(user=user)
        sub = f"[REMINDER] Films-Ticket-ForYou"
        send_email(to_address=user.Email, subject=sub, message=message, content="html")

    return {"msg": "send_reminder Complete"}

@celery_app.task()
def monthly_report(): 
    users = User.query.filter_by(Status='Creator').all()
    current_date = datetime.now()
    last_month = current_date.replace(day=1) - timedelta(days=1)
    year = last_month.year
    previous_month = last_month.month
    month = calendar.month_name[previous_month]

    for user in users:
        print(user)
        UserName = user.UserName
        Albums = Album.query.filter_by(User_id=user.User_id).all()
        Songs = Song.query.filter_by(User_id=user.User_id).all()

        data = [{
            "User": user,
            "Albums": Albums,
            "Songs": Songs
        }]
        
        with open(r"templates/monthly_report_mail.html") as file:
            temp = Template(file.read())
        
        u = {
            "UserName": UserName,
            "Year": year,
            "Month": month
        }

        message = temp.render(user=u)
        sub = f"[MONTHLY REPORT] MusicFusion"
        if len(data)!=0:
            create_pdf_report("templates/monthly_report_pdf.html",data)
            file = str(data[0]['User'].UserName)+ ".pdf"
            send_email(to_address=user.Email, subject=sub, message=message, content="html", attachment_file=file)
            os.remove(file)
    
    return {"msg": "monthly_report Complete"}


def format_report(template_file, data={}):
    with open(template_file) as file:
        template = Template(file.read())
        return template.render(data=data)
    
def create_pdf_report(template, data):
    template = template
    message = format_report(template, data=data)
    html = HTML(string=message)
    a = data[0]["User"].UserName
    file_name = str(a) + ".pdf"
    print(file_name)
    return  html.write_pdf(target=file_name)

    
api.add_resource(UserSignup,'/signup')
api.add_resource(UserLogin,'/login', '/registercreator')
api.add_resource(UserLogout,'/logout')
api.add_resource(AdminLogin,'/adminlogin', '/admindashboard', '/admindashboard/<FlagSong>')
api.add_resource(AlbumAPI,'/createalbum', '/updatealbum/<Album_id>','/albums', '/allalbums/<All>','/album/<Album_id>', '/deletealbum/<Album_id>')
api.add_resource(SongAPI,'/createsong/<Album_id>', '/updatesong/<Song_id>', '/songs/<Album_id>','/song/<Song_id>' ,'/allsongs' , '/deletesong/<Song_id>' )
api.add_resource(Rate,'/ratesong/<Song_id>/<rate>')
api.add_resource(PlaylistAPI,'/createplaylist', '/playlistsongs', '/playlistsongs/<Playlist_id>', '/deleteplaylist/<Playlist_id>', '/removesong/<Song_id>/<Playlist_id>')
api.add_resource(Search,'/search')
api.add_resource(CreatorDashboard,'/creatordashboard')

if __name__ == '__main__':
    app.run(debug=True, port=5000)