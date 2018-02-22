#!/usr/bin/env python3

# create a folder to store extracted images
import os
folder = 'Input'  
os.mkdir(folder)
# use opencv to do the job
import cv2
print(cv2.__version__)  # my version is 3.1.0
vidcap = cv2.VideoCapture('4tel_train_video.MP4')
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
print('length: {}' .format(length))
count = 0
while True: #count < 100:
    success,image = vidcap.read()
    if not success:
    	break

    if count%15 == 0:
    	cv2.imwrite(os.path.join(folder,"frame{:d}.jpg".format(count)), image)     # save frame as JPEG file
    count += 1
    print(count)

print("{} images are extacted in {}.".format(count/15,folder))