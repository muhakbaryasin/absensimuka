import face_recognition
import os
import numpy as np
import shutil


def recognize(face_to_recognize_):
    result_ = None
    known_face_encodings = []
    known_face_names = []

    for path in os.listdir('images'):
        if os.path.isfile(os.path.join('images', path)):
            known_image = face_recognition.load_image_file("images/{}".format(path))
            known_face_encodings.append(face_recognition.face_encodings(known_image)[0])
            known_face_names.append(' '.join(path.split('.')[0:-1]).upper())

    unknown_image = face_recognition.load_image_file(face_to_recognize_)
    unknown_encoding = face_recognition.face_encodings(unknown_image)

    for face_encoding in unknown_encoding:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            if result_ is None:
                result_ = []

            name = known_face_names[best_match_index]
            result_.append(name)

    return result_


def register(face_to_recognize_):
    extension = face_to_recognize_.split('.')[-1]
    name = input("name: ")
    shutil.copy(face_to_recognize_, 'images/{}.{}'.format(name, extension))


if __name__ == '__main__':
    face_to_recognize = "unknown.jpeg"
    result = recognize(face_to_recognize)

    if result is None:
        register(face_to_recognize)

    print(result)
