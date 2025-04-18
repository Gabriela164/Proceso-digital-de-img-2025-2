from PIL import Image, ImageDraw
import random, math
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
         
        return grey_img #Retorna una imagen en escala de grises
    
    
def get_average_color(image, x, y, width, height, version):  
    '''
    Funcion para obtener el color promedio de una zona dentro de una imagen.
    '''
    pixels = image.load()   
    total_r, total_g, total_b, count, a = 0, 0, 0, 0, 0    
    average_color = -1

    if version == 1 or version == 2:
        #Iteramos en bloques sobre la imagen dada
        for i in range(x, min(x + width, image.width)):
            for j in range(y, min(y + height, image.height)):

                if version == 1:
                    #Si la imagen dada esta en escala de grises
                    grey = pixels[i, j][0] # Tomar el valor de gris (R=G=B)
                    a =  pixels[i, j][3]
                    total_g += grey
                else:
                    #En caso contrario,
                    temp_r, temp_g, temp_b, a = pixels[i, j]
                    total_r += temp_r # Aumentamos el contador para cada canal
                    total_g += temp_g
                    total_b += temp_b

                count += 1 # Aumentamos el contador

        if count == 0:
            average_color = 0
        elif version == 1:
            #Obtenemos el promedio. Cada contador de cada canal se divide entre el contador total y el canal A permanece igual. 
            average_color = (total_g // count, total_g // count, total_g // count, a)
        else:
            average_color = (total_r // count, total_g // count, total_b // count, a)
    
    #Devuelve el color promedio de una zona dentro de una imagen 
    return average_color


def select_best_thumbnail(image_list, target_color, version):
    '''
    Funcion que nos permite elegir la miniatura más adecuada para reemplazar una zona
    de la imagen de referencia con base en su color promedio.
    '''
    right_index = 0
    minimum_difference = float('inf')

    if version == 1:     
        interval_size = 255 / 30 
        target_color = target_color[0]       
        right_index = max(0, min(int(target_color / interval_size), 29))  #  Empleamos indexación para elegir el tono de
        best_thumbnail = image_list[right_index]         # gris promedio más idóneo   

    elif version == 2:        
        for ind, couple in enumerate(image_list):
            temp_r, temp_g, temp_b = couple[0]            # Se elige el tono cuya diferencia sea la menor
            target_r, target_g, target_b, target_a = target_color   # respecto del color promedio de la zona                    
            temp_difference = math.sqrt((temp_r - target_r)**2 + (temp_g - target_g)**2 + (temp_b - target_b)**2 )

            if temp_difference < minimum_difference:                
                minimum_difference = temp_difference
                right_index = ind 

        best_thumbnail_tuple = image_list[right_index]
        best_thumbnail = best_thumbnail_tuple[1] 

    return best_thumbnail


def random_dithering(reference_image): 
    '''
    Función que aplica dithering al azar 
    '''
    image_width, image_height = reference_image.size     #Se obtiene las dimensiones de la imagen de referencia 
    result_image = Image.new("RGBA", reference_image.size)  #Creamos una nueva imagen RGBA del mismo tamaño
    
    #Cargamos los pixeles de ambas imagenes
    result_pixels = result_image.load() 
    reference_pixels = reference_image.load()

    #Iteramos sobre cada pixel de la imagen de referencia
    for x in range(image_width):
        for y in range(image_height):                   
            r, g, b, a = reference_pixels[x, y]        # Obtenemos los valores de cada canal RGBA
            random_threshold = random.randint(0, 255)  # Genera un valor aleatorio para el umbral
            
            new_pixel = 255 if r > random_threshold else 0
            result_pixels[x, y] = (new_pixel, new_pixel, new_pixel, a)  #Asignamos el nuevo pixel 
    
    return result_image


def matrix_dithering(reference_image, matrix):
    '''
    Función que aplica dithering dada una matriz de umbral.
    '''
    image_width, image_height = reference_image.size
    result_image = Image.new("RGBA", reference_image.size) 
    result_pixels = result_image.load()
    reference_pixels = reference_image.load()    
    matrix_size = len(matrix)

    for x in range(image_width):
        for y in range(image_height): # Recorre la imagen
            r, g, b, a = reference_pixels[x, y]   
            scaled_pixel_value = r // 28           # Escalar el valor del pixel a un rango de 0 a 9
            matrix_value = matrix[y % matrix_size][x % matrix_size]  # Obtener el valor de la matriz en la posición correspondiente           
            
            if scaled_pixel_value < matrix_value:
                result_pixels[x, y] = (0, 0, 0, a)  # Lo convierte a negro
            else:
                result_pixels[x, y] = (255, 255, 255, a)  # Lo convierte en blanco
    
    return result_image
    
    
def floyd_steinberg_dithering(reference_image):    
    '''
    Aplica el algoritmo de dithering de Floyd-Steinberg a una imagen en escala de grises. 
    '''
    image_width, image_height = reference_image.size
    result_image = Image.new("RGBA", reference_image.size) #Preparación de la imagen
    reference_pixels = reference_image.load()  
    result_pixels = result_image.load()
    
    for x in range(image_width):
        for y in range(image_height):
            old_pixel, g, b, a = reference_pixels[x, y]    #Determinar el color del pixel
            new_pixel = 255 if old_pixel > 127 else 0      
            result_pixels[x, y] = (new_pixel, new_pixel, new_pixel, a)
            
            # Calcular el error de cuantización
            quant_error = old_pixel - new_pixel
            
            # Distribuir el error a los píxeles vecinos, si existen
            if y + 1 < image_height:  # Abajo
                r, g, b, a = reference_pixels[x, y + 1]
                error_color = int(min(max(r + quant_error * 7 / 16, 0), 255))
                reference_pixels[x, y + 1] = (error_color, error_color, error_color, a)
            
            if x + 1 < image_width and y - 1 >= 0:  # Derecha arriba
                r, g, b, a = reference_pixels[x + 1, y - 1]
                error_color = int(min(max(r + quant_error * 3 / 16, 0), 255))
                reference_pixels[x + 1, y - 1] = (error_color, error_color, error_color, a)
            
            if x + 1 < image_width:  # Derecha                
                r, g, b, a = reference_pixels[x + 1, y]
                error_color = int(min(max(r + quant_error * 5 / 16, 0), 255))
                reference_pixels[x + 1, y] = (error_color, error_color, error_color, a)
            
            if x + 1 < image_width and y + 1 < image_height:  # Derecha abajo
                r, g, b, a = reference_pixels[x + 1, y + 1]
                error_color = int(min(max(r + quant_error * 1 / 16, 0), 255))
                reference_pixels[x + 1, y + 1] = (error_color, error_color, error_color, a)
    
    return result_image


def fake_floyd_steinberg_dithering(image: Image.Image) -> Image.Image:
    '''
    Aplica el dithering Fake Floyd-Steinberg a una imagen en escala de grises.
    '''
    image = image.convert("L")  # Convertir a escala de grises
    img_array = np.array(image, dtype=np.float32)
    height, width = img_array.shape
    
    for y in range(height - 1):
        for x in range(width - 1):
            old_pixel = img_array[y, x]
            new_pixel = 255 if old_pixel > 127 else 0
            img_array[y, x] = new_pixel
            error = old_pixel - new_pixel
            
            # Distribuir el error según Fake Floyd-Steinberg
            img_array[y, x + 1] += error * (3 / 8)
            img_array[y + 1, x] += error * (3 / 8)
            img_array[y + 1, x + 1] += error * (2 / 8)
    
    img_array = np.clip(img_array, 0, 255)  # Asegurar valores válidos
    return Image.fromarray(img_array.astype(np.uint8))


def jarvis_judice_ninke_dithering(reference_image):
    '''
    Aplica el algoritmo de dithering de Jarvis, Judice, Ninke.
    '''
    image_width, image_height = reference_image.size
    result_image = Image.new("RGBA", reference_image.size)  # Crear una nueva imagen para el resultado
    reference_pixels = reference_image.load()  
    result_pixels = result_image.load()

    # Definir el patrón de dispersión de Jarvis, Judice, Ninke
    diffusion_matrix = [
        [0, 0, 7, 5, 3],
        [3, 5, 7, 0, 0],
        [1, 3, 5, 7, 0],
        [0, 1, 3, 5, 7]
    ]
    matrix_width = len(diffusion_matrix[0])
    matrix_height = len(diffusion_matrix)

    for x in range(image_width):
        for y in range(image_height):
            r, g, b, a = reference_pixels[x, y]    
            old_pixel = r  # Usamos el valor de rojo ya que la imagen está en escala de grises
            new_pixel = 255 if old_pixel > 127 else 0
            result_pixels[x, y] = (new_pixel, new_pixel, new_pixel, a)

            # Calcular el error de cuantización
            quant_error = old_pixel - new_pixel

            # Distribuir el error a los píxeles vecinos según el patrón de dispersión
            for dx in range(matrix_width):
                for dy in range(matrix_height):
                    nx = x + dx - 2  # Ajustar las posiciones con respecto al píxel actual
                    ny = y + dy - 2
                    if 0 <= nx < image_width and 0 <= ny < image_height:
                        r, g, b, a = reference_pixels[nx, ny]
                        error_color = int(min(max(r + quant_error * diffusion_matrix[dy][dx] / 48, 0), 255))
                        reference_pixels[nx, ny] = (error_color, error_color, error_color, a)

    return result_image


def save_image(image, filename):
    '''
    Método para guardar una imagen en disco.
    
    Parámetros:
    image: Imagen a guardar.
    filename: Nombre del archivo de salida.
    
    Retorna: None
    '''
    image.save(filename)
    print(f"Imagen guardada como: {filename}")
    
    
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
        
        grey_image = grey_scale(original_image, 2) # Primero lo convertimos a escala de grises
        result_image = None
        # Y le aplicamos el filtro según la versión dada
        if version == 1 :
            result_image = random_dithering(grey_image) 
        elif version == 2 :
            clustered_matrix = [
                [8, 3, 4],  
                [6, 1, 2],
                [7, 5, 9] 
            ]
            result_image = matrix_dithering(grey_image, clustered_matrix)
        elif version == 3 :
            dispersed_matrix = [
                [1, 7, 4],  
                [5, 8, 3],
                [6, 2, 9] 
            ]
            result_image = matrix_dithering(grey_image, dispersed_matrix)
        elif version == 4:
            matrix_2x2 = np.array([
                [4, 1],
                [2, 3]
            ])
            result_image = matrix_dithering(grey_image, matrix_2x2)
        elif version == 5:
            matrix_4x4 = np.array([
                [  16,  4,  13, 1],
                [ 8,  12, 5,  9],
                [  14, 2,  15,  3],
                [ 6,  10, 7,  11]
            ])
            result_image = matrix_dithering(grey_image, matrix_4x4)
        elif version == 6 :
            result_image = floyd_steinberg_dithering(grey_image)
        elif version == 7: 
            result_image = fake_floyd_steinberg_dithering(grey_image)
        elif version == 8:
            result_image = jarvis_judice_ninke_dithering(grey_image)
        return result_image
    
    
    
    
    
