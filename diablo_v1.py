import os
import cv2 as cv
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
                blur_frame = cv.blur(frame, (frame.shape[0]//10, frame.shape[1]//10))
                width, height = blur_frame.shape[1], blur_frame.shape[0]
                width = int(width * 220 // 100)
                height = int(height * 220 // 100)
                dim = width, height
                blur_frame = cv.resize(blur_frame, dim, interpolation = cv.INTER_AREA)
                crop_width, crop_height = image_to_ratio(width, height)
                blur_frame = blur_frame[0:crop_height, 0:crop_width]
                bg_made = True

            if ret:
                # Calculating True FPS
                new_frame_time = time.time()
                fps = 1 / (new_frame_time - prev_frame_time)
                prev_frame_time = new_frame_time

                # Resize original to fit in new
                dst = frame # if its not made by the if statement
                frame_width, frame_height = frame.shape[1], frame.shape[0]
                if frame_height // 9 != frame_width // 16:
                    if frame_width // 9 >= (frame_height // 16) - 10:
                        frame_width = int(frame_width * (blur_frame.shape[0] / frame_height))
                        frame_height = blur_frame.shape[0]
                    elif frame_height // 16 >= frame_width // 9:
                        frame_height = int(frame_height * (blur_frame.shape[1] / frame_width))
                        frame_width = blur_frame.shape[1]
                    frame = cv.resize(frame, (frame_width, frame_height), interpolation = cv.INTER_AREA)

                    # Display original image on top
                    dst = merge_image(blur_frame, frame, ((crop_width // 2) - (frame.shape[1] // 2)), ((crop_height // 2) - (frame.shape[0] // 2)))
                
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

    # Set size of bg to 16x9
    width, height = img_bg.shape[1], img_bg.shape[0]
    width = int(width * 220 // 100)
    height = int(height * 220 // 100)
    dim = width, height
    img_bg = cv.resize(img_bg, dim, interpolation = cv.INTER_AREA)
    crop_width, crop_height = image_to_ratio(width, height)
    img_bg = img_bg[0:crop_height, 0:crop_width]

    # Resize original to fit in bg
    img_width, img_height = img.shape[1], img.shape[0]
    if img_width // 9 >= img_height // 16:
        img_width = int(img_width * (img_bg.shape[0] / img_height))
        img_height = img_bg.shape[0]
    elif img_height // 16 >= img_width // 9:
        img_height = int(img_height * (img_bg.shape[1] / img_width))
        img_width = img_bg.shape[1]
    img = cv.resize(img, (img_width, img_height), interpolation = cv.INTER_AREA)

    # Display original image on top
    dst = merge_image(img_bg, img, ((crop_width // 2) - (img.shape[1] // 2)), ((crop_height // 2) - (img.shape[0] // 2)))

    return dst

def display_primary():
    print('placeholder')
    return

def display():
    # Open content folder
    path = "content"
    filenames = glob.glob(os.path.join(path, "*"))
    print(filenames)

    # Create window, set to fullscreen, and keep aspect ration of image.
    cv.namedWindow("photo_frame", cv.WINDOW_NORMAL)
    #cv.setWindowProperty("photo_frame", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.setWindowProperty("photo_frame", cv.WND_PROP_ASPECT_RATIO, cv.WINDOW_KEEPRATIO)

    # Shuffle files in content
    random.shuffle(filenames)

    for filename in filenames:

        # Transition
        

        if filename.endswith('.MOV') or filename.endswith('.mp4') or filename.endswith('.mov'):
            play_video(filename)
        else:
            cv.imshow("photo_frame", display_img(filename))
            if cv.waitKey(2000) == ord('q'):# TIME FOR IMAGE *************************
                return

def image_to_ratio(w, h):
    if (w / h) < (16 / 9):
        w = (w // 16) * 16
        h = (w // 16) * 9
    else: 
        h = (h // 9) * 9
        w = (h // 9) * 16
    return w, h

def merge_image(back, front, x,y):
    # convert to rgba
    if back.shape[2] == 3:
        back = cv.cvtColor(back, cv.COLOR_BGR2BGRA)
    if front.shape[2] == 3:
        front = cv.cvtColor(front, cv.COLOR_BGR2BGRA)

    # crop the overlay from both images
    bh,bw = back.shape[:2]
    fh,fw = front.shape[:2]
    x1, x2 = max(x, 0), min(x+fw, bw)
    y1, y2 = max(y, 0), min(y+fh, bh)
    front_cropped = front[y1-y:y2-y, x1-x:x2-x]
    back_cropped = back[y1:y2, x1:x2]

    alpha_front = front_cropped[:,:,3:4] / 255
    alpha_back = back_cropped[:,:,3:4] / 255
    
    # replace an area in result with overlay
    result = back.copy()
    result[y1:y2, x1:x2, :3] = alpha_front * front_cropped[:,:,:3] + (1-alpha_front) * back_cropped[:,:,:3]
    result[y1:y2, x1:x2, 3:4] = (alpha_front + alpha_back) / (1 + alpha_front*alpha_back) * 255

    return result

check_folder()
display()
cv.destroyAllWindows()