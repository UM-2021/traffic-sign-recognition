import cv2 
import numpy as np
import identify_red
import os

#  TEST OF EVERY IMAGE OF TEST FOLDER 

folder='./data/my_test_set/contramano-test/'

imgcount = 0
correctpredicts = 0

for filename in os.listdir(folder):
        imgcount += 1
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            imag = np.uint8(cv2.imread(os.path.join(folder,filename)))

            result_red = identify_red.identify(imag)

            if result_red:
                result_resize_red = result_red[0]
                predict_prob_red= result_red[1]
                predict_red= result_red[2]

            # PRINT RESULTS

            print("\n\nRESULTS:")

            if result_red and predict_prob_red > 0.85:
                print("PROB RED PREDICTION: ", predict_prob_red)
                print("RED PREDICTION: ", predict_red)
                # cv2.imshow("image", result_resize_red)
                # cv2.waitKey(0)
            if predict_red == 'CONTRAMANO':
                correctpredicts += 1

print("---------------------------")
print("Correct predictions percentage: ", (correctpredicts/imgcount)*100)