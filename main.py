from PIL import Image, ExifTags
from bottle import route, app, Request, request, run, template
from peewee import SqliteDatabase, Model, CharField, TextField
import os
import datetime
import face_recognition
import hashlib


salt = "648739fhpoevevedlsdsvkjfbue;?dkfbv745" #asenda suvalise kombinatsiooniga
db = SqliteDatabase('kasutajad.db')


class Kasutaja(Model):
    kasutajanimi = CharField()
    parool = CharField()
    kasutaja_tekst = TextField()

    class Meta:
        database = db  

db.connect()
db.create_tables([Kasutaja])


@route('/')
def index():
    return template("./templates/index.tpl")


@route('/login')
def login():
    return template("./templates/login.tpl")


@route('/register')
def register():
    return template("./templates/register.tpl")


@route('/error')
def error():
    return template("./templates/error.tpl", error="")


@route('/updatenotepad', method='POST')
def update_notepad():
    kasutajanimi = request.forms.get('kasutajanimi')
    parool = request.forms.get('parool')
    tekst = request.forms.get('notepadtext')
    hashed_parool = parool
    kasutaja = Kasutaja.get(Kasutaja.kasutajanimi == kasutajanimi)

    if kasutaja.parool == hashed_parool:
        kasutaja.kasutaja_tekst = tekst.strip()
        kasutaja.save()
        return template("./templates/notepad.tpl", kasutajanimi=kasutajanimi, parool=hashed_parool, tekst=kasutaja.kasutaja_tekst)


@route('/notepad')
def testroute():
    return template('./templates/notepad.tpl')


@route('/loginupload', method='POST')
def login_upload():
    upload = request.files.get('upload')
    kasutajanimi = request.forms.get('kasutajanimi')
    parool = request.forms.get('parool')
    hashed_parool = hashlib.sha256(
        str(parool + salt).encode('utf-8')).hexdigest()

    try:  # kontrollin kas kasutajanimi on õige (whitespace loeb)
        kasutaja = Kasutaja.get(Kasutaja.kasutajanimi == kasutajanimi)
    except:
        return template("./templates/error.tpl", error="Sisselogimine ebaõnnestus. Antud nimega kasutajat ei eksisteeri.")

    # _ on failinimi ilma extensionita
    _, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return 'File extension not allowed.'
    upload.filename = str(datetime.datetime.now())+".jpg"
    save_path = os.getcwd()+"/uploads/"
    upload.save(save_path)  # failinimi lisatakse save_pathile automaatselt

    try:  # kontrollin EXIF rotation informatsiooni, vajadusel panen pildi õiget pidi
        image = Image.open(os.getcwd()+"/uploads/"+upload.filename)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(os.getcwd()+"/uploads/"+upload.filename)
        image.close()

    except (AttributeError, KeyError, IndexError):
        # pildil ei ole EXIF atrubuute
        pass

    try:  # laen pildid programmi
        known_image = face_recognition.load_image_file(
            os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg")
        unknown_image = face_recognition.load_image_file(
            os.getcwd()+"/uploads/"+upload.filename)
    except FileNotFoundError:
        return template("./templates/error.tpl", error="Antud kasutajat ei leidu")

    try:  # üritan piltidel nägusi tuvastata
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        markus_encoding = face_recognition.face_encodings(known_image)[0]
    except IndexError:
        return template("./templates/error.tpl", error="Sisselogimine ebaõnnestus. Pildil ei tuvastatud ühte konkreetset nägu.")

    try:  # teostan nägude võrdluse
        results = face_recognition.compare_faces(
            [markus_encoding], unknown_encoding)
        if results[0] == True:
            if kasutaja.parool == hashed_parool:
                return template("./templates/notepad.tpl", kasutajanimi=kasutajanimi, parool=hashed_parool, tekst=kasutaja.kasutaja_tekst)
            else:
                return template("./templates/error.tpl", error="Sisselogimine ebaõnnestus. Sisestatud parool on vale")
        else:
            return template("./templates/error.tpl", error="Sisselogimine ebaõnnestus. Nägu ei vasta kasutajale.")
        return str(results[0])
    except NameError:
        return "Fail"


@route('/registerupload', method='POST')
def register_upload():
    upload = request.files.get('upload')
    kasutajanimi = request.forms.get('kasutajanimi')
    parool = request.forms.get('parool')
    hashed_parool = hashlib.sha256(
        str(parool + salt).encode('utf-8')).hexdigest()

    # _ on failinimi ilma extensionita
    _, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return 'error: Ei ole pilt'

    upload.filename = kasutajanimi+".jpg"
    save_path = os.getcwd()+"/kasutajad/"

    try:
        # appends upload.filename automatically upload.file on fail
        upload.save(save_path)
    except IOError:
        return template("./templates/error.tpl", error="Registreerimine ebaõnnestus. Antud nimega kasutaja juba eksisteerib")

    try:  # kontrollin EXIF rotation informatsiooni, vajadusel panen pildi õiget pidi
        image = Image.open(os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg")
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg")
        image.close()

    except (AttributeError, KeyError, IndexError):
        # pildil ei ole EXIF atribuute
        pass

    uus_kasutaja_pilt = face_recognition.load_image_file(
        os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg")
    try:  # kontrollin kas pildil on nägu
        uus_kasutaja_pilt_encoding = face_recognition.face_encodings(uus_kasutaja_pilt)[
            0]
    except IndexError:
        # kustutan pildi, millel nägu ei tuvastatud
        os.remove(os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg")
        return template("./templates/error.tpl", error="Registreerimine ebaõnnestus. Pildil ei tuvastatud ühte konkreetset nägu.")
    uus_kasutaja = Kasutaja.create(kasutajanimi=kasutajanimi, parool=hashed_parool,
                                   kasutaja_tekst=" ")  # Salvestab kasutaja sqlite anmdebaasi
    uus_kasutaja.save()
    return template("./templates/register_success.tpl")


run(host='localhost', port=8080)
# production: run(host='localhost', server='bjoern', port=8080)