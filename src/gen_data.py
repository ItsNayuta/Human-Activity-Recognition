import cv2
import mediapipe as mp
import pandas as pd
import time
from config import *
import os
import warnings

# Tắt thông báo cảnh báo, giúp làm sạch đầu ra và giảm phần nhiễu trong quá trình huấn luyện mô hình TensorFlow.
# warnings.filterwarnings('ignore')
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Init variables
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("path_to_video.mp4")
mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
pose = mpPose.Pose()
ls_landmark = []

label = 'Sneak'
print("done")
# Create dataset of landmarks and timestamp
def make_landmark_timestamp(poseRet):
    ret = []
    for idx, lm in enumerate(poseRet.pose_landmarks.landmark):
        ret.append(lm.x)
        ret.append(lm.y)
        ret.append(lm.z)
        ret.append(lm.visibility)
    return ret

# Draw landmarks on image
def draw_landmark(frame, mpDraw, pose_landmarks=None, face_landmarks = None):
    if (pose_landmarks is not None):
        mpDraw.draw_landmarks(frame, pose_landmarks, mpPose.POSE_CONNECTIONS)
    if (face_landmarks is not None):
        mpDraw.draw_landmarks(frame, face_landmarks, mpPose.FACEMESH_CONTOURS)
    return frame

def draw_count_frame(cnt, total, frame):
    text = "Frame: {}/{}".format(cnt, total)
    pos = (10,30)
    scale = 1
    thickness = 2
    lineType = 2
    fontColor = (0, 0, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(
        frame,
        text,
        pos,
        font,
        scale,
        fontColor,
        thickness,
        lineType
    )
    return frame

for i in range(5):
    print(i)
    time.sleep(1)

while len(ls_landmark) < N_FRAME:
    ret, frame = cap.read()
    if (ret):
        # Show input
        cv2.imshow('camera', frame)
        if cv2.waitKey(1)==ord('q'):
            break
        
        # Convert to RGB and create pose estimation
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        poseRet = pose.process(rgb)

        # Draw and create data
        if (poseRet.pose_landmarks):
            landmark = make_landmark_timestamp(poseRet)
            ls_landmark.append(landmark)
            frame = draw_landmark(frame, mpDraw, pose_landmarks=poseRet.pose_landmarks, face_landmarks = None)

        # Draw frame count
        frame = draw_count_frame(len(ls_landmark), N_FRAME,frame)

        # Show pose
        cv2.imshow('pose', frame)
        
df = pd.DataFrame(ls_landmark)
df.to_csv("../data2/{}.csv".format(label),index=False)

cap.release()
cv2.destroyAllWindows()