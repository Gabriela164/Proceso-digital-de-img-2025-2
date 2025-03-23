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
        color (tuple): Color de referencia en formato (R, G, B).
    
    Retorna:
        PIL.Image: Imagen con el filtro aplicado.
    """
    rgb_image = image.copy().convert('RGBA')  # La imagen se convierte a RGBA
    width, height = rgb_image.size            
    filter_r, filter_g, filter_b = color          # Se obtienen los componentes RGB del color de referencia
    filtered_image = Image.new('RGBA', (width, height))
    original_pixels = rgb_image.load()
    filtered_pixels = filtered_image.load()    
    
    for i in range(width):
        for j in range(height):            
            original_r, original_g, original_b, original_a = original_pixels[i, j]  # Se obtienen los componentes RGB de un píxel
            new_r = (original_r + filter_r) // 2   # Se mezclan los colores
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
    for i in range(temp_img.width):
        for j in range(temp_img.height):
            r, g, b, a = bright_pixels[i, j]    # Se obtienen los componentes RGB de un píxel
            new_r = min(max(int(r * factor), 0), 255)   # Se ajusta el brillo de cada componente con el factor
            new_g = min(max(int(g * factor), 0), 255)
            new_b = min(max(int(b * factor), 0), 255)
            bright_pixels[i, j] = (new_r, new_g, new_b, a)  # Se actualiza el píxel con el nuevo brillo


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
        tuple: Color promedio en formato (R, G, B, A).
    """
    pixels = image.load()
    total_r, total_g, total_b, count, a = 0, 0, 0, 0, 0     # Inicialización de variables
    
    for i in range(x, min(x + width, image.width)):
        for j in range(y, min(y + height, image.height)):
            temp_r, temp_g, temp_b, a = pixels[i, j]   # Se obtienen los componentes RGB de un píxel
            total_r += temp_r                          # Se suman los componentes RGB
            total_g += temp_g
            total_b += temp_b
            count += 1                                # Se incrementa el contador de píxeles

    if count == 0:
        return (0, 0, 0, 255)                         
    else:
        return (total_r // count, total_g // count, total_b // count, a) # Se retorna el color promedio


def select_best_thumbnail(image_list, target_color):
    """
    Selecciona la miniatura más parecida a un color objetivo.
    
    Parámetros:
        image_list (list): Lista de miniaturas con sus colores asociados.
        target_color (tuple): Color objetivo en formato (R, G, B, A).
    
    Retorna:
        PIL.Image: Miniatura más adecuada.
    """
    right_index = 0
    minimum_difference = float('inf')
      
    for ind, (temp_color, image) in enumerate(image_list):           #Se recorren las miniaturas y sus colores asociados
        temp_r, temp_g, temp_b = temp_color                          #Se obtienen los componentes RGB del color de la miniatura
        target_r, target_g, target_b, target_a = target_color        #Se obtienen los componentes RGB del color objetivo
        temp_difference = math.sqrt((temp_r - target_r)**2 + (temp_g - target_g)**2 + (temp_b - target_b)**2 ) #Se calcula la diferencia entre los colores

        if temp_difference < minimum_difference:           # Se actualiza el índice de la miniatura con la menor diferencia     
            minimum_difference = temp_difference
            right_index = ind 

    return image_list[right_index][1]               # Se retorna la miniatura más adecuada


def recursive_image_generation(reference_image, filler_image, tile_width, tile_height):    
    """
    Genera una imagen de forma recursiva utilizando una imagen de referencia y una de relleno.
    
    Parámetros:
        reference_image (PIL.Image): Imagen de referencia.
        filler_image (PIL.Image): Imagen de relleno.
        tile_width (int): Ancho de cada mosaico.
        tile_height (int): Alto de cada mosaico.
    
    Retorna:
        PIL.Image: Imagen generada con mosaicos.
    """
    if reference_image and filler_image:
        
        # Se convierten las imágenes a RGBA
        reference_image = reference_image.copy().convert('RGBA') 
        filler_image = filler_image.copy().convert('RGBA')   
        
        recursive_image = Image.new("RGBA", reference_image.size)    # Se crea una nueva imagen RGBA
        image_list = []
        webpalette_rgb_codes = []    
        
        with open('Tareas/Tarea3/CSV/WebPalette.csv', 'r') as csv_file_palette:  # Se lee el archivo CSV con la paleta de colores
            reader = csv.DictReader(csv_file_palette)          
            for row in reader:                       
                triplet = ast.literal_eval(row['rgb_values'])
                webpalette_rgb_codes.append(triplet)            
            
        for i, color in enumerate(webpalette_rgb_codes):         # Se aplica el filtro de color a la imagen y se guardan las copias
            filtered_image = color_filter(
                filler_image.copy().resize((tile_width, tile_height), Image.Resampling.LANCZOS),
                color
            )
            image_list.append((color, filtered_image))
            
        for i in range(0, recursive_image.width, tile_width):         # Se generan los mosaicos           
            for j in range(0, recursive_image.height, tile_height):   # Se recorren las posiciones de los mosaicos
                block_width = min(tile_width, recursive_image.width - i)  # Se calcula el ancho y alto del mosaico
                block_height = min(tile_height, recursive_image.height - j)                                         
                zone_color = get_average_color(reference_image, i, j, block_width, block_height)   # Se obtiene el color promedio de la zona
                best_thumbnail = select_best_thumbnail(image_list, zone_color)                    # Se selecciona la miniatura más adecuada
                recursive_image.paste(best_thumbnail, (i, j))                                     # Se pega la miniatura en la posición del mosaico

    return recursive_image
