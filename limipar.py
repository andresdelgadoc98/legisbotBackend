import re


with open('db/pdfs/Codigo_Proced_Civil.txt', 'r', encoding='utf-8') as file:
    contenido = file.read()

contenido_limpio = re.sub(r'Periddico Oficial del Estado Pagina \d+ de \d+', '', contenido)

# Guarda el archivo limpio
with open('archivo_limpio.txt', 'w', encoding='utf-8') as file:
    file.write(contenido_limpio)

print("Pie de página eliminado y archivo guardado como 'archivo_limpio.txt'.")