import cv2
import time
import os


# Time (seconds) to wait to extract the frames
TIME_WINDOW = 1

# Craetes a directory to store frames, relative to the script path. 
cwd = os.path.dirname(os.path.realpath(__file__))
image_directory = cwd + '/image-directory'
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

# Initialize the video
cam = cv2.VideoCapture(0)

# Extracting process
start_time = time.process_time()
while True:
    ret, image = cam.read()
    cv2.imshow('Imagetest', image)
    k = cv2.waitKey(1)
    if k != -1:
        break

    time_difference = time.process_time() - start_time
    if time_difference > TIME_WINDOW:
        start_time = time.process_time()
        cv2.imwrite(image_directory + '/image-to-process.jpg', image)

cam.release()
cv2.destroyAllWindows()
