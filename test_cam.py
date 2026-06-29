import cv2

print("Starting camera test...")

# macOS needs AVFoundation backend
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()
else:
    print("✅ Camera connected! Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("HARMONY Test Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
