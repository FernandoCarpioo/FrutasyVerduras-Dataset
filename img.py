import os

ruta_base = r"C:\Users\ferna\PycharmProjects\FrutasyVerduras-Datasetnuevo\Training"

extensiones = (".png", ".jpg", ".jpeg")

ruta_frutas = os.path.join(ruta_base, "Frutas")
ruta_verduras = os.path.join(ruta_base, "Verduras")

def contar_imagenes(ruta):
    total = 0
    for root, dirs, files in os.walk(ruta):
        total += sum(1 for f in files if f.lower().endswith(extensiones))
    return total

total_frutas = contar_imagenes(ruta_frutas)
total_verduras = contar_imagenes(ruta_verduras)

print("📌 TOTAL DE IMÁGENES")
print(f"Frutas: {total_frutas}")
print(f"Verduras: {total_verduras}")
print(f"TOTAL GENERAL: {total_frutas + total_verduras}")
