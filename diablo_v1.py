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

def display():
    path = "content"
    filenames = glob.glob(os.path.join(path, "*"))
    print(filenames)

    cv.namedWindow("window", cv.WINDOW_NORMAL)
    #cv.setWindowProperty("window", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.setWindowProperty("window", cv.WND_PROP_ASPECT_RATIO, cv.WINDOW_KEEPRATIO)

    random.shuffle(filenames)
    for filename in filenames:
        print(filename)
        img = cv.imread(filename)

        cv.imshow("window", img)

        if cv.waitKey(1000) == ord('q'):
            return

check_folder()
display()