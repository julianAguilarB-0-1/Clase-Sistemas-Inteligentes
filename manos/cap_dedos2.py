import cv2
import csv
import os
import time
import numpy as np
from collections import deque
import Lib_ann_ern

CSV_PATH = "dataset_rnn_manos.csv"
TIMESTEPS = 10
NUM_FEATURES = 32

ROI_X, ROI_Y, ROI_W, ROI_H = 5, 100, 250, 250
headers = Lib_ann_ern.crear_headers(TIMESTEPS, NUM_FEATURES)
Lib_ann_ern.crear_csv_si_no_existe(CSV_PATH, headers)

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")

buffer = deque(maxlen=TIMESTEPS)

# contador por dedo
conteo = {1:0, 2:0, 3:0, 4:0, 5:0}

print("CAPTURA DE FEATURES (RNN)")
print("Teclas: 1-5 = guardar secuencia | r = reset buffer | ESC = salir")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    cv2.rectangle(frame, (ROI_X, ROI_Y), (ROI_X+ROI_W, ROI_Y+ROI_H), (0, 255, 0), 2)

    feats = Lib_ann_ern.extraer_features(frame, ROI_X, ROI_Y, ROI_W, ROI_H)

    if feats is not None:
        feats = np.asarray(feats, dtype=np.float32).reshape(-1)
        if feats.shape[0] != NUM_FEATURES:
            raise ValueError(f"extraer_features devolvió {feats.shape[0]} features, pero NUM_FEATURES={NUM_FEATURES}")
        buffer.append(feats)

    # Información del buffer
    cv2.putText(frame, f"Buffer: {len(buffer)}/{TIMESTEPS}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2)

    cv2.putText(frame, "1-5 guarda | r reset | ESC salir",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2)

    # Aviso cuando la secuencia está completa
    if len(buffer) == TIMESTEPS:
        cv2.putText(frame, "SECUENCIA LISTA - PRESIONA 1-5",
                    (10, 95),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,0,255),
                    2)

    # 🔹 Mostrar conteo de capturas en pantalla
    y_offset = 130
    for dedo in conteo:
        texto = f"Dedo {dedo}: {conteo[dedo]}"
        cv2.putText(frame, texto,
                    (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255,255,0),
                    2)
        y_offset += 25

    cv2.imshow("Camara", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break

    if key == ord('r'):
        buffer.clear()
        print("Buffer reiniciado.")
        continue

    if ord('1') <= key <= ord('5'):
        label = key - ord('0')

        if len(buffer) < TIMESTEPS:
            print(f"Faltan frames: {len(buffer)}/{TIMESTEPS}. Espera y vuelve a presionar {label}.")
            continue

        seq = np.stack(buffer, axis=0)
        Lib_ann_ern.guardar_secuencia(CSV_PATH, seq, label)

        conteo[label] += 1

        print(f"✅ Guardada secuencia label={label} | frames={TIMESTEPS} | feats/frame={NUM_FEATURES}")

cap.release()
cv2.destroyAllWindows()

print("\n📊 RESUMEN DE CAPTURAS:")
total = 0
for dedo in conteo:
    print(f"Dedo {dedo}: {conteo[dedo]} secuencias")
    total += conteo[dedo]

print(f"TOTAL: {total} secuencias")
print("Listo.")