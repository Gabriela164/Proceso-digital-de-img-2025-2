from PIL import Image, ImageDraw, ImageFont


def grey_scale(original_image, version):
    '''
    Función que implementa 2 filtros de escala de grises.
    version = 1: emplea una media simple.
    version = 2: emplea una media ponderada.
    Parametros:
    original_image: imagen original a la que se le aplicará el filtro.
    version: versión del filtro a aplicar.
    Return: 
    imagen en escala de grises.
    '''
    if original_image:   
        original_image =  original_image.copy().convert("RGBA")   
        grey_img = Image.new("RGBA", original_image.size)
        
        pixels = original_image.load()
        grey_pixels = grey_img.load()

        for i in range(original_image.width):
            for j in range(original_image.height):
                r, g, b, a = pixels[i, j]
                grey = (r + g + b) // 3

                if version == 2:
                    grey = int(r*0.299 + g*0.587 + b*0.114)
                grey_pixels[i, j] = (grey, grey, grey, a)
         
        return grey_img


 
def watercolor(original_image, matrix_size, version):
    '''
    Funcion que aplica el filtro oleo 
    Parametros:
    - original_image: imagen original a la que se le aplicará el filtro.
    - matrix_size: tamaño de la matriz de vecindad.
    - version: versión del filtro a aplicar.
    Return:
    - imagen con filtro oleo.
    '''
    if original_image and (version ==1 or version == 2):
        original_image =  original_image.copy().convert("RGBA")   
        watercolor_image = Image.new("RGBA", original_image.size) 
        watercolor_pixels = watercolor_image.load()

        if version == 2:
            # Si la versión es 2, aplicar filtro de escala de grises ponderado
            original_image = grey_scale(original_image, 2)
        
        original_pixels = original_image.load()

        image_width, image_height = original_image.size
        radius = matrix_size // 2

        # Recorrer todos los píxeles de la imagen
        for x in range(image_width):
            for y in range(image_height):
                # Crear una lista para almacenar los colores de la vecindad
                color_count = {}                 
                # Recorrer la vecindad alrededor del píxel (x, y)
                for i in range(matrix_size):
                    for j in range(matrix_size):
                        offset_x = i - radius
                        offset_y = j - radius
                        nx = x + offset_x
                        ny = y + offset_y

                        if 0 <= nx < image_width and 0 <= ny < image_height:
                            current_color = original_pixels[nx, ny]
                                
                            # Si el color ya está en el diccionario, incrementar el contador
                            if current_color in color_count:
                                color_count[current_color] += 1
                            else:
                                color_count[current_color] = 1

                # Encontrar el color más común
                most_common_color = max(color_count, key=color_count.get)
                
                # Si no hay un color que se repita más, calcular el promedio
                if color_count[most_common_color] == 1:
                    avg_r = sum([color[0] for color in color_count.keys()]) // len(color_count)
                    avg_g = sum([color[1] for color in color_count.keys()]) // len(color_count)
                    avg_b = sum([color[2] for color in color_count.keys()]) // len(color_count)
                    avg_a = sum([color[3] for color in color_count.keys()]) // len(color_count)
                    watercolor_pixels[x, y] = (avg_r, avg_g, avg_b, avg_a)
                else:
                    watercolor_pixels[x, y] = most_common_color

        return watercolor_image
