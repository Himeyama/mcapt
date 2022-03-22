from types import ModuleType
import cv2
import mediapipe as mp
import pandas as pd
import time
import logging as log
log.basicConfig(level=log.DEBUG)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands: ModuleType = mp.solutions.hands

# Web カメラ
cap: cv2.VideoCapture = cv2.VideoCapture(0)
data_list: list[pd.DataFrame] = []

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    start: float = time.time()
    frame: int = 0
    while cap.isOpened():
        success: bool
        image: cv2.VideoCapture
        success, image = cap.read()
        if not success:
            print("空のカメラフレームを無視します。")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        # BGR -> RGB 変換
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 推定
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in \
                    enumerate(results.multi_hand_landmarks):
                # print(hand_landmarks.landmark[0].x)
                df_list = [
                    {'Frame': frame,
                     'Time': time.time() - start,
                     'Hand': hand_idx,
                     'Part': i,
                     'X': _.x,
                     'Y': _.y,
                     'Z': _.z}
                    for i, _ in enumerate(hand_landmarks.landmark)
                ]
                frame += 1
                df = pd.DataFrame(df_list)
                data_list.append(df)

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands (press ESC to exit)', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:  # ESC
            break

# cap.release()
cv2.destroyAllWindows()

if data_list:
    log.info('キャプチャーデータを保存しました。')
    df = pd.concat(data_list)
    df.to_csv("test.csv", index=None)
else:
    log.warning('キャプチャーデータは存在しないため保存されませんでした。')
