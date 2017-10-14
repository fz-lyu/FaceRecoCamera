import face_recognition
import cv2
import main
import img_file_parser
import distance

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
# obama_image = face_recognition.load_image_file("fanzhe1.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# face_encoding_list = [obama_face_encoding]
# name_list = ["fanzhe"]
temp = img_file_parser.img_parser()
name_list = temp[0]
# print(name_list)
face_encoding_list = temp[1]


# Initialize some variables

process_this_frame = True
detected = False
face_locations = []
face_encodings = []
face_names = []

while True:

    # Grab a single frame of video
    ret, frame = video_capture.read()   # Local camera
    # frame = main.get_video()          # Kinect Camera
    frame = cv2.resize(frame, (640, 480))

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        face_locations = []
        face_encodings = []
        face_names = []
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(face_encoding_list, face_encoding, tolerance=0.48)
            # al = distance.calc(face_encoding_list, face_encoding)
            # idx = al.index(min(al))
            # print(al)
            # print(idx)
            # print(match)
            name = "Unknown"
            try:
                matchingFace = match.index(True)
            except ValueError:
                matchingFace = -1
            faceLength = len(match)
            
            
            if matchingFace == -1:
                if detected:
                    largeNewName = raw_input("Input your name: ")
                    detected = False
                    if not largeNewName == "X" and not largeNewName == "x":
                        name_list.append(largeNewName)
                        face_encoding_list.append(face_encoding)
                        print(largeNewName)
                        print(face_encoding)
                        cv2.imwrite(largeNewName + ".jpg", small_frame)
                else:
                    detected = True
            else:
                name = name_list[matchingFace]
                detected = False
                
            # name = name_list[idx + 1]
            # print(name_list[idx])
            face_names.append(name)

    process_this_frame = not process_this_frame
    # print(face_names)

    # Display the results
    for (top, right, bottom, left), name1 in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # print(name1)
        # print([top, right, bottom, left])
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name1, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()