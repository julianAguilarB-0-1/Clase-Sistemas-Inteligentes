import json
import pickle
import random
import numpy as np

import nltk
from nltk.stem import SnowballStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# ── Descargar recursos de NLTK (solo la primera vez) ──
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

# ── Configuración ──────────────────────────────────────
DATASET_PATH = "dataset.json"
MODELO_PATH  = "modelo_chatbot.pkl"
STEMMER      = SnowballStemmer("spanish")

# ── Carga del dataset ──────────────────────────────────
with open(DATASET_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

intents = data["intents"]

# ── Preparación de datos ───────────────────────────────
textos    = []   # frases de entrenamiento
etiquetas = []   # tags correspondientes

for intent in intents:
    if intent["tag"] == "desconocido":
        continue                        # se maneja aparte
    for pattern in intent["patterns"]:
        textos.append(pattern.lower())
        etiquetas.append(intent["tag"])

if not textos:
    raise ValueError("El dataset no contiene patrones de entrenamiento.")

print(f"Patrones cargados: {len(textos)}")
print(f"Clases únicas   : {len(set(etiquetas))}\n")

# ── Construcción del pipeline ──────────────────────────
#   TF-IDF vectoriza el texto → Logistic Regression clasifica
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        analyzer="char_wb",      # n-gramas de caracteres (más robusto al español)
        ngram_range=(2, 4),
        min_df=1,
        sublinear_tf=True
    )),
    ("clf", LogisticRegression(
        max_iter=1000,
        solver="lbfgs",
        multi_class="multinomial",
        C=5.0,
        random_state=42
    ))
])

# ── Entrenamiento ──────────────────────────────────────
pipeline.fit(textos, etiquetas)
print("✔ Modelo entrenado correctamente.")

# ── Evaluación rápida (sobre los mismos datos de entrenamiento) ──
score = pipeline.score(textos, etiquetas)
print(f"✔ Precisión en entrenamiento: {score * 100:.1f}%\n")

# ── Guardar modelo y respuestas ────────────────────────
respuestas = {
    intent["tag"]: intent["responses"]
    for intent in intents
}

with open(MODELO_PATH, "wb") as f:
    pickle.dump({"pipeline": pipeline, "respuestas": respuestas}, f)

print(f"Modelo guardado en: {MODELO_PATH}")
print("\n¡Entrenamiento completado!")