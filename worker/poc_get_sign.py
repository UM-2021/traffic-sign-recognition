import cv2 
import numpy as np
import identify_red

imag = np.uint8(cv2.imread('./data/my_test_set/cierre-carril-test/00044.png'))

result_red = identify_red.identify(imag)

if result_red:
    result_resize_red = result_red[0]
    predict_prob_red= result_red[1]
    predict_red= result_red[2]

# PRINT RESULTS

print("\n\nRESULTS:")

if result_red and predict_prob_red > 0.8:
    print("PROB RED PREDICTION: ", predict_prob_red)
    print("RED PREDICTION: ", predict_red)
    cv2.imshow("image", result_resize_red)
    cv2.waitKey(0)
    

    
