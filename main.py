from bottle import route, app, Request, request, run, template
import os
import datetime
#todo vota bottle file upload docist kood ja kasuta categoryt kasutajanimena, matchi see algpildiga nii saab multi userina teha

import face_recognition

@route('/') # or @route('/login')
def index():
    return '''
        <form action="/upload" method="post" enctype="multipart/form-data">
        Kasutajanimi: <input type="text" name="kasutajanimi" />
        Select a file: <input type="file" name="upload" />
        <input type="submit" value="Autentikeeri" />
        </form>
    '''
#@route('/templatetest', method="GET")
#def ttest():
#    return template("template.tpl")

@route('/upload', method='POST')
def do_upload():
    upload     = request.files.get('upload')
    kasutajanimi = request.forms.get('kasutajanimi')
    name, ext = os.path.splitext(upload.filename) #_ on failinimi ilma extensionita
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'
    upload.filename = str(datetime.datetime.now())
    save_path = "/home/markus/recotest/uploadid/"
    upload.save(save_path) # appends upload.filename automatically upload.file on fail
    try:
        known_image = face_recognition.load_image_file("/home/markus/recotest/kasutajad/"+kasutajanimi.lower()+".jpg")
        unknown_image = face_recognition.load_image_file("/home/markus/recotest/uploadid/"+upload.filename)
    except FileNotFoundError:
        return "Antud kasutajat ei leidu"
    try:
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        markus_encoding = face_recognition.face_encodings(known_image)[0]
    except IndexError:
        return "Nagu ei tuvastatud"

    try:
        results = face_recognition.compare_faces([markus_encoding], unknown_encoding)
        return str(results[0])
    except NameError:
        return "Fail"

    #return 'OK'


run(host='localhost', port=8080)


















