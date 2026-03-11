import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import tensorflow as tf
import keras
from keras import layers

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def mostrar_matriz_confusion(model, X_test, y_test):
    """
    Genera y muestra la matriz de confusión como mapa de calor.
    """
    # Predicciones
    y_pred = np.argmax(model.predict(X_test), axis=1)

    # Matriz
    cm = confusion_matrix(y_test, y_pred)

    # Mapa de calor
    plt.figure(figsize=(6,5))
    sns.heatmap(cm,
                annot=True,
                fmt="d",
                cmap="Blues",
                xticklabels=["1","2","3","4","5"],
                yticklabels=["1","2","3","4","5"])

    plt.xlabel("Predicción")
    plt.ylabel("Clase Real")
    plt.title("Matriz de Confusión - Reconocimiento de Dedos")
    plt.show()


CSV_PATH = "dataset_rnn_manos.csv"

# 1) Cargar dataset
df = pd.read_csv(CSV_PATH)

X = df.drop(columns=["label", "timestamp"], errors="ignore").values.astype("float32")
y = df["label"].values.astype("int32")  # 0..9

# 2) Split (estratificado)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3) Normalizar (clave para redes)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train).astype("float32")
X_test  = scaler.transform(X_test).astype("float32")

# 4) Modelo MLP pequeño (tabular)
model = keras.Sequential([
    layers.Input(shape=(X_train.shape[1],)),
    layers.Dense(64, activation="relu"),
    layers.Dense(32, activation="relu"),
    layers.Dense(10, activation="softmax")
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# 5) Callbacks (EarlyStopping para no sobreentrenar)
early = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=15,
    restore_best_weights=True
)  # docs oficiales :contentReference[oaicite:1]{index=1}

history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=300,
    batch_size=32,
    callbacks=[early],
    verbose=1
)

# 6) Evaluación
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_acc:.4f}")

# 7) Guardar modelo + scaler
model.save("modelo_manos.keras")
import joblib
joblib.dump(scaler, "scaler_manos.joblib")

print("Guardado: modelo_manos.keras y scaler_manos.joblib")


test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_acc:.4f}")

#Y justo debajo pegas

mostrar_matriz_confusion(model, X_test, y_test)