import os
import random
import numpy as np
from PIL import Image
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import joblib


# RUTA DE TU DATASET
ruta_training = r"C:\Users\ferna\PycharmProjects\FrutasyVerduras-Datasetnuevo\Training"

# TAMAÑO DE IMAGEN
tamano_imagen = (192, 192)

# -------------------------------------------------------------
# Cargar imágenes con límite por clase (float32 optimizado)
# -------------------------------------------------------------
def cargar_muestras_limitadas(ruta_base, limite=9100):
    X, y = [], []

    ruta_frutas = os.path.join(ruta_base, "Frutas")
    ruta_verduras = os.path.join(ruta_base, "Verduras")

    def recolectar_imagenes(ruta_categoria):
        lista = []
        for root, _, files in os.walk(ruta_categoria):
            for f in files:
                if f.lower().endswith((".png", ".jpg", ".jpeg")):
                    lista.append(os.path.join(root, f))
        return lista

    print("Recolectando rutas de imágenes...")
    frutas = recolectar_imagenes(ruta_frutas)
    verduras = recolectar_imagenes(ruta_verduras)

    random.shuffle(frutas)
    random.shuffle(verduras)

    frutas = frutas[:limite]
    verduras = verduras[:limite]

    print(f"Usando {len(frutas)} frutas y {len(verduras)} verduras")

    def cargar_lista(lista, etiqueta):
        for ruta in lista:
            try:
                img = Image.open(ruta).convert("RGB").resize(tamano_imagen)
                # FLOAT32 → LA MITAD DE RAM
                X.append(np.array(img, dtype=np.float32).flatten())
                y.append(etiqueta)
            except:
                pass

    print("Cargando imágenes a memoria...")
    cargar_lista(frutas, "Frutas")
    cargar_lista(verduras, "Verduras")

    return np.array(X, dtype=np.float32), np.array(y)

# -------------------------------------------------------------
# ENTRENAMIENTO COMPLETO (sin test)
# -------------------------------------------------------------

print("\nCargando datos del dataset...")
X, y = cargar_muestras_limitadas(ruta_training, limite=9100)

print(f"\nTotal de imágenes cargadas: {X.shape[0]}")
print(f"Dimensión de cada imagen: {X.shape[1]}")

# Asegurar float32 (por si acaso)
X = X.astype(np.float32)

# -------------------------------------------------------------
# Pipeline: Scaler + PCA + SVM probabilístico
# -------------------------------------------------------------
modelo = Pipeline([
    ("scaler", StandardScaler(with_mean=True, with_std=True)),
    ("pca", PCA(n_components=100)),  # 100 componentes = mejor para RAM
    ("svm", SVC(kernel="rbf", probability=True, C=10, gamma='scale'))
])


print("\nEntrenando modelo SVM + PCA + Scaler...")
modelo.fit(X, y)

# Guardar pipeline COMPLETO
joblib.dump(modelo, "modelo_svm_pipeline.pkl")

print("\n✔ Entrenamiento COMPLETO!")
print("✔ Modelo guardado como: modelo_svm_pipeline.pkl")
