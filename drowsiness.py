import cv2
import time
try:
    import winsound
except ImportError:
    class WinsoundMock:
        @staticmethod
        def Beep(frequency, duration):
            # Fallback for Linux/macOS where winsound is not available
            print(f"🔊 [Beep Fallback] Freq: {frequency}Hz, Dur: {duration}ms")
    winsound = WinsoundMock()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)

def start_drowsiness():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not working ❌")
        return

    closed_start = None
    status = "ACTIVE"
    alarm_on = False   # 🔴 ADD

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        eyes_detected = False
        face_detected = False   # 🔴 ADD

        if len(faces) > 0:
            face_detected = True

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(frame, (x+ex,y+ey), (x+ex+ew,y+ey+eh), (0,255,0), 2)

            if len(eyes) > 0:
                eyes_detected = True

        # 🔴 FIXED LOGIC
        if face_detected and not eyes_detected:
            if closed_start is None:
                closed_start = time.time()
            else:
                if time.time() - closed_start > 2:
                    status = "DROWSY"

                    # 🔴 beep only once
                    if not alarm_on:
                        winsound.Beep(2500, 2000)
                        alarm_on = True

                    # 🔴 status write
                    with open("status.txt", "w") as f:
                        f.write("DROWSY")

        else:
            closed_start = None
            alarm_on = False   # 🔴 RESET

            if face_detected:
                with open("status.txt", "w") as f:
                    f.write("ACTIVE")

        cv2.putText(frame, status, (30,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0,0,255), 2)

        cv2.imshow("Driver Monitoring", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_drowsiness()