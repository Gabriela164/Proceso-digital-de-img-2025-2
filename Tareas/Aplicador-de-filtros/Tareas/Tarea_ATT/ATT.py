from PIL import Image, ImageOps
import math
'''
Tarea filtro ATT

Descripción: Dada una imagen, aplica un filtro de alto contraste y un filtro de escala de grises ponderado.
Luego, genera una imagen con franjas horizontales de alto contraste en un fondo blanco. De esta manera, 
se simula un efecto de "filtro" del logo AT&T

Autor: Gabriela López Diego 
No. de cuenta: 318243485
Fecha: 19 de Abril del 2025
'''

# Utilizamos los filtros de la tarea 1 (gris ponderado y alto contraste)
def filtro_gris_ponderado(imagen):
    '''
    Convierte una imagen a blanco y negro usando un promedio ponderado (.30*r + .70*g + .10*b) 
    Le damos más importancia al canal verde (Green)

    Parámetros:
    1. imagen : Imagen de entrada

    Devuelve:
    1. Imagen en blanco y negro (escala de grises)
    '''
    #Nos aseguramos que este en formato RGBA
    imagen = imagen.convert("RGBA")  
    ancho, altura = imagen.size
    nueva_imagen = imagen.copy()

    #Recorremos cada pixel de la imagen 
    for x in range(ancho):
        for y in range(altura):
            r, g, b, a = imagen.getpixel((x, y))
            gris = int(.30 * r + .70 * g + .10 * b)   #Aplicamos un peso distinto a cada canal (rojo 30%, verde 70%, azul 10%)
            nueva_imagen.putpixel((x, y), (gris,gris,gris,a))
    return nueva_imagen


def filtro_alto_contraste(imagen):
    '''
    Aplica un filtro de alto contraste, convirtiendo los píxeles a blanco o negro según su intensidad.

    Parámetros:
    1. Imagen: Imagen de entrada para plicar el filtro. 
    
    Devuelve:
    1. Imagen con alto contraste.
    '''
    imagen = imagen.convert("RGBA")  
    ancho, altura = imagen.size
    nueva_imagen = imagen.copy()

    #Recorremos cada pixel de la imagen 
    for x in range(ancho):
        for y in range(altura):
            r, g, b, a = imagen.getpixel((x, y))
            # Calcular el valor de gris (promedio ponderado estandar)
            gris = int(0.299 * r + 0.587 * g + 0.114 * b)
            # Si el valor de gris es más claro que 128 se vuelve blanco(255,255,255) sino se vuelve negro (0,0,0)
            nuevo_color = (255, 255, 255, a) if gris > 128 else (0, 0, 0, a)
            nueva_imagen.putpixel((x, y), nuevo_color) # Aplicamos el nuevo color al pixel

    return nueva_imagen


def filter_att(image, stripe_thickness=4):
    '''
    Aplica un filtro visual inspirado en el logo de AT&T, creando franjas horizontales curvas
    sobre la imagen con un efecto de alto contraste en escala de grises.

    Parámetros:
    - image (PIL.Image): Imagen a la que se le aplicará el filtro.
    - stripe_thickness (int): Grosor de cada franja horizontal (en píxeles).

    Retorna:
    - result_image (PIL.Image): Imagen resultante con el filtro aplicado.
    '''

    # Creamos una copia y le aplicamos el filtro de gris ponderado y alto contraste
    image = image.copy()
    gray_image = filtro_gris_ponderado(image)
    high_contrast_image = filtro_alto_contraste(gray_image)

    # Creamos una nueva imagen del mismo tamaño con fondo blanco y canal alfa (RGBA)
    result_image = Image.new("RGBA", image.size, (255, 255, 255, 255))

    # Obtenemos las dimensiones y centro de la imagen
    width, height = image.size
    center_x = width // 2
    center_y = height // 2

    # Calculamos el radio máximo del círculo en el cual se aplicarán las franjas
    # Esto evita que las franjas se dibujen fuera del área de la imagen
    max_radius = int(min(width, height) // 2 * 0.95)

    # Recorremos la imagen verticalmente, de dos franjas en dos (una sí, una no)
    for y in range(0, height, stripe_thickness * 2):
        # Definimos el inicio y fin de la franja
        stripe_start = y  
        stripe_end = min(y + stripe_thickness, height)  

        # Calcular la distancia vertical del centro de la franja al centro de la imagen
        vertical_distance = abs(y + stripe_thickness // 2 - center_y)

        # Si la franja está dentro del círculo definido, se calcula el ancho horizontal
        if vertical_distance < max_radius:
            # Teorema de Pitágoras para obtener el "ancho medio" de la franja
            half_width = int(math.sqrt(max_radius ** 2 - vertical_distance ** 2))
        else:
            # Si la franja está fuera del círculo, se salta
            continue

        # Determinar los límites horizontales de la franja, centrada horizontalmente
        start_x = max(0, center_x - half_width)
        end_x = min(width, center_x + half_width)

        # Rellenar los píxeles dentro de la franja con los valores de la imagen procesada
        for yy in range(stripe_start, stripe_end):
            for x in range(start_x, end_x):
                pixel = high_contrast_image.getpixel((x, yy))
                result_image.putpixel((x, yy), pixel)

    return result_image

