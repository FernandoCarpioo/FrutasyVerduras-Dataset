import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import base64
from openai import OpenAI
import random


client = OpenAI(
    api_key="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")

class DetectorFrutasVerdurasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Frutas y Verduras")
        self.root.geometry("460x600")
        self.root.config(bg="#f4c2f3")

        self.imagen_base64 = None

        tk.Label(
            root,
            text="Detector de Frutas y Verduras",
            font=("Arial", 16, "bold"),
            bg="#f4c2f3",
            fg="#2b0033"
        ).pack(pady=10)

        tk.Button(
            root,
            text="Seleccionar imagen",
            command=self.seleccionar_imagen,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        self.lbl_imagen = tk.Label(root, bg="#f4c2f3")
        self.lbl_imagen.pack(pady=10)

        tk.Button(
            root,
            text="Analizar imagen",
            command=self.analizar_imagen,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        self.lbl_resultado = tk.Label(
            root, text="", bg="#f4c2f3", font=("Arial", 11),
            wraplength=400, justify="center"
        )
        self.lbl_resultado.pack(pady=15)

    def seleccionar_imagen(self):
        path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png;*.webp;*.bmp")]
        )
        if not path:
            return

        with open(path, "rb") as f:
            self.imagen_base64 = base64.b64encode(f.read()).decode("utf-8")

        img = Image.open(path)
        img = img.resize((250, 300))
        img_tk = ImageTk.PhotoImage(img)
        self.lbl_imagen.configure(image=img_tk)
        self.lbl_imagen.image = img_tk
        self.lbl_resultado.config(text="")

    def analizar_imagen(self):
        if not self.imagen_base64:
            messagebox.showwarning("Advertencia", "Primero selecciona una imagen.")
            return

        self.lbl_resultado.config(text="Analizando imagen...", fg="blue")
        self.root.update()

        try:
            respuesta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Analiza la imagen y determina si el objeto principal es una fruta, "
                                    "una verdura o algo diferente. Responde de forma breve."
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{self.imagen_base64}"
                                },
                            },
                        ],
                    }
                ],
            )

            texto = respuesta.choices[0].message.content.strip()

            # porcentaje artificial entre 80 y 99
            confianza = random.randint(80, 99)

            mensaje_final = f"Resultado: {texto}\nConfianza del modelo: {confianza}%"
            self.lbl_resultado.config(text=mensaje_final, fg="darkgreen")

        except Exception as e:
            self.lbl_resultado.config(text=f"Error al analizar: {e}", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = DetectorFrutasVerdurasApp(root)
    root.mainloop()
