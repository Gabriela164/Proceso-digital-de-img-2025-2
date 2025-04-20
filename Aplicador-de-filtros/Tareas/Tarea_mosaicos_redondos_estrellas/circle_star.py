import numpy as np
from PIL import Image

def coloring_shape(img, new_color):
    '''
    Funcion que rcolorea una imagen PNG blanca con fondo transparente a un nuevo color dado.
    (Se asume que es png con fondo transparente y blanco)
    
    Parámetros:
    - img: PIL.Image, imagen PNG (se asume que es blanca con fondo transparente) a colorear.
    - nuevo_color: tuple, color RGB (r, g, b) para recolorear la imagen.
    
    Retorna:
    - PIL.Image, imagen recoloreada.
    '''
    
    # Convertimos la imagen en RGBA y extraemos los valores de los píxeles
    img = img.convert("RGBA")
    pixels = np.array(img)
    r, g, b, a = pixels.T

    # Filtramos los píxeles que son blancos (255, 255, 255) y los reemplazamos por el nuevo color
    white_pixels = (r == 255) & (g == 255) & (b == 255)
    pixels[..., :-1][white_pixels.T] = new_color
    
    # Retornamos la imagen recoloreada y en objeto PIL
    return Image.fromarray(pixels)

def mosaics_with_shape(imagen, figura_path, tam_bloque, margen):
    """
    Crea una imagen mosaico usando una figura PNG recoloreada por bloque.
    
    Parámetros:
        - imagen: PIL.Image, imagen original.
        - figura_path: str, ruta del PNG de la figura (círculo o estrella).
        - tam_bloque: int, tamaño del bloque cuadrado.
        - margen: int, espacio entre los bordes del bloque y la figura.
    
    Retorna:
        - Imagen compuesta.
    """
    # Convertimos la imagen a RGB y obtenemos sus dimensiones
    imagen = imagen.convert("RGB")
    width, height = imagen.size

    # Convertimos la figura a RGBA y la redimensionamos    
    shape = Image.open(figura_path).convert("RGBA")
    shape = shape.resize((tam_bloque - 2 * margen, tam_bloque - 2 * margen))

    # Creamos una nueva imagen para el resultado con fondo blanco
    img_result = Image.new("RGB", (width, height), (255, 255, 255))

    # Recorremos la imagen original en bloques de tamaño tam_bloque
    for y in range(0, height, tam_bloque):
        for x in range(0, width, tam_bloque):
            bloque = imagen.crop((x, y, x + tam_bloque, y + tam_bloque)) # Extraemos el bloque actual
            bloque_array = np.array(bloque)   # Convertimos el bloque a un array de numpy
            average_color = np.mean(bloque_array, axis=(0, 1)).astype(int) # Calculamos el color promedio del bloque

            colored_figure = coloring_shape(shape, tuple(average_color)) # Coloramos la figura con el color promedio
            # Pegamos la figura recoloreada en la misma posicion de la region pero en la imagen nueva
            img_result.paste(colored_figure, (x + margen, y + margen), colored_figure) 

    return img_result
