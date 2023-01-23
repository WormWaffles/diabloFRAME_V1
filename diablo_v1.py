import os
import cv2 as cv
import glob
import random

def check_folder():
    print('Looking for folder...')
    if os.path.exists("content"):
        print('Folder found.')
    else:
        print('Folder not found, creating...')
        os.mkdir("content")
        print('Done.')

def play_video(file):
    cap = cv.VideoCapture(file)

    while cap.isOpened():
        ret, frame = cap.read() # If frame is read, ret is true

        if not ret:
            print('Error: did not receive frame. Exiting...')
            break
        cv.imshow('window', frame)
        if cv.waitKey(1) == ord('q'):
            break
    return None

def display_img(file):
    print(file)
    img = cv.imread(file)

    return img

def display():
    # Open content folder
    path = "content"
    filenames = glob.glob(os.path.join(path, "*"))
    print(filenames)

    # Create window, set to fullscreen, and keep aspect ration of image.
    cv.namedWindow("window", cv.WINDOW_NORMAL)
    #cv.setWindowProperty("window", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.setWindowProperty("window", cv.WND_PROP_ASPECT_RATIO, cv.WINDOW_KEEPRATIO)

    # Shuffle files in content
    random.shuffle(filenames)
    for filename in filenames:
        if filename.endswith('.MOV'):
            play_video(filename)
        
        cv.imshow("window", display_img(filename))

        if cv.waitKey(1000) == ord('q'):# TIME FOR IMAGE *************************
            return

check_folder()
display()