import cv2
import pickle

plant_image = cv2.imread('plant_sample2.jpg')

width, height = 75, 75


# need to try to find the file(plant_space_position) if present
# then load the position list, to avoid  replace a new one when its run again
try:
    with open('plant_space_position', 'rb') as f:
        position_list = pickle.load(f)
except:
    position_list = []


def mouse_click(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        position_list.append((x, y))  # add square from the frame
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(position_list):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:  # check if the mouse is  inside the square
                position_list.pop(i)  # delete square form the frame


# save the position list into a file so that if we close and run again the previews position stay the same
    with open('plant_space_position', 'wb') as f:
        pickle.dump(position_list, f)


while True:
    plant_image = cv2.imread('plant2.jpg')

    for pos in position_list:
        cv2.rectangle(plant_image, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow('plant_tray', plant_image)
    cv2.setMouseCallback('plant_tray', mouse_click)

    if cv2.waitKey(10) == ord("q"):  # 10
        break

cv2.destroyAllWindows()
