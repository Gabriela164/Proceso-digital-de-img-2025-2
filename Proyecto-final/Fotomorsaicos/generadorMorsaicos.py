'''
PROYECTO FINAL: Morsaicos

CURSO: Proceso Digital de Imágenes 2025-2
Alumna: López Diego Gabriela 
Fecha: Mayo 2025

Descripción:
Este script nos permite procesar una imagen y generar un morsaico a partir de una galería de extensa 
de imágenes.

El script contiene las siguientes funciones:
- get_average_color: obtiene el color promedio de una región de una imagen.
- save_average_colors: procesa una biblioteca de imágenes y obtiene el color promedio de cada una.
- get_closest_image: busca la imagen más cercana en términos de color promedio respecto a un color de referencia.
- process_image_to_mosaic: procesa una imagen por regiones y utiliza las funciones anteriores para
construir un morsaicos de imágenes en HTML.
'''

import os
from PIL import Image
import math


def get_average_color(image, x, y, width, height):  
    '''
    Funcion que obtiene el color promedio de una región de una imagen
    
    Parametros:
    - image: imagen a procesar.
    - x: coordenada x del punto de inicio de la región.
    - y: coordenada y del punto de inicio de la región.
    - width: ancho de la región.
    - height: alto de la región.
    
    Retorna:
    - average_color: tripleta con el color promedio de la región.
    '''
    pixels = image.load()
    total_r, total_g, total_b, count, a = 0, 0, 0, 0, 0    
    average_color = -1

    for i in range(x, min(x + width, image.width)):
        for j in range(y, min(y + height, image.height)):  #Se restringe el análisis al área              
        
            temp_r, temp_g, temp_b, a = pixels[i, j]  #Se procesan los valores rgb de cada pixel 
            total_r += temp_r                       
            total_g += temp_g
            total_b += temp_b
            count += 1

    if count == 0:
        average_color = 0        
    else:
        average_color = (total_r // count, total_g // count, total_b // count) #Tripleta con el color promedio
    
    return average_color


def save_average_colors(folder_path, output_file):    
    '''
    Funcion que procesa una biblioteca de imágenes y obtiene el color promedio
    de cada una de ellas.
    Parametros:
    - folder_path: ruta del directorio que contiene la biblioteca de imágenes.
    - output_file: ruta del archivo de salida donde se guardará la información.
    
    Devuelve:
    - None: genera un archivo .txt con la información obtenida del proceso.
    '''
    with open(output_file, "w") as f:
        
        for image_file in os.listdir(folder_path):
            if image_file.lower().endswith((".jpg", ".png")):
                image_path = os.path.join(folder_path, image_file)
                image = None
                
                with Image.open(image_path) as img:        
                    image = img.convert("RGBA")

                avg_color = get_average_color(image, 0, 0, image.width, image.height)                
                f.write(f"{image_file},{avg_color[0]},{avg_color[1]},{avg_color[2]}\n")                             
    

def get_closest_image(avg_color, color_file, image_usage, version):   
    '''
    Funcion que busca la imagen más cercana en términos de color promedio respecto a un color de referencia.
    Parametros:
    - avg_color: color promedio de referencia.
    - color_file: ruta del archivo con la información de las imágenes.
    - image_usage: factor numérico para reducir la repetición de imágenes.
    - version: entero que indica el tipo de medida a emplear para determinar la distancia.
    
    Devuelve:
    - closest_image: nombre de la imagen más cercana al color promedio de referencia.
    '''
    min_distance = float("inf")
    closest_image = None
    with open(color_file, "r") as f:
        for line in f:
            name, r, g, b = line.strip().split(",")
            r, g, b = map(int, (r, g, b))
            distance = 0
            if version == 1:
                # Distancia euclidiana
                distance = math.sqrt((avg_color[0] - r) ** 2 + 
                                     (avg_color[1] - g) ** 2 + 
                                     (avg_color[2] - b) ** 2)
            elif version == 2:
                # Fórmula de distancia de Riemersma
                dr = avg_color[0] - r
                dg = avg_color[1] - g
                db = avg_color[2] - b
                # Ponderación según sensibilidad visual
                distance = math.sqrt(
                    (2 + dr / 256.0) * (dr ** 2) +
                    4 * (dg ** 2) +
                    (2 + (255 - dr) / 256.0) * (db ** 2)
                )
            
            usage_penalty = image_usage.get(name, 0)  # Penalizar imágenes más usadas
            adjusted_distance = distance + usage_penalty * 10  # Ajusta peso según uso
            if adjusted_distance < min_distance:
                min_distance = adjusted_distance
                closest_image = name    
    
    if closest_image:
        image_usage[closest_image] = image_usage.get(closest_image, 0) + 1
    
    return closest_image


def html_mosaic(img, color_file, region_size, base_library_path, version):   
    '''
    Funcion que procesa una imagen por regiones, obtiene el color promedio de cada una y busca
    la imagen más cercana en color dentro de una biblioteca, para asignarla a cada región en una tabla HTML.
    
    Parametros:
    - img: imagen a procesar.
    - color_file: ruta al archivo con la información de la biblioteca.
    - region_size: tamaño de las regiones (cuadradas) a procesar.
    - base_library_path: ruta de la biblioteca de imágenes 
    - version: entero que indica el tipo de medida a emplear para determinar la distancia.
    
    Devuelve:
    - html: cadena con el código HTML para generar un mosaico de imágenes y poder visualizarlo en un navegador.
    '''     
    
    if img.mode != "RGBA":
        img = img.convert("RGB")
    
    image = img.convert("RGBA")   
     
    html = "<html><body><table style='border-collapse: collapse;'>"
    width, height = image.size
    image_usage = {}  # Para rastrear el uso de miniaturas.

    for j in range(0, height, region_size):
        html += "<tr>"
        for i in range(0, width, region_size):
            block_width = min(region_size, width - i)
            block_height = min(region_size, height - j)
            
            # Obtener el color promedio de la región.
            zone_color = get_average_color(image, i, j, block_width, block_height)
            
            # Obtener la miniatura más cercana.
            best_thumbnail_name = get_closest_image(zone_color, color_file, image_usage, version)
            
            # Construir la ruta relativa.
            best_thumbnail_path = os.path.join(base_library_path, best_thumbnail_name)
            best_thumbnail_relative = os.path.relpath(best_thumbnail_path)
            
            # Añadir la celda al HTML.
            html += f"<td style='padding: 0;'>"
            html += f"<img src='{best_thumbnail_relative}' width='{region_size}' height='{region_size}' />"
            html += "</td>"
        
        html += "</tr>"
    
    html += "</table></body></html>"
    
    return html
    
    
def img_mosaic(img, color_file, region_size, base_library_path, version):
    '''
    Construye una imagen tipo PIL (morsaico) a partir de una imagen original
    y una biblioteca de miniaturas, pegando la miniatura más cercana al color
    promedio de cada región.

    Parámetros:
    - img: imagen original (PIL.Image).
    - color_file: archivo con los colores promedio de la biblioteca.
    - region_size: tamaño de los bloques.
    - base_library_path: carpeta con las miniaturas.
    - version: método de cálculo de distancia.

    Devuelve:
    - mosaic_img: imagen PIL resultante.
    '''
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    
    width, height = img.size
    mosaic_img = Image.new("RGBA", (width, height))
    image_usage = {}

    for y in range(0, height, region_size):
        for x in range(0, width, region_size):
            block_width = min(region_size, width - x)
            block_height = min(region_size, height - y)

            avg_color = get_average_color(img, x, y, block_width, block_height)
            best_match_name = get_closest_image(avg_color, color_file, image_usage, version)
            
            if best_match_name:
                best_match_path = os.path.join(base_library_path, best_match_name)
                with Image.open(best_match_path) as thumb:
                    thumb = thumb.resize((block_width, block_height))
                    mosaic_img.paste(thumb, (x, y))
    
    return mosaic_img

