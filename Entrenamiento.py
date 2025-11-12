import os, random
import numpy as np
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

##AQUI COLOCAR LA RUTA BIEN
ruta_training = r"C:\Users\ferna\PycharmProjects\FrutasyVerduras-Datasetnuevo\Training"
ruta_test = r"C:\Users\ferna\PycharmProjects\FrutasyVerduras-Datasetnuevo\Test"
max_imagenes_por_clase = 1000
tamano_imagen = (64, 64)

def cargar_datos_recursivo(ruta_base, max_por_clase=None):
    X, y = [], []
    total_imagenes = 0

    for root, dirs, files in os.walk(ruta_base):
        partes = root.split(os.sep)
        if len(partes) < 2:
            continue
        etiqueta = partes[-2]
        imagenes = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if max_por_clase and len(imagenes) > max_por_clase:
            imagenes = random.sample(imagenes, max_por_clase)

        for img_file in imagenes:
            ruta_imagen = os.path.join(root, img_file)
            try:
                img = Image.open(ruta_imagen).convert('RGB').resize(tamano_imagen)
                features = np.array(img).flatten()
                X.append(features)
                y.append(etiqueta)
                total_imagenes += 1
            except Exception as e:
                print(f"Error cargando {ruta_imagen}: {e}")

    print(f"Se cargaron {total_imagenes} imágenes desde {ruta_base}")
    return np.array(X), np.array(y)

print("Cargando datos...")
X_train, y_train = cargar_datos_recursivo(ruta_training, max_imagenes_por_clase)
X_test, y_test = cargar_datos_recursivo(ruta_test, max_imagenes_por_clase)

print("Estandarizando y aplicando PCA...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

pca = PCA(n_components=100)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

print("Entrenando Random Forest...")
modelo_rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    n_jobs=-1,
    random_state=42
)
modelo_rf.fit(X_train_pca, y_train)

y_pred = modelo_rf.predict(X_test_pca)
print(f"\nPrecisión: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))
print("Matriz de confusión:")
print(confusion_matrix(y_test, y_pred))

joblib.dump(modelo_rf, "modelo_randomforest.pkl")
joblib.dump(pca, "pca_transform.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\n✅ Modelo, PCA y Scaler guardados correctamente.")
