
from PIL import Image, ExifTags
from bottle import route, app, Request, request, run, template
import os
import datetime

import face_recognition

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
    return template("./templates/error.tpl", error="testiarror")



@route('/loginupload', method='POST')
def login_upload():
    upload     = request.files.get('upload')
    kasutajanimi = request.forms.get('kasutajanimi')
    _, ext = os.path.splitext(upload.filename) #_ on failinimi ilma extensionita
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'
    upload.filename = str(datetime.datetime.now())+".jpg"
    save_path = os.getcwd()+"/uploadid/"
    upload.save(save_path) # failinimi lisatakse save_pathile automaatselt
    
    try: #kontrollin EXIF rotation informatsiooni, vajadusel panen pildi õiget pidi
        image=Image.open(os.getcwd()+"/uploadid/"+upload.filename)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(image._getexif().items())

        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)
        image.save(os.getcwd()+"/uploadid/"+upload.filename)
        image.close()

    except (AttributeError, KeyError, IndexError):
        # pildil ei ole EXIF atrubuute
        pass

    try:  #laen pildid programmi
        known_image = face_recognition.load_image_file(os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg")
        unknown_image = face_recognition.load_image_file(os.getcwd()+"/uploadid/"+upload.filename)
    except FileNotFoundError:
        return template("./templates/error.tpl", error="Antud kasutajat ei leidu")
    
    try: #üritan piltidel nägusi tuvastata
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        markus_encoding = face_recognition.face_encodings(known_image)[0]
    except IndexError:
        return template("./templates/error.tpl", error="Sisselogimine ebaõnnestus. Pildil ei tuvastatud nägu")

    try: #teostan nägude võrdluse
        results = face_recognition.compare_faces([markus_encoding], unknown_encoding)
        if results[0] == True:
            return template("./templates/login_success.tpl", pealkiri='Sisselogimine õnnestus', sonum='todo:väljasta auth token')
        else:
            return template("./templates/error.tpl", error="Sisselogimine ebaõnnestus. Nägu ei vasta kasutajale.")
        return str(results[0])
    except NameError:
        return "Fail"

@route('/registerupload', method='POST')
def register_upload():
    upload     = request.files.get('upload')
    kasutajanimi = request.forms.get('kasutajanimi')

    _, ext = os.path.splitext(upload.filename) #_ on failinimi ilma extensionita
    if ext not in ('.png','.jpg','.jpeg'):
        return 'error: Ei ole pilt'
    
    upload.filename = kasutajanimi+".jpg"
    save_path = os.getcwd()+"/kasutajad/"
    
    try:
        upload.save(save_path) # appends upload.filename automatically upload.file on fail
    except IOError:
        return template("./templates/error.tpl", error="Registreerimine ebaõnnestus. Antud nimega kasutaja juba eksisteerib")

    try:    #kontrollin EXIF rotation informatsiooni, vajadusel panen pildi õiget pidi
        image=Image.open(os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg")
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(image._getexif().items())

        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)
        image.save(os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg")
        image.close()

    except (AttributeError, KeyError, IndexError):
        # pildil ei ole EXIF atribuute
        pass
    
    uus_kasutaja_pilt = face_recognition.load_image_file(os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg")
    try: #kontrollin kas pildil on nägu
        uus_kasutaja_pilt_encoding = face_recognition.face_encodings(uus_kasutaja_pilt)[0]
    except IndexError:
        os.remove(os.getcwd()+"/kasutajad/"+kasutajanimi+".jpg") #kustutan pildi, millel nägu ei tuvastatud
        return template("./templates/error.tpl", error="Registreerimine ebaõnnestus. Pildil ei tuvastatud nägu")
    return template("./templates/register_success.tpl")
    
run(host='localhost', port=8080)
# production: run(host='localhost', server='bjoern', port=8080)


















