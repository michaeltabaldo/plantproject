import cv2
import pickle
import cvzone
import numpy as np

# video feed
# cap = cv2.VideoCapture("https://192.168.0.16:8080/video")
image = cv2.imread('plant2.jpg')

with open('plant_space_position', 'rb') as f:
    position_list = pickle.load(f)

width, height = 75, 75


def check_plant_space(image_process):
    # to count the  space
    space_counter = 0

    for pos in position_list:
        x, y = pos

        # to crop image
        image_crop = image_process[y:y + height, x: x + width]
        # cv2.imshow(str(x * y), image_crop)

        # pixel count is not a lot pixel means no plant
        count = cv2.countNonZero(image_crop)

        # put pixel count inside the crop image
        cvzone.putTextRect(image, str(count), (x, y + height - 4), scale=1.2, thickness=1, offset=0, colorR=(0, 0, 255))

        if count < 600:
            color = (0, 0, 255)  # red
            thickness = 5
            space_counter += 1
        else:
            color = (0, 255, 0)  # green
            thickness = 2
        cv2.rectangle(image, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(image, f'NG: {space_counter}/{len(position_list)}', (80, 45), scale=3, thickness=2, offset=10,
                       colorR=(0, 200, 0))


while True:
    # if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # for looping video feed,
    #     if exceed to total frame count it will reset to o means beginning

    # success, img = cap.read()

    # convert crop image into binary image, to base on their edges or corners to compute pixel count
    # if it is a plane image means no plant, if its have a higher pixel value means it has a plant.
    # first we do thresholding, after we get our image we convert it to a grayscale.
    # after gray, we add some blur
    # image_gray = cv2.cvtColor(image, cv2.COLOR_BAYER_RG2GRAY)

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # after gray, we add some blur
    image_blur = cv2.GaussianBlur(image_gray, (3, 3), 1)

    # after blur convert to binary image
    image_threshold = cv2.adaptiveThreshold(image_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 25, 18)
    # remove salt like in image
    image_median = cv2.medianBlur(image_threshold, 5)

    # the line thicker
    kernel = np.ones((3, 3), np.uint8)
    image_dilate = cv2.dilate(image_median, kernel, iterations=1)

    check_plant_space(image_dilate)

    # for pos in position_list:
    #     cv2.rectangle(image, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow('plant_tray_2', image)
    # cv2.imshow('imageBlur', image_blur)
    cv2.imshow('imageThresh', image_median)

    # cv2.imshow('plant_video_feed', cap)

    if cv2.waitKey(10) == ord("q"):  # 10
        break

cv2.destroyAllWindows()
