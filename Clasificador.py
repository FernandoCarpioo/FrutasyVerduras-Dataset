import numpy as np
from PIL import Image, ImageTk
import joblib
import tkinter as tk
from tkinter import filedialog, Label, Button

tamano_imagen = (64, 64)

def predecir_imagen(ruta_imagen):
    modelo = joblib.load("modelo_randomforest.pkl")
    pca = joblib.load("pca_transform.pkl")
    scaler = joblib.load("scaler.pkl")

    img = Image.open(ruta_imagen).convert('RGB').resize(tamano_imagen)
    features = np.array(img).flatten().reshape(1, -1)
    features_scaled = scaler.transform(features)
    features_pca = pca.transform(features_scaled)

    pred = modelo.predict(features_pca)[0]
    proba = modelo.predict_proba(features_pca)[0]
    return pred, dict(zip(modelo.classes_, proba.round(3))), img

##INTERFAZ
def seleccionar_imagen():
    ruta_imagen = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
    )
    if ruta_imagen:
        pred, proba, img = predecir_imagen(ruta_imagen)
        mostrar_resultado(pred, proba, img)

def mostrar_resultado(pred, proba, img):
    img_mostrada = img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img_mostrada)
    lbl_imagen.config(image=img_tk)
    lbl_imagen.image = img_tk

    texto = f"Predicción: {pred}\n\nProbabilidades:\n"
    for clase, p in proba.items():
        texto += f"{clase}: {p*100:.1f}%\n"

    lbl_resultado.config(text=texto)

ventana = tk.Tk()
ventana.title("Clasificador Frutas y Verduras")
ventana.geometry("400x400")

btn_cargar = Button(ventana, text="Cargar Imagen", command=seleccionar_imagen, font=("Arial", 12))
btn_cargar.pack(pady=10)

lbl_imagen = Label(ventana)
lbl_imagen.pack(pady=10)

lbl_resultado = Label(ventana, text="", font=("Arial", 11))
lbl_resultado.pack(pady=10)

ventana.mainloop()
