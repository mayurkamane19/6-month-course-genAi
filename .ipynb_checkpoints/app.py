import cv2
import numpy as np
from ultralytics import YOLO
import os

# -------------------- YOUR VIDEO (fixed absolute path) --------------------
video_path = r"C:\Users\mayur\Downloads\road_trafifc.mp4"

if not os.path.exists(video_path):
    raise FileNotFoundError(f"❌ ERROR: Video NOT found at:\n{video_path}")

print("✔ Using Video:", video_path)

# -------------------- LOAD YOLO MODEL --------------------
model = YOLO("yolo11s.pt")   # auto-downloads if missing
print("✔ YOLO11 Model Loaded")

# -------------------- LANE DETECTION --------------------
def detect_lanes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    edges = cv2.Canny(blur,100,200)

    h, w = edges.shape
    mask = np.zeros_like(edges)
    roi = np.array([[(0,h),(w,h),(w,int(h*0.55)),(0,int(h*0.55))]])
    cv2.fillPoly(mask, roi, 255)

    masked = cv2.bitwise_and(edges, mask)
    lines = cv2.HoughLinesP(masked,1,np.pi/180,70,minLineLength=80,maxLineGap=60)

    if lines is not None:
        for l in lines:
            x1,y1,x2,y2 = l[0]
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),3)

    return frame

# -------------------- SPEED DETECTION --------------------
previous_positions = {}
pixel_dist = 80
meters_dist = 8
fps = 24

speed_factor = (meters_dist / pixel_dist) * fps * 3.6   # km/h conversion

# -------------------- VIDEO PROCESSING --------------------
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise Exception("❌ ERROR: Video cannot be opened. Wrong path or corrupted file.")

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output_traffic.mp4", fourcc, fps,
                      (int(cap.get(3)), int(cap.get(4))))

print("✔ Processing started... Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("✔ Video Finished!")
        break

    results = model(frame, stream=True)

    for r in results:
        boxes = r.boxes.xyxy
        ids = r.boxes.id
        cls = r.boxes.cls

        if ids is None: 
            continue

        for i, box in enumerate(boxes):
            x1,y1,x2,y2 = map(int, box)
            obj_id = ids[i].item()
            label = int(cls[i])

            # Cars, bikes, buses, trucks
            if label not in [2,3,5,7]:
                continue

            cx = int((x1 + x2) // 2)

            # SPEED CALCULATION
            if obj_id in previous_positions:
                old_x = previous_positions[obj_id]
                movement = abs(cx - old_x)
                speed = movement * speed_factor
                cv2.putText(frame, f"{speed:.1f} km/h",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255,50,0), 2)

            previous_positions[obj_id] = cx

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,120,255),2)

    # Add lane detection
    frame = detect_lanes(frame)

    out.write(frame)
    cv2.imshow("YOLO11 Traffic Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("✔ Output saved: output_traffic.mp4")
print("✔ Traffic Analysis Completed Successfully!")
