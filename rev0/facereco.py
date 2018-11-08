import face_recognition
known_image = face_recognition.load_image_file("1.jpg")
unknown_image = face_recognition.load_image_file("2.jpg")

markus_encoding = face_recognition.face_encodings(known_image)[0]
try:
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    markus_encoding = face_recognition.face_encodings(known_image)[0]
except IndexError:
    print("Nagu ei tuvastatud")

try:
    results = face_recognition.compare_faces([markus_encoding], unknown_encoding)
    print(results)
except NameError:
    print("Fail")