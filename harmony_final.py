import cv2
from ultralytics import YOLO
import pygame
import math
import os
import time
import numpy as np

print("Loading YOLO model...")
model = YOLO('yolov8n.pt')

pygame.mixer.init()

# ---------------- CAMERA ----------------
def initialize_camera():
    print("Initializing camera...")

    for index in [0,1,2]:
        cap = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
        if cap.isOpened():
            print(f"Camera connected at index {index}")
            return cap

    print("No camera found.")
    exit()

cap = initialize_camera()


class HarmonyHOL:

    def __init__(self):

        # System state
        self.current_state = "IDLE"

        self.last_person = None
        self.last_waste = None
        self.last_bin = None

        # -------- Perspective Transform --------
        self.src_points = np.float32([
            [350,320],
            [1700,320],
            [120,1120],
            [1950,1120]
        ])

        self.dst_points = np.float32([
            [0,0],
            [800,0],
            [0,800],
            [800,800]
        ])

        self.M = cv2.getPerspectiveTransform(self.src_points,self.dst_points)

        #  Calibrated value (adjust if needed)
        self.pixel_to_meter = 0.0032


    def transform_point(self,point):
        pts = np.array([[point]],dtype="float32")
        transformed = cv2.perspectiveTransform(pts,self.M)

        return (
            int(transformed[0][0][0]),
            int(transformed[0][0][1])
        )


    # ---------------- DETECTION ----------------
    def perception(self,frame):

        results = model.predict(frame,conf=0.4,verbose=False)

        person=None
        waste=None

        for r in results:
            for box in r.boxes:

                cls = int(box.cls[0])
                coords = box.xyxy[0]

                center = (
                    int((coords[0]+coords[2])/2),
                    int(coords[3])
                )

                if cls == 0:
                    person=center

                elif cls in [39,41,45,67]:
                    waste=center

        # fallback memory
        if person:
            self.last_person = person
        if waste:
            self.last_waste = waste

        return person,waste,results[0].plot()


# ---------------- UI ----------------
def create_ui(frame):

    h,w,_ = frame.shape
    hud = 80

    canvas = np.zeros((h+hud,w,3),dtype=np.uint8)
    canvas[hud:] = frame

    return canvas


# ---------------- MAIN ----------------
hol = HarmonyHOL()

cv2.namedWindow("HARMONY HOL",cv2.WINDOW_NORMAL)

while cap.isOpened():

    success,frame = cap.read()
    if not success:
        break

    p_center,w_center,visual = hol.perception(frame)

    # fallback for stability
    if p_center is None:
        p_center = hol.last_person

    if w_center is None:
        w_center = hol.last_waste


    # -------- NORMAL DISTANCE --------
    raw_dist_pw = None
    if p_center and w_center:
        raw_dist_pw = math.sqrt(
            (p_center[0]-w_center[0])**2 +
            (p_center[1]-w_center[1])**2
        )

    # -------- BIRD DISTANCE --------
    dist_pw = None
    if p_center and w_center:

        tp = hol.transform_point(p_center)
        tw = hol.transform_point(w_center)

        dist_pw = math.sqrt(
            (tp[0]-tw[0])**2 +
            (tp[1]-tw[1])**2
        )


    # -------- CONVERT TO METERS --------
    normal_m = None
    bird_m = None

    if raw_dist_pw:
        normal_m = raw_dist_pw * hol.pixel_to_meter

    if dist_pw:
        bird_m = dist_pw * hol.pixel_to_meter


    # -------- UI --------
    final_display = create_ui(visual)

    if normal_m:
        cv2.putText(final_display,
                    f"Normal: {normal_m:.2f} m",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,0,255),
                    2)

    if bird_m:
        cv2.putText(final_display,
                    f"BirdEye: {bird_m:.2f} m",
                    (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2)


    # -------- BIRD VIEW --------
    top_view = cv2.warpPerspective(frame,hol.M,(800,800))

    if p_center:
        tp = hol.transform_point(p_center)
        cv2.circle(top_view,tp,10,(0,255,0),-1)
        cv2.putText(top_view,"P",(tp[0]+10,tp[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    if w_center:
        tw = hol.transform_point(w_center)
        cv2.circle(top_view,tw,10,(0,0,255),-1)
        cv2.putText(top_view,"W",(tw[0]+10,tw[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    if bird_m:
        cv2.putText(top_view,
                    f"{bird_m:.2f} m",
                    (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,255),
                    2)


    # -------- SHOW --------
    cv2.imshow("HARMONY HOL",final_display)
    cv2.imshow("Bird Eye View",top_view)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()