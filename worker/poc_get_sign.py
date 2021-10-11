import cv2 
import numpy as np
import os
from PIL import Image
from joblib import load
import identify_red
import identify_yellow 

imag = np.uint8(cv2.imread('./my_test_set/testnico1.png'))
# imag = np.uint8(cv2.imread('./my_test_set/amarelo.jpg'))
# imag = np.uint8(cv2.imread('./my_test_set/cedapaso.jpg'))

result_red = identify_red.identify(imag)

if result_red:
    result_resize_red = result_red[0]
    predict_prob_red= result_red[1]
    predict_red= result_red[2]

result_yellow = identify_yellow.identify(imag)


if result_yellow:
    result_resize_yellow = result_yellow[0]
    predict_prob_yellow= result_yellow[1]
    predict_yellow= result_yellow[2]

# PRINT RESULTS

print("\n\nRESULTS:")

if result_red and predict_prob_red > 0.2: # and predict_prob_red > predict_prob_yellow:
    print("PROB RED PREDICTION: ", predict_prob_red)
    print("RED PREDICTION: ", predict_red)
    cv2.imshow("image", result_resize_red)
    cv2.waitKey(0)
    
if result_yellow and predict_prob_yellow > 0.2: # and predict_prob_red < predict_prob_yellow:
    print("PROB YELLOW PREDICTION: ", predict_prob_yellow)
    print("YELLOW PREDICTION: ", predict_yellow)
    cv2.imshow("image", result_resize_yellow)
    cv2.waitKey(0)
    
