import math
from PIL import Image, ImageDraw, ImageFont
'''
Script que aplica a una imagen los filtros:
- Semitonos
- Dados

Autor: López Diego Gabriela
Fecha: 22/Mar/25
Versión: 1.0
'''

def grey_scale(original_image, version):
    '''
    Funcion que convierte una imagen a escala de grises.
    Parametros:
        original_image: imagen a convertir
        version: versión del filtro a aplicar
    Retorna:
        grey_img: imagen en escala de grises
    '''
    if original_image:   
        original_image =  original_image.copy().convert("RGBA")   #Creamos una copia y la convertimos a RGBA
        grey_img = Image.new("RGBA", original_image.size) # Crear una nueva imagen en modo RGB para almacenar el resultado del filtro
        
        #Obtenemos los pixeles de las 2 imagenes anteriores
        pixels = original_image.load()
        grey_pixels = grey_img.load()
        
        #Iteramos sobre cada pixel de la imagen original 
        for i in range(original_image.width):
            for j in range(original_image.height): 
                r, g, b, a = pixels[i, j]   #Obtenemos los valores de cada canal RGBA
                grey = (r + g + b) // 3     #Calcular el promedio de los valores de los canales RGB

                if version == 2:
                    grey = int(r*0.299 + g*0.587 + b*0.114) # Calcular el promedio ponderado de los valores de los canales RGB
                grey_pixels[i, j] = (grey, grey, grey, a)  #Se asgina los nuevos valores gris (el canal a permanece igual)
         
        return grey_img
    
    
def get_average_color(image, x, y, width, height, version):  
    '''
    Funcion que obtiene el color promedio de una zona dentro de una imagen 
    Parámetros:
        - image: imagen a procesar
        - x, y: coordenadas de inicio de la zona
        - width, height: dimensiones de la zona
        - version: versión del filtro a aplicar
    Retorna:
        average_color: color promedio de la zona
    '''
    pixels = image.load()   #Carga los pixeles de la imagen
    total_r, total_g, total_b, count, a = 0, 0, 0, 0, 0    #Inicializa los contadores en cero 
    average_color = -1  

    if version == 1 or version == 2:
        #Recorremos la imagen por bloques 
        for i in range(x, min(x + width, image.width)):
            for j in range(y, min(y + height, image.height)):

                #Si la img esta en escala de grises 
                if version == 1:
                    grey = pixels[i, j][0] # Tomar el valor de gris (R=G=B)
                    a =  pixels[i, j][3]
                    total_g += grey
                else:
                    #En caso contrario, 
                    temp_r, temp_g, temp_b, a = pixels[i, j] #Obtenemos los valores de cada canal de la img original
                    total_r += temp_r   #Aumentamos los contadores de cada canal
                    total_g += temp_g
                    total_b += temp_b

                count += 1 #Aumentamos el contador total

        if count == 0:
            #No hay color promedio 
            average_color = 0
        elif version == 1:
            #Dividimos cada contador de cada canal entre el contador total (el canal A permanece igual)
            average_color = (total_g // count, total_g // count, total_g // count, a)
        else:
            #Dividimos cada contador de cada canal entre el contador total (el canal A permanece igual)
            average_color = (total_r // count, total_g // count, total_b // count, a)
    
    return average_color #Retornamos el color promedio encontrado en dicha region 


def generate_dice_face(value, square_length, background_color, dot_color):    
    '''
    Genera una imagen de una cara de un dado con el número de puntos especificado.
    Recibe el número de puntos en la cara del dado, el tamaño de los lados del recuadro,
    así como los colores de fondo y para los puntos.
    Parámetros:
        - value: número de puntos en la cara del dado
        - square_length: tamaño de los lados del recuadro
        - background_color: color de fondo
        - dot_color: color para los puntos
    Retorna:
        image: imagen de la cara del dado
    '''
    image = Image.new("RGBA", (square_length, square_length), background_color)
    draw = ImageDraw.Draw(image)

    # Coordenadas relativas de los puntos para cada cara del dado
    dot_positions = {
        1: [(0.5, 0.5)],
        2: [(0.25, 0.25), (0.75, 0.75)],
        3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
        4: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)],
        5: [(0.25, 0.25), (0.25, 0.75), (0.5, 0.5), (0.75, 0.25), (0.75, 0.75)],
        6: [(0.25, 0.25), (0.25, 0.5), (0.25, 0.75), (0.75, 0.25), (0.75, 0.5), (0.75, 0.75)]
    }

    diameter = square_length // 5  # Tamaño relativo de los puntos
    
    for x_factor, y_factor in dot_positions[value]:
        x0 = int((x_factor * square_length) - diameter // 2)
        y0 = int((y_factor * square_length) - diameter // 2)
        x1 = x0 + diameter
        y1 = y0 + diameter
        draw.ellipse([x0, y0, x1, y1], fill=dot_color)

    return image


def select_best_thumbnail(image_list, target_color, version):
    '''
    Función que nos permite elegir la miniatura más adecuada para reemplazar una zona
    de la imagen de referencia con base en su color promedio. 
    Parámetros:
        - image_list: lista de miniaturas
        - target_color: color promedio de la zona
        - version: versión del filtro a aplicar
    Retorna:
        best_thumbnail: miniatura más adecuada
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


def generate_dot(diameter, square_length, background_color, dot_color):
    '''
    Genera una imagen que consta de un ciculo al centro de un 
    cuadrado. Se peuden ajustar las dimensiones del círculo y el cuadro,
    también se pueden seleccionar los colores para el fondo y el círculo 
    
    Parámetros: 
        - diameter: diámetro del círculo
        - square_length: tamaño del cuadrado
        - background_color: color de fondo
        - dot_color: color del círculo
    Retorna:
        image: imagen con el círculo
    '''
    image = Image.new("RGBA", (square_length, square_length), background_color) 
    draw = ImageDraw.Draw(image)
    x0 = (square_length - diameter) // 2
    y0 = (square_length - diameter) // 2                #Generar el fondo y detectar su centro
    x1 = x0 + diameter
    y1 = y0 + diameter
    
    draw.ellipse([x0, y0, x1, y1], fill=dot_color)      #Trazar el círculo
    
    return image


def semitones(original_image, grid_size, background_color, dot_color):
    '''
    FILTRO SEMITONOS:
    Recorre la imagen original por sectores de un tamaño determinado y, de acuerdo al color gris
    promedio de cada sector, elige la miniatura con un círculo del tamaño adecuado para reemplazar
    dicho sector.
    '''
    if original_image:
        grey_image = grey_scale(original_image, 2)         
        result_image = Image.new("RGBA", original_image.size)
        
        
        max_diameter = grid_size 
        num_steps = grid_size         # Crear una lista de imágenes con círculos desde diámetro 0 hasta el máximo
        image_list = []               # posible, el ancho mismo del recuadro     

        for i in range(num_steps + 1):
            diameter = int(i * max_diameter / num_steps)
            dot_image = generate_dot(diameter, grid_size, background_color, dot_color)
            average_dot_grey = get_average_color(dot_image, 0, 0, dot_image.width, dot_image.height, 1)[0]
            dot_grey = (average_dot_grey, average_dot_grey, average_dot_grey)            
            image_list.append((dot_grey, dot_image)) 
            if diameter == max_diameter:
                break;     
        
        for i in range(0, original_image.width, grid_size):                    
            for j in range(0, original_image.height, grid_size):       #Generar el mosaico             
                block_width = min(grid_size, original_image.width - i)
                block_height = min(grid_size, original_image.height - j)                                         
                zone_grey = get_average_color(grey_image, i, j, block_width, block_height, 1)[0] 
                zone_color = (zone_grey, zone_grey, zone_grey,  255)          
                best_thumbnail = select_best_thumbnail(image_list, zone_color, 2)                    
                result_image.paste(best_thumbnail, (i, j))  

        return result_image


def dices_filter(original_image, grid_size, background_color, dot_color):  
    '''
    FILTRO DADO:
    Reemplaza regiones de la imagen con caras de dados basadas en el gris promedio.
    Recibe la imagen a procesar, el tamaño de las regiones a reemplazar, así como
    los colores para la construcción de las caras de dado.
    Parámetros:
        - original_image: imagen a procesar
        - grid_size: tamaño de las regiones a reemplazar
        - background_color: color de fondo
        - dot_color: color para los puntos
    Retorna:
        result_image: imagen con las regiones reemplazadas por caras de dado
    '''  
    if original_image:
        grey_image = grey_scale(original_image, 2)
        result_image = Image.new("RGBA", original_image.size)

        # Crear lista de imágenes con las 6 caras del dado
        dice_faces = []
        for i in range(1, 7):
            dice_image = generate_dice_face(i, grid_size, background_color, dot_color)
            average_grey = get_average_color(dice_image, 0, 0, dice_image.width, dice_image.height, 1)[0]
            dice_faces.append(((average_grey, average_grey, average_grey), dice_image))

        # Recorrer la imagen por bloques
        for i in range(0, original_image.width, grid_size):
            for j in range(0, original_image.height, grid_size):
                block_width = min(grid_size, original_image.width - i)
                block_height = min(grid_size, original_image.height - j)
                zone_grey = get_average_color(grey_image, i, j, block_width, block_height, 1)[0]
                zone_color = (zone_grey, zone_grey, zone_grey, 255)
                
                # Seleccionar la cara del dado más cercana en gris
                best_thumbnail = select_best_thumbnail(dice_faces, zone_color, 2)
                result_image.paste(best_thumbnail, (i, j))

        return result_image