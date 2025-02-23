'''
PROCESO DIGITAL DE IMAGENES 2025-2

Tarea 2: Sopa de letras. 

Alumna: Gabriela López Diego 
No. de cuenta: 318243485 
Fecha: Febrero 2025
'''
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def letter_with_color(imagen_path, letra, tam_bloque=15):  
    '''
    Ejercicio 1: Crear una imagen con la letra "M" en cada bloque de la imagen original, con el color promedio del bloque.
    
    Parámetros:
        - imagen_path: str, ruta de la imagen a procesar.
        - letra: str, letra a dibujar en cada bloque.
        - tam_bloque: int, tamaño de los bloques en los que se dividirá la imagen.
        
    Devuelve:
        - Guarda la imagen resultante en el directorio de trabajo.
    '''
    imagen = Image.open(imagen_path)
    imagen = imagen.convert("RGB")  
    ancho, alto = imagen.size

    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Imagen con fondo blanco para apreciar mejor el resultado generado
    draw = ImageDraw.Draw(imagen_pil)
    #Cargamos la fuente Roboto proporcionada en el proyecto
    fuente = ImageFont.truetype("Fuentes/Roboto.ttf", tam_bloque)

    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen.crop((x, y, x + tam_bloque, y + tam_bloque))
            bloque_array = np.array(bloque)
            color_promedio = np.mean(bloque_array, axis=(0, 1)).astype(int)
            draw.text((x, y), letra, font=fuente, fill=tuple(color_promedio))

    imagen_pil.save("1_M_con_color.png")  # Guarda la imagen
    print("Imagen guardada como 1_M_con_color.png")

def letter_with_grayscale(imagen_path, letra, tam_bloque=15):  
    '''
    Ejercicio 2: Crear una imagen con la letra "M" en cada bloque de la imagen original,
    con el valor promedio en escala de grises del bloque.
    
    Parámetros:
        - imagen_path: str, ruta de la imagen a procesar.
        - letra: str, letra a dibujar en cada bloque.
        - tam_bloque: int, tamaño de los bloques en los que se dividirá la imagen.
        
    Devuelve:
        - Guarda la imagen resultante en el directorio de trabajo.
    '''
    imagen = Image.open(imagen_path)
    imagen = imagen.convert("RGB")  # Asegurarse de que la imagen esté en formato RGB
    ancho, alto = imagen.size

    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Imagen con fondo blanco
    draw = ImageDraw.Draw(imagen_pil)

    # Cargar la fuente con una M 
    fuente = ImageFont.truetype("Fuentes/Roboto.ttf", tam_bloque)

    # Recorrer la imagen en bloques de tamaño tam_bloque
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen.crop((x, y, x + tam_bloque, y + tam_bloque))
            bloque_array = np.array(bloque)
            gris_promedio = np.mean(bloque_array @ [0.2989, 0.5870, 0.1140])  # Fórmula de RGB a gris
            # Convertir el valor gris promedio a un valor entero de 0 a 255
            gris_promedio = int(gris_promedio)
            draw.text((x, y), letra, font=fuente, fill=(gris_promedio, gris_promedio, gris_promedio))

    imagen_pil.save("2_M_con_escala_de_grises.png")  
    print("Imagen guardada como 2_M_con_escala_de_grises.png")
    
    
def letters_bn(imagen_path, tam_bloque=15):
    '''
    Ejercicio 3: Letras blanco y negro. Reemplazamos los tonos de gris con letras de la lista.
    
    Parámetros:
        - imagen_path: str, ruta de la imagen a procesar.
        - tam_bloque: int, tamaño de los bloques en los que se dividirá la imagen.
        
    Devuelve:
        - Guarda la imagen resultante en el directorio de trabajo.
    '''
    # Lista de letras para reemplazar los tonos de gris
    letras = ["M", "N", "H", "#", "Q", "U", "A", "D", "0", "Y", "2", "$", "%", "+", "."]
    
    imagen = Image.open(imagen_path)
    imagen = imagen.convert("RGB") 
    ancho, alto = imagen.size

    imagen_new = Image.new("RGB", (ancho, alto), (250, 250, 250))  # Fondo gris 
    draw = ImageDraw.Draw(imagen_new)

    # Cargar la fuente con una M gordita y gruesa
    fuente = ImageFont.truetype("Fuentes/Roboto.ttf", tam_bloque)

    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen.crop((x, y, x + tam_bloque, y + tam_bloque))
            bloque_array = np.array(bloque)
            gris_promedio = np.mean(bloque_array @ [0.2989, 0.5870, 0.1140])  # Fórmula de RGB a gris
            gris_promedio = int(gris_promedio)
            intervalo = gris_promedio // (256 // len(letras))
            letra = letras[intervalo]
            draw.text((x, y), letra, font=fuente, fill=(0, 0, 0))  # Letras en negro

    imagen_new.save("3_letras_bn_gris.png")
    print("Imagen guardada como 3_letras_bn_gris.png")


def color_with_text(imagen_path, texto, tam_bloque=15):
    '''
    Ejercicio 4: Crear una imagen con el texto dado en cada bloque de la imagen original, 
    con el color promedio del bloque.
    
    Parámetros:
        - imagen_path: str, ruta de la imagen a procesar.
        - texto: lista de caracteres, el texto a dibujar en los bloques.
        - tam_bloque: int, tamaño de los bloques en los que se dividirá la imagen.
        
    Devuelve:
        - Guarda la imagen resultante en el directorio de trabajo.
    '''
    imagen = Image.open(imagen_path)
    imagen = imagen.convert("RGB")  
    ancho, alto = imagen.size

    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Fondo blanco
    draw = ImageDraw.Draw(imagen_pil)

    # Cargar la fuente con una M gordita y gruesa
    fuente = ImageFont.truetype("Fuentes/Roboto.ttf", tam_bloque)

    # Inicializar un índice para recorrer las letras del texto
    indice_letra = 0
    texto_len = len(texto)

    # Recorrer la imagen en bloques 
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen.crop((x, y, x + tam_bloque, y + tam_bloque))
            bloque_array = np.array(bloque)
            color_promedio = np.mean(bloque_array, axis=(0, 1)).astype(int)
            letra = texto[indice_letra % texto_len]  # Iteramos sobre el texto hasta llenar el ultimo bloque
            indice_letra += 1
            draw.text((x, y), letra, font=fuente, fill=tuple(color_promedio))

    imagen_pil.save("4_color_with_text.png") 
    print("Imagen guardada como 4_color_with_text.png")
    
    
def domino(imagen_path, fuente, tam_bloque=20):
    '''
    Ejercicio 5.1: Crear una imagen con las fichas de dominó asignadas según el tono de gris de cada bloque.

    Parámetros:
        - imagen_path: str, ruta de la imagen a procesar.
        - fuente: str, tipo de fuente ('blanco' o 'negro').
        - tam_bloque: int, tamaño de los bloques en los que se dividirá la imagen.

    Devuelve:
        - Guarda la imagen resultante en el directorio de trabajo con un nombre que indica la fuente usada.
    '''
    imagen = Image.open(imagen_path)
    ancho, alto = imagen.size

    imagen_gris = imagen.convert("L")  # Convertimos a escala de grises
    ancho, alto = imagen_gris.size

    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Fondo blanco
    draw = ImageDraw.Draw(imagen_pil)

    # Cargamos la fuente proporcionada por el usuario
    if fuente == "blanco":
        fuente_path = "Fuentes/DominoBlanco.ttf"
        nombre_salida = "5_domino_blanco.png"
    elif fuente == "negro":
        fuente_path = "Fuentes/DominoNegro.ttf"
        nombre_salida = "5_domino_negro.png"
    else:
        raise ValueError("Fuente no válida. Usa 'blanco' o 'negro'")

    fuente = ImageFont.truetype(fuente_path, tam_bloque)

    fichas = [
        "00", "01", "02", "03", "04", "05", "06",
        "10", "11", "12", "13", "14", "15", "16",
        "20", "21", "22", "23", "24", "25", "26",
        "30", "31", "32", "33", "34", "35", "36"
    ]

    # Recorremos la imagen en bloques de tamaño tam_bloque
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen_gris.crop((x, y, x + tam_bloque, y + tam_bloque))
            bloque_array = np.array(bloque)
            gris_promedio = int(np.mean(bloque_array))
            intervalo = gris_promedio // (256 // len(fichas))  
            ficha = fichas[intervalo]
            draw.text((x, y), ficha, font=fuente, fill=(0, 0, 0))

    imagen_pil.save(nombre_salida)
    print("Imagen guardada como 5_domino_blanco o 5_domino_negro")
    


def naipes(imagen_path, tam_bloque=20):
    '''
    Crear una imagen con los símbolos de naipes asignados según el tono de gris de cada bloque.

    Parámetros:
        - imagen_path: str, ruta de la imagen a procesar.
        - tam_bloque: int, tamaño de los bloques en los que se dividirá la imagen.

    Devuelve:
        - Guarda la imagen resultante en el directorio de trabajo.
    '''
    imagen = Image.open(imagen_path)
    ancho, alto = imagen.size

    imagen_gris = imagen.convert("L")  # Convertimos a escala de grises
    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Fondo blanco
    draw = ImageDraw.Draw(imagen_pil)

    try:
        fuente = ImageFont.truetype("Fuentes/Cartas.ttf", tam_bloque)
    except IOError:
        print("No se encontro la ruta especificada")
        return
    
    # Símbolos de naipes en función de la escala de grises
    simbolos = ["♠", "♥", "♦", "♣", "A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]

    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen_gris.crop((x, y, x + tam_bloque, y + tam_bloque))
            gris_promedio = int(np.mean(np.array(bloque)))

            # Asegurar que el índice no supere el tamaño de la lista
            indice = min(gris_promedio // (256 // len(simbolos)), len(simbolos) - 1)
            simbolo = simbolos[indice]
            draw.text((x, y), simbolo, font=fuente, fill=(0, 0, 0))

    imagen_pil.save("6_naipes.png")
    print("Imagen guardada como 6_naipes.png")

def main():
    imagen_de_prueba = "ejemplo.png"
    letra = "M"
    texto_p = "PROCESO DIGITAL DE IMAGENES 2025"

    letter_with_color(imagen_de_prueba, letra)
    letter_with_grayscale(imagen_de_prueba, letra)
    letters_bn(imagen_de_prueba)
    color_with_text(imagen_de_prueba, texto_p)
    domino(imagen_de_prueba,"blanco")
    domino(imagen_de_prueba,"negro")
    naipes("natu.png")


if __name__ == "__main__":
    main()
