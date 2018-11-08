from bottle import route, app, Request, request, run
import os



@route('/index') # or @route('/login')
def index():
    return '''
        <form action="/upload" method="post" enctype="multipart/form-data">
        Select a file: <input type="file" name="upload" />
        <input type="submit" value="Start upload" />
        </form>
    '''

@route('/upload', method='POST')
def do_upload():
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

    save_path = "/home/markus/recotest"
    upload.save(save_path) # appends upload.filename automatically
    return 'OK'


run(host='localhost', port=8080)


















