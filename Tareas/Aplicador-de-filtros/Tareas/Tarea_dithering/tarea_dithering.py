from PIL import Image
import random
import numpy as np
'''
Script que aplica varios filtros a una imagen dada por el usuario. 

Lista de filtros
    1. Random dithering (al azar)
    2. Ordenado dithering (clustered) 
    3. Disperso dithering
    4. Disperso 2x2 mediante matriz de dithering
    5. Disperso 4x4 mediante matriz de dithering
    6. Floyd-Steinberg
    7. Fake Floyd-Steinberg  
    8. Jarvis, Judice, Ninke
    
Autor: Gabriela López Diego 
Fecha: 12/Marzo/2025 
'''

def grey_scale(original_image, version):
    '''
    Aplica dos versiones de la escala de grises a una imagen.  
    '''
    if original_image:   
        
        original_image =  original_image.copy().convert("RGBA")   
        grey_img = Image.new("RGBA", original_image.size) 
        
        #Obtenemos los pixeles de cada imagen
        pixels = original_image.load()
        grey_pixels = grey_img.load()
        
        #Recorremos cada pixel de la imagen original
        for i in range(original_image.width):
            for j in range(original_image.height):
                r, g, b, a = pixels[i, j] # Obtener los valores RGBA 
                grey = (r + g + b) // 3   # Obtenemos el gris promedio de cada pixel

                if version == 2: #Si es la version 2
                    grey = int(r*0.299 + g*0.587 + b*0.114)  # Multiplicamos cada canal por un factor para obtener un gris ponderado

                grey_pixels[i, j] = (grey, grey, grey, a) #Asignamos el nuevo valor a cada canal RGBA
         
        return grey_img 
    

def random_dithering(reference_image): 
    '''
    Función que aplica dithering al azar. 
    
    Parametros:
        - reference_image(PIL.image): Imagen que se le aplicará el dithering.
    Retorna:
        - result_image(PIL.image): Imagen resultante después de aplicar el dithering.
    '''
    image_width, image_height = reference_image.size       #Obtenemos las dimensiones de la imagen
    result_image = Image.new("RGBA", reference_image.size)  #Creamos una nueva imagen RGBA del mismo tamaño
    
    #Cargamos los pixeles de ambas imagenes(la imagen y la nueva imagen)
    result_pixels = result_image.load() 
    reference_pixels = reference_image.load()

    #Iteramos sobre cada pixel de la imagen 
    for x in range(image_width):
        for y in range(image_height):                   
            r, g, b, a = reference_pixels[x, y]        # Obtenemos los valores de cada canal RGBA
            random_threshold = random.randint(0, 255)  # Generamos un valor aleatorio para el umbral entre 0 y 255
            
            new_pixel = 255 if r > random_threshold else 0 
            result_pixels[x, y] = (new_pixel, new_pixel, new_pixel, a)  #Asignamos el nuevo pixel a cada canal RGB (el alfa permanece igual)
    
    return result_image


def matrix_dithering(reference_image, matrix):
    '''
    Función que aplica dithering dada una matriz de umbral.
    
    Parametros:
    - reference_image(PIL.image): Imagen que se le aplicará el dithering.
    - matrix(list): Matriz de umbral que se usará para el dithering (con valores del 0-9)
    
    Retorna:
    - result_image(PIL.image): Imagen resultante después de aplicar el dithering.
    '''
    
    #Obtenemos las dimensiones de la imagen y creamos una nueva imagen RGBA del mismo tamaño
    image_width, image_height = reference_image.size  
    result_image = Image.new("RGBA", reference_image.size) 
    
    #Cargamos los pixeles de ambas imagenes(la imagen y la nueva) 
    result_pixels = result_image.load()
    reference_pixels = reference_image.load()    
    
    matrix_size = len(matrix) 
    
    # Iteramos sobre cada pixel de la imagen
    for x in range(image_width):
        for y in range(image_height): 
            r, g, b, a = reference_pixels[x, y]     # Obtenemos los valores de cada canal RGBA 
            
            scaled_pixel_value = r // 28           # Reducimos el valor del pixel del canal rojo a un rango de 0 a 9 
            matrix_value = matrix[y % matrix_size][x % matrix_size]  # Obtenemos el valor correspondiente en la matriz umbral usando las coordenadas del pixel        
            
            # Comparamos el valor del pixel escalado con el valor de la matriz
            if scaled_pixel_value < matrix_value:
                result_pixels[x, y] = (0, 0, 0, a)  # Si es menor, lo convierte a negro
            else:
                result_pixels[x, y] = (255, 255, 255, a)  # Si es mayor, lo convierte en blanco
    
    return result_image
    
    

def floyd_steinberg_dithering(reference_image):
    '''
    Aplica el algoritmo de dithering de Floyd-Steinberg a una imagen en escala de grises. 
    [    ][ x  ][7/16]
    [3/16][5/16][1/16]

    Parámetros:
    - reference_image (PIL.Image): Imagen que se le aplicará el dithering.
    
    Retorna:
    - result_image (PIL.Image): Imagen resultante después de aplicar el dithering Floyd-Steinberg.
    '''
    
    # Obtenemos las dimensiones de la imagen y creamos una nueva imagen RGBA del mismo tamaño
    image_width, image_height = reference_image.size
    result_image = Image.new("RGBA", reference_image.size)  # para guardar el resultado
    
    # Cargamos los píxeles de la imagen original y la nueva
    reference_pixels = reference_image.load()  
    result_pixels = result_image.load()

    # Iteramos sobre cada píxel de la imagen
    for y in range(image_height):
        for x in range(image_width):
            r, g, b, a = reference_pixels[x, y]  # Obtenemos los valores de cada canal RGBA

            # En una imagen en escala de grises, r, g, b son iguales, tomamos solo 1
            old_pixel = r  
            new_pixel = 255 if old_pixel > 127 else 0  # Cuantización binaria
            result_pixels[x, y] = (new_pixel, new_pixel, new_pixel, a)
            
            # Calcular el error de cuantización
            quant_error = old_pixel - new_pixel

            # Distribuimos el error a los píxeles vecinos
            def distribute_error(nx, ny, factor):
                # Verificamos que los píxeles estén dentro de los límites de la imagen
                if 0 <= nx < image_width and 0 <= ny < image_height:
                    r, g, b, a = reference_pixels[nx, ny]
                    # Aplicamos el error de cuantización a los píxeles vecinos
                    new_val = int(min(max(r + quant_error * factor, 0), 255))
                    # Asignamos el nuevo valor en cada canal del píxel vecino
                    reference_pixels[nx, ny] = (new_val, new_val, new_val, a)

            distribute_error(x + 1, y,     7 / 16)  # Derecha
            distribute_error(x - 1, y + 1, 3 / 16)  # Abajo izquierda
            distribute_error(x,     y + 1, 5 / 16)  # Abajo
            distribute_error(x + 1, y + 1, 1 / 16)  # Abajo derecha

    return result_image


def fake_floyd_steinberg_dithering(reference_image):
    '''
    Aplica una versión simplificada (Fake) del algoritmo de dithering de Floyd-Steinberg.
    En lugar de distribuir el error a múltiples píxeles, se distribuye SOLO A 1 píxel vecino (a la derecha).
    
    Parámetros:
    - reference_image (PIL.Image): Imagen que se le aplicará el dithering.
    
    Retorna:
    - result_image (PIL.Image): Imagen resultante después de aplicar el dithering Fake Floyd-Steinberg.
    '''
    
    # Obtenemos las dimensiones de la imagen y creamos una nueva imagen RGBA del mismo tamaño
    image_width, image_height = reference_image.size
    result_image = Image.new("RGBA", reference_image.size)  # para guardar el resultado
    
    # Cargamos los píxeles de la imagen original y la nueva
    reference_pixels = reference_image.load()  
    result_pixels = result_image.load()

    # Iteramos sobre cada píxel de la imagen
    for y in range(image_height):
        for x in range(image_width):
            r, g, b, a = reference_pixels[x, y]  # Obtenemos los valores de cada canal RGBA

            # En una imagen en escala de grises, r, g, b deberían ser iguales, tomamos uno solo
            old_pixel = r  
            new_pixel = 255 if old_pixel > 127 else 0  # Cuantización binaria
            result_pixels[x, y] = (new_pixel, new_pixel, new_pixel, a)
            
            # Calcular el error de cuantización
            quant_error = old_pixel - new_pixel

            # Distribuir el error al píxel de la derecha (en lugar de a varios vecinos)
            if x + 1 < image_width:  # Verificamos que el píxel derecho esté dentro de los límites
                r, g, b, a = reference_pixels[x + 1, y]
                new_val = int(min(max(r + quant_error, 0), 255))
                reference_pixels[x + 1, y] = (new_val, new_val, new_val, a)

    return result_image


def jarvis_judice_ninke_dithering(reference_image):
    '''
    Aplica el algoritmo original de Jarvis, Judice y Ninke (JJN).
    '''
    # Convertimos la imagen a escala de grises y luego a RGBA
    reference_image = reference_image.convert("L").convert("RGBA")
    
    # Obtenemos las dimensiones de la imagen y creamos una nueva imagen RGBA del mismo tamaño
    image_width, image_height = reference_image.size
    result_image = Image.new("RGBA", reference_image.size)

    # Cargamos los píxeles de la imagen original y la nueva
    reference_pixels = reference_image.load()
    result_pixels = result_image.load()

    # Matriz de difusión de JJN
    diffusion_matrix = [
        [0, 0, 0, 7, 5],
        [3, 5, 7, 5, 3],
        [1, 3, 5, 3, 1]
    ]
    matrix_height = len(diffusion_matrix)
    matrix_width = len(diffusion_matrix[0])

    # Iteramos sobre cada píxel de la imagen
    for y in range(image_height):
        for x in range(image_width):
            r, g, b, a = reference_pixels[x, y]
            old_pixel = r  # ya es gris
            new_pixel = 255 if old_pixel > 127 else 0
            # asignamos el nuevo valor al píxel resultante y en la imagen nueva
            result_pixels[x, y] = (new_pixel, new_pixel, new_pixel, a)
            
            # Calcular el error de cuantización
            quant_error = old_pixel - new_pixel

            # Distribuir el error según la matriz de JJN
            for dy in range(matrix_height):
                for dx in range(matrix_width):
                    # Obtenemos el peso de la matriz de difusión (cuánto del error de cuantización se va a distribuir)
                    weight = diffusion_matrix[dy][dx]
                    
                    if weight == 0: # si el peso es cero, no hacemos nada
                        continue

                    # Alineamos el pixel con el centro de la matriz
                    nx = x + dx - 2  # desplazamiento horizontal (centro en el tercer valor)
                    ny = y + dy      # desplazamiento vertical (solo hacia abajo)

                    # Verificamos que el píxel esté dentro de los límites de la imagen
                    if 0 <= nx < image_width and 0 <= ny < image_height:
                        r2, g2, b2, a2 = reference_pixels[nx, ny]
                        # Aplicamos el error de cuantización al píxel vecino
                        new_value = int(min(max(r2 + quant_error * weight / 48, 0), 255))
                        # Asignamos el nuevo valor en cada canal del píxel vecino y alfa lo mantenemos igual
                        reference_pixels[nx, ny] = (new_value, new_value, new_value, a2)

    return result_image

    
def dithering_version(original_image, version):
    '''
    Selecciona el tipo de dithering a aplicar basado en una versión específica.
    Convierte la imagen original a escala de grises antes de aplicar el algoritmo de dithering
    correspondiente (aleatorio, con matriz dispersa o agrupada, o Floyd-Steinberg).
    Opcion 1: Random dithering
    Opcion 2: Clustered dithering
    Opcion 3: Dispersed dithering
    Opcion 4; Dispersed 2x2 dithering
    Opcion 5: Dispersed 4x4 dithering
    Opcion 6: Floyd-Steinberg dithering
    Opcion 7: Fake Floyd-Steinberg dithering
    Opción 8: Jarvis, Judice, Ninke dithering
    '''
    if original_image:
        
        grey_image = grey_scale(original_image, 2) # Nos aseguramos que la imagen esté en escala de grises
        result_image = None   # Creamos una variable para guardar la imagen resultante
        # Y le aplicamos el filtro según la versión dada
        if version == 1 :
            # Aplicamos el dithering aleatorio
            result_image = random_dithering(grey_image) 
        elif version == 2 :
            clustered_matrix = [
                [8, 3, 4],  
                [6, 1, 2],
                [7, 5, 9] 
            ]
            # Aplicamos el dithering ordenado 
            result_image = matrix_dithering(grey_image, clustered_matrix)
        elif version == 3 :
            dispersed_matrix = [
                [1, 7, 4],  
                [5, 8, 3],
                [6, 2, 9] 
            ]
            # Aplicamos el dithering disperso
            result_image = matrix_dithering(grey_image, dispersed_matrix)
        elif version == 4:
            matrix_2x2 = np.array([
                [4, 1],
                [2, 3]
            ])
            # Aplicamos el dithering disperso 2x2
            result_image = matrix_dithering(grey_image, matrix_2x2)
        elif version == 5:
            matrix_4x4 = np.array([
                [  16,  4,  13, 1],
                [ 8,  12, 5,  9],
                [  14, 2,  15,  3],
                [ 6,  10, 7,  11]
            ])
            # Aplicamos el dithering disperso 4x4
            result_image = matrix_dithering(grey_image, matrix_4x4)
        elif version == 6 :
            # Aplicamos el dithering de Floyd-Steinberg
            result_image = floyd_steinberg_dithering(grey_image)
        elif version == 7: 
            # Aplicamos el dithering de Floyd-Steinberg falso
            result_image = fake_floyd_steinberg_dithering(grey_image)
        elif version == 8:
            # Aplicamos el dithering de Jarvis, Judice y Ninke
            result_image = jarvis_judice_ninke_dithering(grey_image)
        return result_image
    
    
    
    
    
