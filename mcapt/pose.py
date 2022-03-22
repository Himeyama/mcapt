import cv2
import mediapipe as mp
# import numpy as np
import itertools
import socket
import struct
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


HOST = 'localhost'
PORT = 8010

# For webcam input:
cap = cv2.VideoCapture(1)
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    # data = s.recv(1024)

    while cap.isOpened():
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
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # s.sendall(b'Test!!')

        if results.pose_landmarks:
            l = [[i, _.x, _.y, _.z] for i, _ in enumerate(results.pose_landmarks.landmark)]
            l[:] = list(itertools.chain.from_iterable(l))
            print(l)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(struct.pack('<132d', *l))
            # s.send(bytes(l))

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands (press ESC to exit)', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
