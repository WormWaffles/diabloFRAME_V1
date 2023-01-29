import os
import cv2 as cv
import numpy as np
import glob
import random
import time

# editable vlues
delay = 5000 # image hold time in miliseconds
home_vid = False # home vids play on the hour

def check_folder():
    print('Looking for CONTENT folder...')
    if os.path.exists("content"):
        print('Folder found.')
    else:
        print('Folder not found, creating...')
        os.mkdir("content")
        print('Done.')
    print('Looking for HOME_VID folder...')
    if home_vid:
        if os.path.exists("home_vid"):
            print('Folder found.')
        else:
            print('Folder not found, creating...')
            os.mkdir("home_vid")
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
    # read file
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

    # if picture is really long...

    # Display original image on top
    del_width = img.shape[1]
    blur_frame_left = img_bg[0:1080, 0:((1920 - del_width) // 2)]
    blur_frame_right = img_bg[0:1080, (((1920 - del_width) // 2) + del_width):1920]
    dst = np.concatenate((blur_frame_left, img), axis=1)
    dst = np.concatenate((dst, blur_frame_right), axis=1)

    return dst

def transition(img1, img2):
    # Transition
    for i in np.linspace(0,1,100):
        alpha = i
        beta = 1 - alpha
        output = cv.addWeighted(img1, alpha, img2, beta, 0)
        cv.imshow('photo_frame', output)
        time.sleep(0.01)
        if cv.waitKey(1) == 27:
            break

def kin_burn(img):
    # take image and use delay to crop it every so often.

    #math math math
    print('placeholder')

def display():
    # Open content folder
    path = "content"
    filenames = glob.glob(os.path.join(path, "*"))

    # Create window, set to fullscreen, and keep aspect ration of image.
    cv.namedWindow("photo_frame", cv.WINDOW_NORMAL)
    #cv.setWindowProperty("photo_frame", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN) # ** UNCOMMENT FOR FULLSCREEN **
    cv.setWindowProperty("photo_frame", cv.WND_PROP_ASPECT_RATIO, cv.WINDOW_KEEPRATIO)
    
    # vaid extentions
    img_ext = {'.jpeg', '.JPG', '.jpg', '.png'}
    vid_ext = {'mov', '.mp4', '.MOV'}

    random.shuffle(filenames)
    print(filenames)
    for i in range(len(filenames)):
        if i < len(filenames) - 1:
            if filenames[i].endswith(tuple(img_ext)) and filenames[i + 1].endswith(tuple(img_ext)):
                cv.imshow('photo_frame', display_img(filenames[i]))
                temp_img = display_img(filenames[i + 1])
                # wait on image
                if cv.waitKey(delay) == ord('q'):
                    return
                # transition
                transition(temp_img, display_img(filenames[i]))
            elif filenames[i].endswith(tuple(vid_ext)) and filenames[i + 1].endswith(tuple(vid_ext)):
                play_video(filenames[i + 1])
            elif filenames[i].endswith(tuple(img_ext)) and filenames[i + 1].endswith(tuple(vid_ext)):
                cv.imshow('photo_frame', display_img(filenames[i]))
                # wait for image
                if cv.waitKey(delay) == ord('q'):
                    return
                play_video(filenames[i + 1])
            else:
                cv.imshow('photo_frame', display_img(filenames[i + 1]))

check_folder()
display()
cv.destroyAllWindows()

# p -> ken_burns -> if next = image (transition) else: play video