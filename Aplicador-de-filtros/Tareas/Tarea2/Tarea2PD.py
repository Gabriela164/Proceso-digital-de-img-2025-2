'''
PROCESO DIGITAL DE IMAGENES 2025-2

Tarea 2: Sopa de letras. 

Alumna: Gabriela López Diego 
No. de cuenta: 318243485 
Fecha: Febrero 2025
'''
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def letter_with_color(imagen, letra, tam_bloque=15):  
    '''
    Ejercicio 1: Crear una imagen con la letra "M" en cada bloque de la imagen original, con el color promedio del bloque.
    
    Parámetros:
        - imagen: PIL.Image, imagen a procesar.
        - letra: str, letra a dibujar en cada bloque.
        - tam_bloque: int, tamaño de los bloques en los que se dividirá la imagen.
        
    Devuelve:
        - Imagen procesada con las letras.
    '''
    imagen = imagen.convert("RGB")  
    ancho, alto = imagen.size

    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Nueva imagen en blanco del mismo tamaño que la original 
    draw = ImageDraw.Draw(imagen_pil) # Creamos un objeto draw para dibuhar texto o formas en imagen_pil
    fuente = ImageFont.truetype("Tareas/Tarea2/Fuentes/Roboto.ttf", tam_bloque) # Cargamos la fuente con M de tamaño igual al bloque 

    # Recorremos la imagen en bloques de tamaño tam_bloque
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen.crop((x, y, x + tam_bloque, y + tam_bloque)) # Extraemos el bloque actual (area rectangular)
            bloque_array = np.array(bloque)  # Convertimos el bloque a un array de NumPy para poder calcular el color promedio (canales RGB)
            color_promedio = np.mean(bloque_array, axis=(0, 1)).astype(int) # Promediamos los valores de cada canal por separado (R, G, B) del bloque por ej. [127, 126, 150]
            draw.text((x, y), letra, font=fuente, fill=tuple(color_promedio)) # Esta línea dibuja la letra (M,etc) en el bloque usando el color promedio encontrado

    return imagen_pil


def letter_with_grayscale(imagen, letra, tam_bloque=15):  
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
    imagen = imagen.convert("RGB")  
    ancho, alto = imagen.size

    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Nueva imagen en blanco del mismo tamaño que la original
    draw = ImageDraw.Draw(imagen_pil)                              # Creamos un objeto draw para dibujar texto o formas en imagen_pil

    # Cargar la fuente con una M de tamaño igual al bloque
    fuente = ImageFont.truetype("Tareas/Tarea2/Fuentes/Roboto.ttf", tam_bloque)

    # Recorrer la imagen en bloques de tamaño tam_bloque
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen.crop((x, y, x + tam_bloque, y + tam_bloque))   # Extraer el bloque actual (area rectangular)
            bloque_array = np.array(bloque)                                # Convertir el bloque a un array de NumPy para poder calcular el color promedio (canales RGB)
            gris_promedio = np.mean(bloque_array @ [0.2989, 0.5870, 0.1140])  # Convertimos cada píxel RGB del bloque a escala de grises con una formula ponderada 
            #y luego calculamos el promedio de todos los valores de gris del bloque
            gris_promedio = int(gris_promedio)   
            draw.text((x, y), letra, font=fuente, fill=(gris_promedio, gris_promedio, gris_promedio)) # Esta línea dibuja la letra (M,etc) en el bloque usando el color promedio en escala de grises encontrado

    return imagen_pil
    
    
def letters_bn(imagen, tam_bloque=15):
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
    
    imagen = imagen.convert("RGB") 
    ancho, alto = imagen.size

    imagen_new = Image.new("RGB", (ancho, alto), (250, 250, 250))  # Nueva imagen en gris del mismo tamaño que la original 
    draw = ImageDraw.Draw(imagen_new)                              # Creamos un objeto draw para dibujar texto o formas en imagen_pil

    # Cargar la fuente con una M del tamaño tam_bloque
    fuente = ImageFont.truetype("Tareas/Tarea2/Fuentes/Roboto.ttf", tam_bloque)
    
    # Determinamos cuanto representa en la escala de grises cada letra
    intervalo_gris = (256 // len(letras)) # Dividimos el rango de gris promedio en intervalos para seleccionar la letra correspondiente
    

    # Recorremos la imagen en bloques de tamaño tam_bloque
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen.crop((x, y, x + tam_bloque, y + tam_bloque))    # Extraer el bloque actual (area rectangular)
            bloque_array = np.array(bloque)                                # Convertimos el bloque a un array de NumPy para poder calcular el color promedio (canales RGB)
            gris_promedio = np.mean(bloque_array @ [0.2989, 0.5870, 0.1140])   # Convertimos cada píxel RGB del bloque a escala de grises con una formula ponderada 
            #y luego calculamos el promedio de todos los valores de gris del bloque
            gris_promedio = int(gris_promedio)
            intervalo = gris_promedio // intervalo_gris # Determinamos que letra se ajusta al gris promedio
            letra = letras[intervalo]               
            draw.text((x, y), letra, font=fuente, fill=(0, 0, 0))  # Dibujamos la linea de texto en la imagen nueva usando la letra correspondiente al gris promedio y en color negro 

    return imagen_new


def color_with_text(imagen, texto, tam_bloque=15):
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
    imagen = imagen.convert("RGB")  
    ancho, alto = imagen.size

    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Nueva imagen con fondo blanco 
    draw = ImageDraw.Draw(imagen_pil)                              # Creamos un objeto draw para dibujar texto o formas en imagen_pil

    # Cargar la fuente con una M de tamaño tam_bloque
    fuente = ImageFont.truetype("Tareas/Tarea2/Fuentes/Roboto.ttf", tam_bloque)

    # Inicializar un indice para recorrer las letras del texto
    indice_letra = 0
    texto_len = len(texto)

    # Recorremos la imagen en bloques de tamaño tam_bloque
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen.crop((x, y, x + tam_bloque, y + tam_bloque)) # Extraer el bloque actual (area rectangular)
            bloque_array = np.array(bloque)                              # Convertimos el bloque a un array de NumPy para poder calcular el color promedio (canales RGB)
            color_promedio = np.mean(bloque_array, axis=(0, 1)).astype(int)   # Promediamos los valores de cada canal por separado (R, G, B) del bloque     
            letra = texto[indice_letra % texto_len]  # Tomamos la letra correspondiente al índice actual 
            indice_letra += 1  # Aumentamos el índice para la siguiente letra
            draw.text((x, y), letra, font=fuente, fill=tuple(color_promedio)) # Dibujamos la letra particular en el bloque usando el color promedio encontrado

    return imagen_pil
    
    
def domino(imagen, fuente, tam_bloque=20):
    '''
    Ejercicio 5.1: Crear una imagen con las fichas de dominó asignadas según el tono de gris de cada bloque.

    Parámetros:
        - imagen_path: str, ruta de la imagen a procesar.
        - fuente: str, tipo de fuente ('blanco' o 'negro').
        - tam_bloque: int, tamaño de los bloques en los que se dividirá la imagen.

    Devuelve:
        - Guarda la imagen resultante en el directorio de trabajo con un nombre que indica la fuente usada.
    '''
    ancho, alto = imagen.size

    imagen_gris = imagen.convert("L")  # Convertimos a escala de grises
    ancho, alto = imagen_gris.size

    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Nueva imagen con fondo blanco 
    draw = ImageDraw.Draw(imagen_pil)

    # Cargamos la fuente proporcionada por el usuario
    if fuente == "blanco":
        fuente_path = "Tareas/Tarea2/Fuentes/DominoBlanco.ttf"
        nombre_salida = "5_domino_blanco.png"               
    elif fuente == "negro":
        fuente_path = "Tareas/Tarea2/Fuentes/DominoNegro.ttf"
        nombre_salida = "5_domino_negro.png"
    else:
        raise ValueError("Fuente no válida. Usa 'blanco' o 'negro'")

    fuente = ImageFont.truetype(fuente_path, tam_bloque) # Cargamos la fuente con el tamaño de tam_bloque

    # Cada ficha representa una pieza de domino 
    fichas = [
        "00", "01", "02", "03", "04", "05", "06",
        "10", "11", "12", "13", "14", "15", "16",
        "20", "21", "22", "23", "24", "25", "26",
        "30", "31", "32", "33", "34", "35", "36"
    ]

    # Recorremos la imagen en bloques de tamaño tam_bloque
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen_gris.crop((x, y, x + tam_bloque, y + tam_bloque))  #Extraemos el bloque actual 
            bloque_array = np.array(bloque)                                    #Lo convertimos a un arreglo con Numpy
            gris_promedio = int(np.mean(bloque_array))                         #Obtenemos el gris promedio de esa area 
            intervalo = min(max(gris_promedio // (256 // len(fichas)), 0), len(fichas) - 1)  
            ficha = fichas[intervalo]            #Seleccionamos la ficha adecuada
            draw.text((x, y), ficha, font=fuente, fill=(0, 0, 0))     #Dibujamos el domino en el bloque con relleno negro 

    return imagen_pil
    


def naipes(imagen, tam_bloque=20):
    '''
    Ejercicio 6. Crear una imagen con los símbolos de naipes asignados según el tono de gris de cada bloque.

    Parámetros:
        - imagen_path: str, ruta de la imagen a procesar.
        - tam_bloque: int, tamaño de los bloques en los que se dividirá la imagen.

    Devuelve:
        - Guarda la imagen resultante en el directorio de trabajo.
    '''
    ancho, alto = imagen.size

    imagen_gris = imagen.convert("L")  # Convertimos a escala de grises
    imagen_pil = Image.new("RGB", (ancho, alto), (255, 255, 255))  # Nueva imagen con fondo blanco 
    draw = ImageDraw.Draw(imagen_pil)   # Creamos un objeto draw para dibujar texto o formas en imagen_pil

    try:
        #Abrimos la fuente del tamaño tam_bloque
        fuente = ImageFont.truetype("Tareas/Tarea2/Fuentes/Cartas.ttf", tam_bloque)
    except IOError:
        print("No se encontro la ruta especificada")
        return
    
    # Simbolos de naipes en función de la escala de grises
    simbolos = ["♠", "♥", "♦", "♣", "A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]

    #Recorremos la imagen en tamaños de bloque tam_bloque
    for y in range(0, alto, tam_bloque):
        for x in range(0, ancho, tam_bloque):
            bloque = imagen_gris.crop((x, y, x + tam_bloque, y + tam_bloque))   # Extraemos el bloque actual
            gris_promedio = int(np.mean(np.array(bloque)))                      # Lo convertimos a un arreglo Numpy y obtenemos el color gris promedio

            # Asegurar que el índice no supere el tamaño de la lista
            indice = min(gris_promedio // (256 // len(simbolos)), len(simbolos) - 1)
            simbolo = simbolos[indice]   #Seleccionamos el simbolo que más se adecue al gris promedio encontrado
            draw.text((x, y), simbolo, font=fuente, fill=(0, 0, 0))   #Dibujamos el simbolo con la fuente cargada y de relleno color negro 

    return imagen_pil




