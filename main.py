import cv2
import imutils
import mediapipe

mp_draw = mediapipe.solutions.drawing_utils
mp_draw_styles = mediapipe.solutions.drawing_styles
mp_pose = mediapipe.solutions.pose

count = 0
position = None
cap = cv2.VideoCapture("shim.mp4")

with mp_pose.Pose(
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.7) as pose:
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("empty camera")
            break

        image = imutils.resize(image, width=500)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        result = pose.process(image)
        lmList = []

        if result.pose_landmarks:
        # Draws the landmarks' points and connects them
            mp_draw.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            for id, im in enumerate(result.pose_landmarks.landmark):
                # Finding the length and width of the video input
                h, w, _ = image.shape

                # Finding the exact coordinates of the body points
                X, Y = int(im.x * w), int(im.y * h)
                lmList.append([id, X, Y])
        lmList = []

        if result.pose_landmarks:
        # Draws the landmarks' points and connects them
            mp_draw.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            for id, im in enumerate(result.pose_landmarks.landmark):
                # Finding the length and width of the video input
                h, w, _ = image.shape

            #    Finding the exact coordinates of the body points
                X, Y = int(im.x * w), int(im.y * h)
                lmList.append([id, X, Y])

    # Checking whether there are any identified landmarks
        if len(lmList) != 0:
        # Condition that identifies the down position
            if (lmList[12][2] and lmList[11][2] >= lmList[14][2] and lmList[13][2]):
                position = "down"

        # Condition that identifies the up position
            if ((lmList[12][2] and lmList[11][2] <= lmList[14][2] and lmList[13][2])
                and position == "down"):
                position = "up"
                count += 1
                print(count)

        cv2.imshow("Push-up counter", cv2.flip(image, 1))
        key = cv2.waitKey(1)

# Program terminates when q is pressed
        if key == ord('q'):
            cap.release()
