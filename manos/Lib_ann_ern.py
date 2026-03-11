import cv2
import csv
import os
import time
import numpy as np
from collections import deque

# =========================
# CONFIG
# =========================
CSV_PATH = "dataset_rnn_manos.csv"

# ROI (ajústalo a tu cámara)
ROI_X, ROI_Y, ROI_W, ROI_H = 5, 100, 250, 250

def crear_headers(timesteps,num_features):
    headers = []
    for t in range(timesteps):
        for i in range(num_features):
            nombre = "t" + str(t) + "_f" + str(i)
            headers.append(nombre)
    headers.append("label")
    headers.append("timestamp")

    return headers


def crear_csv_si_no_existe(path, headers):

    if not os.path.exists(path):

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

        print("Archivo creado:", path)


def guardar_secuencia(csv_path, seq_features, label):

    flat = np.asarray(seq_features, dtype=np.float32).reshape(-1).tolist()
    row = flat + [int(label), time.time()]

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)

# =========================
# EXTRACTOR DE FEATURES (ROI)
# =========================
def extraer_features(frame_bgr, roi_x, roi_y, roi_w, roi_h):
    
    roi = frame_bgr[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    
    if roi.size == 0:
        return None

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 80, 160)

    small = cv2.resize(edges, (8, 4))
    feats = (small.flatten() / 255.0).astype(np.float32)

    return feats
    