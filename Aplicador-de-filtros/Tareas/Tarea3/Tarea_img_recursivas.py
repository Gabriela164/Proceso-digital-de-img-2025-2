from PIL import Image
import csv, ast, math 

"""
Script que genera una imagen de forma recursiva a partir de una imagen de referencia y una imagen de relleno.

Autor: Gabriela López Diego 
Fecha: 08/Marzo/25
Versión: 1.0
"""

def color_filter(image, color):
    """
    Aplica un filtro de color a una imagen.
    
    Parámetros: 
        image (PIL.Image): Imagen de entrada.
        color (tuple = R,G,B): Color de referencia en formato RGB
    
    Retorna:
        PIL.Image: Imagen con el filtro aplicado.
    """
    rgb_image = image.copy().convert('RGBA')  # Nos aseguramos de convertir la img en RGBA
    width, height = rgb_image.size            
    filter_r, filter_g, filter_b = color          # Obtenemos cada canal RGBA de la tupla que se paso como parametro 
    filtered_image = Image.new('RGBA', (width, height)) 
    original_pixels = rgb_image.load()        #Obtenemos lo pixeles de la imagen original
    filtered_pixels = filtered_image.load()   #y de la img nueva
    
    #Recorremos la imagen por pixel
    for i in range(width):
        for j in range(height):            
            original_r, original_g, original_b, original_a = original_pixels[i, j]  # Se obtienen los componentes RGB de cada pixel de la img original
            new_r = (original_r + filter_r) // 2   # Se mezclan los colores de cada canal (de la tupla color y de la img original)
            new_g = (original_g + filter_g) // 2  
            new_b = (original_b + filter_b) // 2          
            filtered_pixels[i, j] = (new_r, new_g, new_b, original_a)  # Se actualiza el píxel con el nuevo color
    
    return filtered_image    
                                       
           
def brightness_mod(temp_img, bright_pixels, factor):         
    """
    Modifica el brillo de los píxeles de una imagen.
    
    Parámetros:
        temp_img (PIL.Image): Imagen de entrada.
        bright_pixels (PixelAccess): Píxeles de la imagen.
        factor (float): Factor de ajuste de brillo.
    """
    
    #Recorremos cada pixel de la imagen dada
    for i in range(temp_img.width):
        for j in range(temp_img.height):
            r, g, b, a = bright_pixels[i, j]    # Se obtienen los componentes RGBA de cada píxel
            new_r = min(max(int(r * factor), 0), 255)   # Se ajusta el brillo de cada componente con el factor
            new_g = min(max(int(g * factor), 0), 255)
            new_b = min(max(int(b * factor), 0), 255)
            bright_pixels[i, j] = (new_r, new_g, new_b, a)  # Se actualiza el pixel con el nuevo brillo


def get_average_color(image, x, y, width, height):  
    """
    Obtiene el color promedio de una región de una imagen.
    
    Parámetros:
        image (PIL.Image): Imagen de entrada.
        x (int): Coordenada X de la zona.
        y (int): Coordenada Y de la zona.
        width (int): Ancho de la zona.
        height (int): Alto de la zona.
    
    Retorna:
        tuple: Color promedio en formato (R, G, B, A)
    """
    pixels = image.load()
    total_r, total_g, total_b, count, a = 0, 0, 0, 0, 0     # Contadores en cero para acumular los colores de cada canal
    
    #Recorremos por regiones, la imagen dada
    for i in range(x, min(x + width, image.width)):
        for j in range(y, min(y + height, image.height)):
            temp_r, temp_g, temp_b, a = pixels[i, j]   # Obtenemos los componentes RGBA de cada pixel de la region
            total_r += temp_r                          # Acumulan los valores de cada canal por separado en la zona
            total_g += temp_g
            total_b += temp_b
            count += 1                                # Cuenta cuantos pixeles hay en la zona

    if count == 0:
        #Si no hay pixeles analizados 
        return (0, 0, 0, 255)                         
    else:
        #Cada contador r,g,b lo dividimos entre el count obtenido (el canal a lo dejamos igual)
        return (total_r // count, total_g // count, total_b // count, a) # Se retorna el color promedio RGBA


def select_best_thumbnail(image_list, target_color):
    """
    Selecciona la miniatura más parecida a un color objetivo de una lista de miniaturas
    utilizando la formula de distancia euclidiana en el espacio RGB.
    
    Parámetros:
        image_list (list): Lista de miniaturas con sus colores RGBA asociados.
        target_color (tuple): Color objetivo en formato (R, G, B, A).
    
    Retorna:
        PIL.Image: Miniatura más adecuada.
    """
    right_index = 0   # Guardará el indice de la miniatura más adecuada al objetivo
    minimum_difference = float('inf')  # Inicializa la diferencia mínima como infinito
      
     #Se recorren las miniaturas y sus colores asociados
    for ind, (temp_color, image) in enumerate(image_list):          
        temp_r, temp_g, temp_b = temp_color                          #Se obtienen los componentes RGB del color de la miniatura
        target_r, target_g, target_b, target_a = target_color        #Se obtienen los componentes RGB del color objetivo
        temp_difference = math.sqrt((temp_r - target_r)**2 + (temp_g - target_g)**2 + (temp_b - target_b)**2 ) #Se calcula la distancia euclidiana entre los colores en el espacio RGB
        # (Entre más pequeña la diferencia, más parecidos son)
        
        # Se actualiza el índice de la miniatura con la menor diferencia
        if temp_difference < minimum_difference:                
            minimum_difference = temp_difference
            right_index = ind  # Se guarda el índice de la miniatura más parecida al color objetivo

    return image_list[right_index][1] # Se retorna la miniatura más adecuada


def recursive_image_generation(reference_image, filler_image, tile_width, tile_height):
    """
    Genera una nueva imagen recursiva de mosaicos a partir de una imagen de referencia y una imagen de relleno.

    La imagen de referencia se divide en bloques, y en cada bloque se selecciona la miniatura más adecuada 
    de la imagen de relleno, filtrada en varios colores, para crear una representación recursiva.

    Parámetros:
        reference_image: Imagen de referencia que se utiliza para calcular los colores promedio de cada bloque.
        filler_image: Imagen de relleno que se utiliza para generar los mosaicos
        tile_width: Ancho de cada mosaico 
        tile_height: Alto de cada mosaico 

    Retorna:
        PIL.Image: Imagen generada con mosaicos
    """
    if reference_image and filler_image:
        
        reference_image = reference_image.copy().convert('RGBA')
        filler_image = filler_image.copy().convert('RGBA')
        recursive_image = Image.new("RGBA", reference_image.size) 
        
        # Inicializamos listas para almacenar las miniaturas filtradas y los códigos de colores de la paleta
        image_list = []
        webpalette_rgb_codes = []

        # Abrimos y leemos el archivo CSV que contiene la paleta de colores para guardar los colores 
        with open('Tareas/Tarea3/CSV/WebPalette.csv', 'r') as csv_file_palette:
            reader = csv.DictReader(csv_file_palette)
            for row in reader:
                # Convertimos cada valor RGB en el archivo a una tupla y lo agregamos a la lista
                triplet = ast.literal_eval(row['rgb_values'])
                webpalette_rgb_codes.append(triplet)

        # Recorremos la lista de colores de la paleta y aplicamos cada filtro a la imagen de relleno (redimensionada)
        # y guardamos la miniatura resultante (para tener una lista de miniaturas con distintos colores)
        for i, color in enumerate(webpalette_rgb_codes):
            filtered_image = color_filter(filler_image.copy().resize((tile_width, tile_height), Image.Resampling.LANCZOS), color)
            image_list.append((color, filtered_image))  

        # Recorremos la imagen de referencia por bloques, de acuerdo con las dimensiones de los mosaicos
        for i in range(0, recursive_image.width, tile_width):
            for j in range(0, recursive_image.height, tile_height):
                
                # Obtenemos el ancho y la altura del bloque actual
                block_width = min(tile_width, recursive_image.width - i)
                block_height = min(tile_height, recursive_image.height - j)
                
                # Obtenemos el color promedio de la zona 
                zone_color = get_average_color(reference_image, i, j, block_width, block_height) 
                
                # Seleccionamos la miniatura más adecuada de la lista de miniaturas 
                best_thumbnail = select_best_thumbnail(image_list, zone_color)
                
                # Pegamos la miniatura seleccionada en la posición correspondiente del mosaico en la imagen nueva 
                recursive_image.paste(best_thumbnail, (i, j))

    return recursive_image
