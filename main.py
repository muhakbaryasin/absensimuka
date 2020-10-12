import face_recognition
import cv2
import numpy as np
import os
import glob
from multiprocessing import Process
import uuid
from tkinter import *
import os

e = None
faces_names = []
faces_encodings = []
cur_direc = os.getcwd()

def callback():
    print (e.get()) # This is the text you may want to use later


def show_textinput():
    master = Tk()
    e = Entry(master)
    e.pack()
    e.focus_set()
    b = Button(master, text = "OK", width = 10, command = callback)
    b.pack()
    mainloop()


def threaD(image_file):
    image = face_recognition.load_image_file(image_file)
    tmp_f_encodings = face_recognition.face_encodings(image)
    
    if (len(tmp_f_encodings) < 1):
        print("No face detected")
        os.remove(image_file)
        return
    
    image_encoding = tmp_f_encodings[0]
    faces_encodings.append(image_encoding)# Create array of known names
    faces_names.append(image_file)


if __name__ == '__main__':
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]    
        
        if process_this_frame:
            face_locations = face_recognition.face_locations( rgb_small_frame)
            face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
            face_names = []
            
            # naming all face in a frame
            for idx, face_encoding in enumerate(face_encodings):
                matches = face_recognition.compare_faces(faces_encodings, face_encoding)
                
                if (len(matches) < 1):
                    top, right, bottom, left = face_locations[idx]
                    
                    if top - 10 >= 0:
                        top = top - 10
                    
                    if bottom + 10 >= rgb_small_frame.shape[0]:
                        bottom = bottom + 10
                    
                    if left - 10 >=0:
                        left = left - 10
                    
                    if right + 10 >= rgb_small_frame.shape[1]:
                        right = right + 10

                    uuid_name = str(uuid.uuid4()) + ".bmp"
                    cv2.imwrite(uuid_name, rgb_small_frame[top:bottom, left:right])
                    face_names.append("unknown")
                    threaD(uuid_name)
                    #p = Process(target=threaD, args=(uuid_name,))
                    #p.start()
                
                if ( len(faces_encodings) < 1 ):
                    continue

                matches = face_recognition.compare_faces(faces_encodings, face_encoding)
                
                face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                name = faces_names[best_match_index]
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
        
        cv2.imshow('Video', frame)
        
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
            
