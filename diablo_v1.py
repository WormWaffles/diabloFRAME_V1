import os
import cv2 as cv
import numpy as np
import glob
import random
import time

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
    initial_time = time.time()
    to_time = time.time()

    set_fps = 30 # Set frame rate

    # Variables Used to Calculate FPS
    prev_frame_time = 0
    new_frame_time = 0

    # Background var
    bg_made = False

    while cap.isOpened():
        while_running = time.time() # Keep updating time with each frame
        new_time = while_running - initial_time # If time taken is 1/fps, then read a frame

        if new_time >= 1 / set_fps:
            ret, frame = cap.read()

            # make bg image
            if not bg_made:
                blur_frame = cv.blur(frame, (frame.shape[0]//15, frame.shape[1]//15))
                blur_frame = cv.resize(blur_frame, (1920, 1080), interpolation = cv.INTER_AREA)
                bg_made = True

            if ret:
                # Calculating True FPS
                new_frame_time = time.time()
                fps = 1 / (new_frame_time - prev_frame_time)
                prev_frame_time = new_frame_time

                # Resize original to fit in new
                crop_width, crop_height = 1920, 1080
                frame_width, frame_height = frame.shape[1], frame.shape[0]
                if frame_height // 9 != frame_width // 16:
                    frame = cv.resize(frame, (int((frame_width / frame_height) * 1080), 1080), interpolation = cv.INTER_AREA)
                    del_width = frame.shape[1]
                    blur_frame_left = blur_frame[0:1080, 0:((1920 - del_width) // 2)]
                    blur_frame_right = blur_frame[0:1080, (((1920 - del_width) // 2) + del_width):1920]
                    dst = np.concatenate((blur_frame_left, frame), axis=1)
                    dst = np.concatenate((dst, blur_frame_right), axis=1)
                else:
                    dst = cv.resize(frame, (1920, 1080), interpolation = cv.INTER_AREA)

                cv.imshow('photo_frame', dst)
                initial_time = while_running # Update the initial time with current time

            else:
                total_time_of_video = while_running - to_time # To get the total time of the video
                print(total_time_of_video)
                break

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

def display_img(file):
    print(file)
    img = cv.imread(file)

    # Blur image for background
    img_bg = cv.blur(img, (img.shape[0]//10, img.shape[1]//10))

    # Set size of bg to 1080p
    crop_width, crop_height = 1920, 1080 # make every image 1080p
    img_bg = cv.resize(img_bg, (1920, 1080))

    # Resize original to fit in bg
    img_width, img_height = img.shape[1], img.shape[0]
    img = cv.resize(img, (int((img_width / img_height) * 1080), 1080), interpolation = cv.INTER_AREA)

    # Display original image on top
    del_width = img.shape[1]
    blur_frame_left = img_bg[0:1080, 0:((1920 - del_width) // 2)]
    blur_frame_right = img_bg[0:1080, (((1920 - del_width) // 2) + del_width):1920]
    dst = np.concatenate((blur_frame_left, img), axis=1)
    dst = np.concatenate((dst, blur_frame_right), axis=1)
    #dst = merge_image(img_bg, img, ((crop_width // 2) - (img.shape[1] // 2)), ((crop_height // 2) - (img.shape[0] // 2)))

    print(dst.shape[0], dst.shape[1])

    return dst

def display():
    # Open content folder
    path = "content"
    filenames = glob.glob(os.path.join(path, "*"))
    print(filenames)

    # Create window, set to fullscreen, and keep aspect ration of image.
    cv.namedWindow("photo_frame", cv.WINDOW_NORMAL)
    #cv.setWindowProperty("photo_frame", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN) # ** UNCOMMENT FOR FULLSCREEN **
    cv.setWindowProperty("photo_frame", cv.WND_PROP_ASPECT_RATIO, cv.WINDOW_KEEPRATIO)

    # Shuffle files in content
    random.shuffle(filenames)
    for filename in filenames:
        if filename.endswith('.MOV') or filename.endswith('.mp4') or filename.endswith('.mov'):
            play_video(filename)
        else:
            cv.imshow("photo_frame", display_img(filename))
            if cv.waitKey(2000) == ord('q'):# TIME FOR IMAGE *************************
                return

check_folder()
display()
cv.destroyAllWindows()