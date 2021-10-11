import cv2 
import numpy as np
import os
import my_classification as train
import imutils
from PIL import Image
from joblib import load

def identify(imag):
    clf_yellow = load('yellow_training.joblib') 

    label_list = list()
    cnts_list = list()
    mser_yellow = cv2.MSER_create(8, 200, 3000)

    img = imag.copy()
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    # cv2.imshow("img_yuv", img_yuv)
    # cv2.waitKey(0)

    # equalize the histogram of the Y channel
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])

    # convert the YUV image back to RGB format
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    # cv2.imshow("img_output", img_output)
    # cv2.waitKey(0)

    # convert the image to HSV format for color segmentation
    img_hsv = cv2.cvtColor(imag, cv2.COLOR_BGR2HSV)
    # cv2.imshow("img_hsv", img_hsv)
    # cv2.waitKey(0)

    # mask to extract yellow
    # lower_yellow = np.array([80, 100, 100])
    # upper_yellow = np.array([100, 255, 255])
    # lower_yellow = np.array([22, 93, 0])
    # upper_yellow = np.array([45, 255, 255])
    lower_yellow = np.array([22, 93, 0])
    upper_yellow = np.array([106, 255, 255])

    mask = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    yellow_mask = cv2.bitwise_and(img_output, img_output, mask=mask)
    yellow_mask = yellow_mask[:800, :]

    # seperate out the channels
    r_channel = yellow_mask[:, :, 2]
    g_channel = yellow_mask[:, :, 1]
    b_channel = yellow_mask[:, :, 0]

    # filter out
    filtered_r = cv2.medianBlur(r_channel, 5)
    filtered_g = cv2.medianBlur(g_channel, 5)
    filtered_b = cv2.medianBlur(b_channel, 5)

    # create a yellow gray space TODO YELLOW MASK, estos coeficientes no estan del todo bien
    filtered_y = 3 * filtered_r - 2 * filtered_b + 1 * filtered_g

    # Do MSER
    regions, _ = mser_yellow.detectRegions(np.uint8(filtered_y))

    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

    blank = np.zeros_like(yellow_mask)
    cv2.fillPoly(np.uint8(blank), hulls, (0, 255, 255))


    # cv2.imshow("mser_yellow", blank)
    # cv2.waitKey(0)

    kernel_1 = np.ones((3, 3), np.uint8)
    kernel_2 = np.ones((5, 5), np.uint8)

    erosion = cv2.erode(blank, kernel_1, iterations=1)
    dilation = cv2.dilate(erosion, kernel_2, iterations=1)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel_2)

    # cv2.imshow("mser_yellow", opening[:, :, 2])
    # cv2.waitKey(0)

    _, y_thresh = cv2.threshold(opening[:, :, 2], 0, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(y_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    max_cnts = 3  # no frame we want to detect more than 3
    print("HERE YELLOW")

    if not cnts == []:
        print("HERE YELLOW")
        cnts_sorted = sorted(cnts, key=cv2.contourArea, reverse=True)
        if len(cnts_sorted) > max_cnts:
            cnts_sorted = cnts_sorted[:3]

        for c in cnts_sorted:
            x, y, w, h = cv2.boundingRect(c)
            # if x < 100:
            #     continue
            # if h < 20:
            #     continue

            # if y > 400:
            #     continue

            # aspect_ratio_1 = w / h
            # aspect_ratio_2 = h / w
            # if aspect_ratio_1 <= 0.5 or aspect_ratio_1 > 1.2:
            #     continue
            # if aspect_ratio_2 <= 0.5:
            #     continue

            hull = cv2.convexHull(c)

            cv2.rectangle(imag, (x, y), (int(x+w), int(y+h)), (0, 255, 0), 2)
            cv2.drawContours(imag, [hull], -1, (0, 255, 0), 2)

            mask = np.zeros_like(imag)
            cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)  # Draw filled contour in mask
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

            #PREDICTION
            predict, prob = train.test_yellow(clf_yellow, out_resize)
            print(np.max(prob))
            print(predict)
            # if np.max(prob) < 0.78:
            #     continue
            cv2.rectangle(imag, (x, y), (int(x + w), int(y + h)), (0, 255, 0), 2)
            label = predict[0]
            # if label == 100:
            #     continue
            
            cnts_list.append(c)
            label_list.append(label)

            # cv2.imshow("image", out_resize)
            # cv2.waitKey(0)

            return out_resize, np.max(prob), predict