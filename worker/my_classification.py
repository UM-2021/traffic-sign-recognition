import cv2
import numpy as np
import os
from PIL import Image
from skimage import feature
from sklearn import svm


def train_red():
    folder_train_red = [["data/my_train_set/red_signs/velocidad-signal/30km", '1'],
                        ["data/my_train_set/red_signs/velocidad-signal/60km", '3'],
                        ["data/my_train_set/red_signs/velocidad-signal/90km", '6'],
                        ["data/my_train_set/red_signs/velocidad-signal/110km", '7'],
                        ["data/my_train_set/red_signs/no-sobrepasar", '8'],
                        ["data/my_train_set/red_signs/contramano", '12'],
                        ["data/my_train_set/red_signs/pare-signal", '13'],
                        ["data/my_train_set/red_signs/ceda-el-paso-signal", '14'],
                        ["data/my_train_set/red_signs/terreno-resbaladizo", '21'],
                        ["data/my_train_set/red_signs/cierre-carril", '22'],
                        ["data/my_train_set/red_signs/cuidado-bicicletas", '26']]

    hog_list_red = list()
    label_list_red = list()
    count_red = 0

    for name_red in folder_train_red:
        value_red = name_red[0]
        label_red = name_red[1]
        image_list_red = [os.path.join(value_red, f) for f in os.listdir(
            value_red) if f.endswith('.ppm')]
        # print(image_list_red)

        for image_red in image_list_red:
            count_red += 1
            # print(count_red)
            im_red = np.array(Image.open(image_red))
            im_gray_red = cv2.cvtColor(im_red, cv2.COLOR_BGR2GRAY)
            im_prep_red = cv2.resize(im_gray_red, (64, 64))

            fd_red, h_red = feature.hog(im_prep_red, orientations=9, pixels_per_cell=(
                8, 8), cells_per_block=(4, 4), transform_sqrt=False, block_norm="L1", visualize=True)
            hog_list_red.append(h_red)
            label_list_red.append(label_red)

    list_hogs_red = []
    for hogs_red in hog_list_red:
        hogs_red = hogs_red.reshape(64 * 64)
        list_hogs_red.append(hogs_red)

    clf_red = svm.SVC(gamma='scale', probability=True,
                      decision_function_shape='ovo')
    clf_red.fit(list_hogs_red, label_list_red)

    return clf_red


def test_red(clf_red, image):
    im_test_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fd_test_red, h_test_red = feature.hog(im_test_gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(4, 4),
                                          transform_sqrt=False, block_norm="L1", visualize=True)

    hog = h_test_red.reshape(64 * 64)
    predict = clf_red.predict([hog])
    class_prob = clf_red.predict_proba([hog])

    return predict, class_prob


def train_yellow():
    folder_train_yellow = [["my_train_set/yellow_signs/flecha-derecha-signal", "CURVA HACIA LA DERECHA"], [
        "my_train_set/yellow_signs/flecha-izquierda-signal", "CURVA HACIA LA IZQUIERDA"], ["my_train_set/yellow_signs/zona-escuela", "ZONA ESCUELA"]]

    hog_list_yellow = list()
    label_list_yellow = list()
    count_yellow = 0

    for name_yellow in folder_train_yellow:
        value_yellow = name_yellow[0]
        label_yellow = name_yellow[1]
        image_list_red = [os.path.join(value_yellow, f) for f in os.listdir(
            value_yellow) if f.endswith('.ppm')]

        for image_yellow in image_list_red:
            count_yellow += 1
            # print(count)
            im_yellow = np.array(Image.open(image_yellow))
            im_gray_yellow = cv2.cvtColor(im_yellow, cv2.COLOR_BGR2GRAY)
            im_prep_yellow = cv2.resize(im_gray_yellow, (64, 64))

            fd_yellow, h_yellow = feature.hog(im_prep_yellow, orientations=7, pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                                              transform_sqrt=False, block_norm="L1", visualize=True)
            # cv2.imshow('hog_train', h_yellow)
            # cv2.waitKey(50)
            hog_list_yellow.append(h_yellow)
            label_list_yellow.append(label_yellow)

    list_hogs_yellow = []
    for hogs_yellow in hog_list_yellow:
        hogs_yellow = hogs_yellow.reshape(64 * 64)
        list_hogs_yellow.append(hogs_yellow)

    clf_yellow = svm.SVC(gamma='scale', probability=True,
                         decision_function_shape='ovo')
    clf_yellow.fit(list_hogs_yellow, label_list_yellow)

    return clf_yellow


def test_yellow(clf_yellow, image):
    im_test_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fd_test_yellow, h_test_yellow = feature.hog(im_test_gray, orientations=7, pixels_per_cell=(8, 8),
                                                cells_per_block=(2, 2), transform_sqrt=False, block_norm="L1", visualize=True)

    hog = h_test_yellow.reshape(64 * 64)
    predict = clf_yellow.predict([hog])
    class_prob = clf_yellow.predict_proba([hog])

    return predict, class_prob
