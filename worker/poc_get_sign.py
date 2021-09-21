import cv2 
import numpy as np
import os
import cv2
import imutils
import my_classification as train
from PIL import Image

def identity_red(imag):
    orig = imag.copy()
    imag_red = imag.copy()

    label_list = list()
    cnts_list = list()
    mser_red = cv2.MSER_create(8, 200, 3000)

    img = imag.copy()

    img2 = imag.copy()[:500, :]  # red signs are only on the above few rows
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    # equalize the histogram of the Y channel
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])

    # convert the YUV image back to RGB format
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    # mask to extract red
    img_hsv = cv2.cvtColor(imag, cv2.COLOR_BGR2HSV)
    lower_red_1 = np.array([0, 70, 60])
    upper_red_1 = np.array([10, 255, 255])
    mask_1 = cv2.inRange(img_hsv, lower_red_1, upper_red_1)
    lower_red_2 = np.array([170, 70, 60])
    upper_red_2 = np.array([180, 255, 255])
    mask_2 = cv2.inRange(img_hsv, lower_red_2, upper_red_2)
    mask = cv2.bitwise_or(mask_1, mask_2)
    red_mask_ = cv2.bitwise_and(img_output, img_output, mask=mask)
    red_mask = red_mask_[:500, :]

    # separating channels
    r_channel = red_mask[:, :, 2]
    g_channel = red_mask[:, :, 1]
    b_channel = red_mask[:, :, 0]

    # filtering
    filtered_r = cv2.medianBlur(r_channel, 5)
    filtered_g = cv2.medianBlur(g_channel, 5)
    filtered_b = cv2.medianBlur(b_channel, 5)

    filtered_r = 4 * filtered_r - 0.5 * filtered_b - 2 * filtered_g

    # MSER detection
    regions, _ = mser_red.detectRegions(np.uint8(filtered_r))

    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

    blank = np.zeros_like(red_mask)
    cv2.fillPoly(np.uint8(blank), hulls, (0, 0, 255))  # fill a blank image with the detected hulls
    # cv2.imshow("mser_red", blank)
    # perform some operations on the detected hulls from MSER
    kernel_1 = np.ones((3, 3), np.uint8)
    kernel_2 = np.ones((5, 5), np.uint8)

    erosion = cv2.erode(blank, kernel_1, iterations=1)
    dilation = cv2.dilate(erosion, kernel_2, iterations=1)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel_2)

    _, r_thresh = cv2.threshold(opening[:, :, 2], 20, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(r_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    max_cnts = 3  # no frame we want to detect more than 3
    if not cnts == []:
        # print("HERE")
        cnts_sorted = sorted(cnts, key=cv2.contourArea, reverse=True)
        if len(cnts_sorted) > max_cnts:
            cnts_sorted = cnts_sorted[:3]

        for c in cnts_sorted:
            # print("HERE")
            x, y, w, h = cv2.boundingRect(c)
            # if x < 800:
            #     continue
            # aspect_ratio_1 = w / h
            # aspect_ratio_2 = h / w
            # if aspect_ratio_1 <= 0.3 or aspect_ratio_1 > 1.2:
            #     continue
            # if aspect_ratio_2 <= 0.3:
            #     continue
            print("HERE")
            hull = cv2.convexHull(c)
            # cv2.drawContours(imag, [hull], -1, (0, 255, 0), 1)

            mask = np.zeros_like(imag)
            # cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)  # Draw filled contour in mask
            cv2.rectangle(mask, (x, y), (int(x + w), int(y + h)), (255, 255, 255), -1)

            out = np.zeros_like(imag)  # Extract out the object and place into output image
            out[mask == 255] = imag[mask == 255]

            x_pixel, y_pixel, _ = np.where(mask == 255)
            (topx, topy) = (np.min(x_pixel), np.min(y_pixel))
            (botx, boty) = (np.max(x_pixel), np.max(y_pixel))
            if np.abs(topx - botx) <= 25 or np.abs(topy - boty) <= 25:
                continue

            out = imag[topx:botx + 1, topy:boty + 1]
            out_resize = cv2.resize(out, (64, 64), interpolation=cv2.INTER_CUBIC)

            # PREDICTION
            predict, prob = train.test_red(clf_red, out_resize)
            print(np.max(prob))
            print(predict)
            if np.max(prob) < 0.78:
                continue
            cv2.rectangle(imag, (x, y), (int(x + w), int(y + h)), (0, 255, 0), 2)
            label = predict[0]
            if label == 100:
                continue
            
            cnts_list.append(c)
            label_list.append(label)

            return out_resize

def identify_yellow(imag, clf_yellow):
    label_list = list()
    cnts_list = list()
    mser_yellow = cv2.MSER_create(8, 400, 4000)

    img = imag.copy()
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    # equalize the histogram of the Y channel
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])

    # convert the YUV image back to RGB format
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    # convert the image to HSV format for color segmentation
    img_hsv = cv2.cvtColor(imag, cv2.COLOR_BGR2HSV)

    # mask to extract yellow
    lower_yellow = np.array([60, 40, 100])
    upper_yellow = np.array([56, 100, 100])
    mask = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    yellow_mask = cv2.bitwise_and(img_output, img_output, mask=mask)

    # seperate out the channels
    r_channel = yellow_mask[:, :, 2]
    g_channel = yellow_mask[:, :, 1]
    b_channel = yellow_mask[:, :, 0]

    # filter out
    filtered_r = cv2.medianBlur(r_channel, 5)
    filtered_g = cv2.medianBlur(g_channel, 5)
    filtered_b = cv2.medianBlur(b_channel, 5)

    # create a yellow gray space TODO YELLOW MASK
    filtered_y = -0.5 * filtered_r + 3 * filtered_b - 2 * filtered_g

    # Do MSER
    regions, _ = mser_yellow.detectRegions(np.uint8(filtered_b))

    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

    blank = np.zeros_like(yellow_mask)
    cv2.fillPoly(np.uint8(blank), hulls, (255, 0, 0))

    # cv2.imshow("mser_yellow", blank)
    kernel_1 = np.ones((3, 3), np.uint8)
    kernel_2 = np.ones((5, 5), np.uint8)

    erosion = cv2.erode(blank, kernel_1, iterations=1)
    dilation = cv2.dilate(erosion, kernel_2, iterations=1)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel_2)

    _, b_thresh = cv2.threshold(opening[:, :, 0], 60, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(b_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    max_cnts = 3  # no frame we want to detect more than 3

    if not cnts == []:
        cnts_sorted = sorted(cnts, key=cv2.contourArea, reverse=True)
        if len(cnts_sorted) > max_cnts:
            cnts_sorted = cnts_sorted[:3]

        for c in cnts_sorted:
            x, y, w, h = cv2.boundingRect(c)
            if x < 100:
                continue
            if h < 20:
                continue

            if y > 400:
                continue

            aspect_ratio_1 = w / h
            aspect_ratio_2 = h / w
            if aspect_ratio_1 <= 0.5 or aspect_ratio_1 > 1.2:
                continue
            if aspect_ratio_2 <= 0.5:
                continue

            hull = cv2.convexHull(c)

            # cv2.rectangle(imag, (x, y), (int(x+w), int(y+h)), (0, 255, 0), 2)
            # cv2.drawContours(imag, [hull], -1, (0, 255, 0), 2)

            mask = np.zeros_like(imag)
            # cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)  # Draw filled contour in mask
            cv2.rectangle(mask, (x, y), (int(x + w), int(y + h)), (255, 255, 255), -1)
            out = np.zeros_like(imag)  # Extract out the object and place into output image
            out[mask == 255] = imag[mask == 255]

            x_pixel, y_pixel, _ = np.where(mask == 255)
            (topx, topy) = (np.min(x_pixel), np.min(y_pixel))
            (botx, boty) = (np.max(x_pixel), np.max(y_pixel))
            if np.abs(topx - botx) <= 25 or np.abs(topy - boty) <= 25:
                continue

            out = imag[topx:botx + 1, topy:boty + 1]
            out_resize = cv2.resize(out, (64, 64), interpolation=cv2.INTER_CUBIC)
            predict, prob = train.test_yellow(clf_yellow, out_resize)
            print(np.max(prob))
            if np.max(prob) < 0.78:
                continue
            cv2.rectangle(imag, (x, y), (int(x + w), int(y + h)), (0, 255, 0), 2)
            label = predict[0]
            if label == 100:
                continue
            
            cnts_list.append(c)
            label_list.append(label)
        return cnts_list, label_list
    else:
        return None, None

clf_red = train.train_red()
# clf_blue = train.train_yellow() 

# imag = np.uint8(cv2.imread('./dataset/images/road97.png'))
imag = np.uint8(cv2.imread('fernandotest.jpeg'))
result = identity_red(imag)
cv2.imshow("image", result)
cv2.waitKey(0)

# activate venv
# .\venv\Scripts\activate

# deactivate venv
# deactivate