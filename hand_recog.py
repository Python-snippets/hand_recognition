import cv2
import mediapipe as mp


mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands


tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

hands = mp_hand.Hands(max_num_hands=1)

while True:
    ret, image = video.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    lmList = []
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            myHands = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHands.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])

            mp_draw.draw_landmarks(
                image, hand_landmark,
                mp_hand.HAND_CONNECTIONS)

    fingers = []
    if len(lmList) != 0:
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)  # 1 means open
        else:
            fingers.append(0)  # 0 means close

        # Other four fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)  # 1 means open
            else:
                fingers.append(0)  # 0 means close

        total = fingers.count(1)

        if total == 0:
            print("Close")
            cv2.rectangle(image, (20, 300), (230, 415),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "Close", (45, 375),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

        elif total == 1:
            print("One Finger")
            cv2.rectangle(image, (20, 300), (400, 415),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "One Finger", (45, 375),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        elif total == 2:
            print("Two Fingers")
            cv2.rectangle(image, (20, 300), (425, 415),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "Two Fingers", (45, 375),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        elif total == 3:
            print("Three Fingers")
            cv2.rectangle(image, (20, 300), (480, 415),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "Three Fingers", (45, 375),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        elif total == 4:
            print("Four Fingers")
            cv2.rectangle(image, (20, 300), (450, 415),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "Four Fingers", (45, 375),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        elif total == 5:
            print("Open All")
            cv2.rectangle(image, (20, 300), (305, 415),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "Open All", (45, 375),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

    # Create window with freedom of dimensions
    cv2.namedWindow("Finger Counter", cv2.WINDOW_NORMAL)
  
    imS = cv2.resize(image, (960, 720))                    # Resize 
    cv2.imshow("Finger Counter", imS)      # Show image

  

    k = cv2.waitKey(1)
    # press q for close
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()