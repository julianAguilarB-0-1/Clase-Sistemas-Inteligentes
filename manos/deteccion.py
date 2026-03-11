import cv2
import numpy as np
from collections import deque
import joblib
import keras
import Lib_ann_ern

# =========================
# CONFIG
# =========================
MODEL_PATH  = "modelo_manos.keras"
SCALER_PATH = "scaler_manos.joblib"

TIMESTEPS = 10
NUM_FEATURES = 32

# ROI (ajusta)
ROI_X, ROI_Y, ROI_W, ROI_H = 5, 100, 250, 250

# Cámara
CAMERA_INDEX = 0


ADD_ONE_TO_PRED = False  # pon False si tus labels en entrenamiento fueron 0..4

model = keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    raise RuntimeError(f"No se pudo abrir la cámara index={CAMERA_INDEX}")

buffer = deque(maxlen=TIMESTEPS)

print("PREDICCIÓN EN TIEMPO REAL")
print("Teclas: r = reset buffer | ESC = salir")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    # Dibujar ROI
    cv2.rectangle(frame, (ROI_X, ROI_Y), (ROI_X+ROI_W, ROI_Y+ROI_H), (0, 255, 0), 2)

    feats = Lib_ann_ern.extraer_features(frame, ROI_X, ROI_Y, ROI_W, ROI_H)
    if feats is not None:
        buffer.append(feats)

    pred_text = "Pred: --"
    conf_text = ""

    # Si ya tenemos una secuencia completa, predecimos
    if len(buffer) == TIMESTEPS:
        seq = np.stack(buffer, axis=0)          # (TIMESTEPS, NUM_FEATURES)
        x = seq.reshape(1, -1).astype("float32")  # (1, 320) para MLP

        # Normalizar EXACTAMENTE igual que en entrenamiento
        x = scaler.transform(x).astype("float32")

        probs = model.predict(x, verbose=0)[0]   # vector de probabilidades
        pred_idx = int(np.argmax(probs))
        conf = float(np.max(probs))

        pred_label = pred_idx + 1 if ADD_ONE_TO_PRED else pred_idx
        pred_text = f"Pred: {pred_label}"
        conf_text = f"Conf: {conf:.2f}"

    # Mostrar estado
    cv2.putText(frame, f"Buffer: {len(buffer)}/{TIMESTEPS}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, pred_text, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    if conf_text:
        cv2.putText(frame, conf_text, (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Predict Manos", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    if key == ord('r'):
        buffer.clear()
        print("Buffer reiniciado.")

cap.release()
cv2.destroyAllWindows()
print("Listo.")