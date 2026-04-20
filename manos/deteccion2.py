import cv2
import numpy as np
from collections import deque
import joblib
import keras
import serial
import time
import Lib_ann_ern

MODEL_PATH  = "modelo_manos.keras"
SCALER_PATH = "scaler_manos.joblib"

TIMESTEPS = 10
NUM_FEATURES = 48

ROI_X, ROI_Y, ROI_W, ROI_H = 5, 100, 250, 250

CAMERA_INDEX = 1
ADD_ONE_TO_PRED = False

model = keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Arduino
arduino = serial.Serial("COM3", 9600, timeout=1)
time.sleep(2)

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")

buffer = deque(maxlen=TIMESTEPS)

pred_label = None
conf = 0

print("PREDICCIÓN EN TIEMPO REAL")
print("ESPACIO = enviar número a Arduino")
print("ESC = salir")

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    cv2.rectangle(frame,(ROI_X,ROI_Y),(ROI_X+ROI_W,ROI_Y+ROI_H),(0,255,0),2)

    feats = Lib_ann_ern.extraer_features(frame,ROI_X,ROI_Y,ROI_W,ROI_H)

    if feats is not None:
        buffer.append(feats)

    pred_text = "Pred: --"
    conf_text = ""

    if len(buffer) == TIMESTEPS:

        seq = np.stack(buffer, axis=0)
        x = seq.reshape(1,-1).astype("float32")

        x = scaler.transform(x).astype("float32")

        probs = model.predict(x, verbose=0)[0]

        pred_idx = int(np.argmax(probs))
        conf = float(np.max(probs))

        pred_label = pred_idx + 1 if ADD_ONE_TO_PRED else pred_idx

        pred_text = f"Pred: {pred_label}"
        conf_text = f"Conf: {conf:.2f}"

    cv2.putText(frame,f"Buffer: {len(buffer)}/{TIMESTEPS}",(10,30),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    cv2.putText(frame,pred_text,(10,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)

    if conf_text:
        cv2.putText(frame,conf_text,(10,90),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    cv2.imshow("Predict Manos",frame)

    key = cv2.waitKey(1) & 0xFF

    # =========================
    # PRESIONAR ESPACIO
    # =========================
    if key == 32 and pred_label is not None:

        print("Enviando:", pred_label)

        if pred_label == 1:
            arduino.write(b'1')
        elif pred_label == 2:
            arduino.write(b'2')
        elif pred_label == 3:
            arduino.write(b'3')
        elif pred_label == 4:
            arduino.write(b'4')
        elif pred_label == 5:
            arduino.write(b'5')

    if key == 27:
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()

print("Programa finalizado")