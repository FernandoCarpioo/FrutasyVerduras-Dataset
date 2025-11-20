import numpy as np
from PIL import Image, ImageTk
import joblib
import tkinter as tk
from tkinter import filedialog, Label, Button

tamano_imagen = (192, 192)


def predecir_imagen(ruta_imagen):
    # Cargar el pipeline (scaler + PCA + SVM)
    modelo = joblib.load("modelo_svm_pipeline.pkl")

    img = Image.open(ruta_imagen).convert("RGB").resize(tamano_imagen)
    features = np.array(img).flatten().reshape(1, -1)

    # Predicción
    pred = modelo.predict(features)[0]

    # Probabilidades: FRUTA vs VERDURA
    proba = modelo.predict_proba(features)[0]

    # Diccionario: {"Frutas": xx, "Verduras": yy}
    proba_dict = dict(zip(modelo.classes_, proba))

    return pred, proba_dict, img


### --- INTERFAZ --- ###

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

    # Mostrar porcentajes
    texto = f"Predicción: {pred}\n\n"
    texto += "Probabilidades:\n"

    for clase, p in proba.items():
        texto += f"{clase}: {p * 100:.2f}%\n"

    lbl_resultado.config(text=texto)


# Ventana
ventana = tk.Tk()
ventana.title("Clasificador Frutas y Verduras")
ventana.geometry("400x450")

btn_cargar = Button(ventana, text="Cargar Imagen", command=seleccionar_imagen, font=("Arial", 12))
btn_cargar.pack(pady=10)

lbl_imagen = Label(ventana)
lbl_imagen.pack(pady=10)

lbl_resultado = Label(ventana, text="", font=("Arial", 11))
lbl_resultado.pack(pady=10)

ventana.mainloop()
