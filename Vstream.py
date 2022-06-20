import cv2

capture = cv2.VideoCapture("https://192.168.0.16:8080/video")

while True:
    _, frame = capture.read()

    # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) # for grayscale
    cv2.imshow('livestream', frame)
    if cv2.waitKey(1) == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()
