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

    while cap.isOpened():
        ret, frame = cap.read() # If frame is read, ret is true

        if not ret:
            print('Error: did not receive frame. Exiting...')
            break
        cv.imshow('window', frame)
        if cv.waitKey(1) == ord('q'):
            break
    return

def display_img(file):
    print(file)
    img = cv.imread(file)
    # Blur image for background
    img_bg = cv.blur(img, (img.shape[0]//10, img.shape[1]//10))

    # I am sorry to anyone who has to read this
    width, height = img_bg.shape[1], img_bg.shape[0]
    width = int(width * 220 // 100)
    height = int(height * 220 // 100)
    dim = width, height
    img_bg = cv.resize(img_bg, dim, interpolation = cv.INTER_AREA) # idk what im doing

    crop_width, crop_height = image_to_ratio(width, height)
    #start_crop_width = int((width - crop_width) // 2)
    #start_crop_height = int((height - crop_height) // 2)
    img_bg = img_bg[0:crop_height, 0:crop_width] # zeros should be start_crop_*

    # Resize original to fit in new
    img_width, img_height = img.shape[1], img.shape[0]

    if img_width // 9 > img_height // 16:
        img_width = int(img_width * (img_bg.shape[0] / img_height))
        img_height = img_bg.shape[0]
    elif img_height // 16 > img_width // 9:
        img_height = int(img_height * (img_bg.shape[1] / img_width))
        img_width = img_bg.shape[1]

    img = cv.resize(img, (img_width, img_height), interpolation = cv.INTER_AREA) # this not working

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
    cv.namedWindow("window", cv.WINDOW_NORMAL)
    #cv.setWindowProperty("window", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.setWindowProperty("window", cv.WND_PROP_ASPECT_RATIO, cv.WINDOW_KEEPRATIO)

    # Shuffle files in content
    random.shuffle(filenames)

    for filename in filenames:
        if filename.endswith('.MOV'):
            play_video(filename)
        else:
            cv.imshow("window", display_img(filename))
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
    print(f'af: {alpha_front.shape}\nab: {alpha_back.shape}\nfront_cropped: {front_cropped.shape}\nback_cropped: {back_cropped.shape}')
    result[y1:y2, x1:x2, :3] = alpha_front * front_cropped[:,:,:3] + (1-alpha_front) * back_cropped[:,:,:3]
    result[y1:y2, x1:x2, 3:4] = (alpha_front + alpha_back) / (1 + alpha_front*alpha_back) * 255

    return result

check_folder()
display()