import os
import cv2
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

def display():
    path = "content"
    filenames = glob.glob(os.path.join(path, "*"))
    print(filenames)

    for filename in filenames:
        print(filename)
        img = cv2.imread(filename)

        cv2.imshow("Slideshow", img)

        if cv2.waitKey(5000) == ord('q'):
            return

check_folder()
display()