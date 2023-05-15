import face_recognition
import os
import numpy as np
import shutil
import base64
import cv2


def recognize(base64data):
    face_to_recognize_ = 'unknown.png'
    base64tofile(base64data)

    known_face_encodings = []
    known_face_names = []

    for path in os.listdir('images'):
        if os.path.isfile(os.path.join('images', path)):
            known_image = face_recognition.load_image_file("images/{}".format(path))
            known_face_encodings.append(face_recognition.face_encodings(known_image)[0])
            known_face_names.append(' '.join(path.split('.')[0:-1]).upper())

    frame = cv2.imread(face_to_recognize_)
    frame = cv2.flip(frame, 1)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []

    # naming all face in a frame
    for idx, face_encoding in enumerate(face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        if len(matches) < 1:
            continue

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        name = known_face_names[best_match_index]
        face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Input text label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # Display the resulting image

    return face_names, mattobase64data(frame)


def registrate(id_, base64data):
    base64tofile(base64data)
    shutil.copy('unknown.png', 'images/{}.png'.format(id_))


def base64tofile(base64data):
    decoded_data = base64.b64decode((base64data))

    with open('unknown.png', 'wb') as f:
        f.write(decoded_data)


def mattobase64data(cv_mat):
    cv_mat = cv2.flip(cv_mat, 1)
    _, im_arr = cv2.imencode('.png', cv_mat)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    return base64.b64encode(im_bytes).decode()
