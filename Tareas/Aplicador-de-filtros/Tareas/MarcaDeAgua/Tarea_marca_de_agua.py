'''
Script que aplica y/o elimina una marca de agua a una imagen 

Autor: Gabriela López Diego 
No. de cuenta: 318243485
Fecha: 26/Feb/25
'''
from PIL import Image, ImageFilter


def apply_watermark(input_image_path, watermark_image_path="Tareas/MarcaDeAgua/logo_prueba.png", position=(0,0)):
    '''
    Función que aplica una marca de agua a una imagen
    
    Parámetros:
        - input_image_path: Ruta de la imagen original
        - output_image_path: Ruta de la imagen de salida
        - watermark_image_path: Ruta de la marca de  (por defecto se puede modificar)
        - position: Posición de la marca de agua en la imagen
    '''
    
    # Abrimos las img y las convertimos a RGBA
    base_image = input_image_path.convert('RGBA')
    watermark = Image.open(watermark_image_path).convert('RGBA')
    
    width, height = base_image.size
    
    # Creamos una imagen nueva con el mismo tamaño que la original y la rellenamos de blanco
    new_img = Image.new('RGBA', (width, height), (0,0,0,0))
    
    # Ahora, pegamos la imagen original y la marca de agua en la imagen nueva
    new_img.paste(base_image, (0,0))
    new_img.paste(watermark, position, mask=watermark)
    
    return new_img #Retorna la nueva imagen con la marca de agua
    
    