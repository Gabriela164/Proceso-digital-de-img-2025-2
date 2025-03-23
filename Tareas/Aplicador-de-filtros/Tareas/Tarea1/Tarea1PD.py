"""

Script que recibe una imagen y le aplica varios filtros sencillos:

1. Filtro mosaico
2. Filtro escala de grises (Promedio RGB)
3. Filtro escala de grises (Ponderado (.30*r + .70*g + .10*b))
4. Filtro alto contraste 
5. Filtro inverso contraste 
6. Filtro mica RGB por separado 
7. Filtro mica RGB combinados
8. Filtro brillo

Alumna: Gabriela López Diego 
No. de cuenta: 318243485 
Fecha: Febrero 2025

"""

from PIL import Image, ImageEnhance


def filtro_mosaico(imagen, tamano_bloque=20):
    '''
    Aplica un filtro de mosaico a una imagen, dividiéndola en bloques de tamaño definido y reemplazando 
    cada bloque con el color promedio de sus píxeles. Esto genera un efecto pixelado.

    Parámetros:
    1. imagen: Imagen de entrada a la que se aplicará el filtro.
    2. tamano_bloque: Tamaño de cada mosaico en píxeles. 

    Devuelve:
    1.Nueva imagen con el filtro mosaico aplicado.
    '''
    imagen = imagen.convert("RGB")  
    pixels = imagen.load()
    ancho, altura = imagen.size

    for y in range(0, altura, tamano_bloque):
        for x in range(0, ancho, tamano_bloque):
            r_total, g_total, b_total, count = 0, 0, 0, 0

            # Calcular el color promedio del bloque
            for i in range(tamano_bloque):
                for j in range(tamano_bloque):
                    if x + j < ancho and y + i < altura:
                        r, g, b = pixels[x + j, y + i]
                        r_total += r
                        g_total += g
                        b_total += b
                        count += 1
                        
            if count > 0:
                color_promedio = (r_total // count, g_total // count, b_total // count)
                
            # Asignar el color promedio al bloque
            for i in range(tamano_bloque):
                for j in range(tamano_bloque):
                    if x + j < ancho and y + i < altura:
                        pixels[x + j, y + i] = color_promedio
    return imagen


def filtro_gris_promedio(imagen):
    '''
    Convierte una imagen a blanco y negro usando el promedio de los valores RGB.

    Parámetros:
    1. imagen: Imagen de entrada.

    Devuelve:
    1.Imagen en blanco y negro (escala de grises).
    '''
    ancho, altura = imagen.size
    nueva_imagen = imagen.copy()

    for x in range(ancho):
        for y in range(altura):
            r, g, b = nueva_imagen.getpixel((x,y))
            gris = (r + g + b) // 3 #promedio 
            nueva_imagen.putpixel((x, y), (gris,gris,gris))
    return nueva_imagen



def filtro_gris_ponderado(imagen):
    '''
    Convierte una imagen a blanco y negro usando (.30*r + .70*g + .10*b)

    Parámetros:
    1. imagen : Imagen de entrada

    Devuelve:
    1. Imagen en blanco y negro (escala de grises)
    '''
    ancho, altura = imagen.size
    nueva_imagen = imagen.copy()

    for x in range(ancho):
        for y in range(altura):
            r, g, b = imagen.getpixel((x, y))
            gris = int(.30 * r + .70 * g + .10 * b)
            nueva_imagen.putpixel((x, y), (gris,gris,gris))
    return nueva_imagen


def filtro_alto_contraste(imagen):
    '''
    Aplica un filtro de alto contraste, convirtiendo los píxeles a blanco o negro según su intensidad.

    Parámetros:
    1. Imagen: Imagen de entrada para plicar el filtro. 
    
    Devuelve:
    1. Imagen con alto contraste.
    '''
    ancho, altura = imagen.size
    nueva_imagen = imagen.copy()

    for x in range(ancho):
        for y in range(altura):
            r, g, b = imagen.getpixel((x, y))
            # Calcular el valor de gris (promedio ponderado)
            gris = int(0.299 * r + 0.587 * g + 0.114 * b)
            # Determinamos si el píxel es blanco o negro en función de la intensidad del gris
            nuevo_color = (255, 255, 255) if gris > 128 else (0, 0, 0)
            nueva_imagen.putpixel((x, y), nuevo_color)

    return nueva_imagen


def filtro_alto_contraste_inverso(imagen):
    '''
    Aplica un filtro de alto contraste inverso, convirtiendo los píxeles a blanco o negro según su intensidad.

    Parámetros:
    - imagen: Imagen de entrada.
    
    Devuelve:
    1. Imagen con alto contraste inverso.
    '''
    ancho, altura = imagen.size    
    nueva_imagen = imagen.copy()

    # Iterar sobre cada píxel
    for x in range(ancho):
        for y in range(altura):
            r, g, b = imagen.getpixel((x, y))
            gris = int(0.299 * r + 0.587 * g + 0.114 * b)
            #Invertimos la lógica
            nuevo_color = (0, 0, 0) if gris > 128 else (255, 255, 255)
            nueva_imagen.putpixel((x, y), nuevo_color)
    return nueva_imagen


def filtro_mica_roja(imagen):
    '''
    Separa los canales de color RGB de la imagen en imágenes individuales.

    Parámetros:
    1. imagen: Imagen de entrada.

    Devuelve:
    1. Tres imágenes cada una representando un canal de color (R, G, B).
    '''
    imagen = imagen.copy().convert("RGB")   

    # Crear imágenes vacías para cada canal de color
    imagen_roja = Image.new("RGB", imagen.size)      
    imagen_verde = Image.new("RGB", imagen.size)      
    imagen_azul = Image.new("RGB", imagen.size)      

    # Obtenemos los píxeles de la imagen original y de las nuevas imágenes
    pixeles = imagen.load()
    pixeles_rojo = imagen_roja.load()
    pixeles_verde = imagen_verde.load()
    pixeles_azul = imagen_azul.load()
    
    ancho, altura = imagen.size  

    # Recorrer la imagen y extraer cada canal
    for i in range(ancho):
        for j in range(altura):
    
            r, g, b = pixeles[i, j]
            pixeles_rojo[i, j] = (r, 0, 0)   #Asignamos el color rojo y los demás en 0
            pixeles_verde[i, j] = (0, g, 0)  #Asginamos el color verde y los demás en 0
            pixeles_azul[i, j] = (0, 0, b)   #Asignamos el color azul y los demás en 0
            
    return imagen_roja


def filtro_mica_verde(imagen):
    '''
    Separa los canales de color RGB de la imagen en imágenes individuales.

    Parámetros:
    1. imagen: Imagen de entrada.

    Devuelve:
    1. Tres imágenes cada una representando un canal de color (R, G, B).
    '''
    imagen = imagen.copy().convert("RGB")   

    # Crear imágenes vacías para cada canal de color
    imagen_roja = Image.new("RGB", imagen.size)      
    imagen_verde = Image.new("RGB", imagen.size)      
    imagen_azul = Image.new("RGB", imagen.size)      

    # Obtenemos los píxeles de la imagen original y de las nuevas imágenes
    pixeles = imagen.load()
    pixeles_rojo = imagen_roja.load()
    pixeles_verde = imagen_verde.load()
    pixeles_azul = imagen_azul.load()
    
    ancho, altura = imagen.size  

    # Recorrer la imagen y extraer cada canal
    for i in range(ancho):
        for j in range(altura):
    
            r, g, b = pixeles[i, j]
            pixeles_rojo[i, j] = (r, 0, 0)   #Asignamos el color rojo y los demás en 0
            pixeles_verde[i, j] = (0, g, 0)  #Asginamos el color verde y los demás en 0
            pixeles_azul[i, j] = (0, 0, b)   #Asignamos el color azul y los demás en 0
            
    return imagen_verde

def filtro_mica_azul(imagen):
    '''
    Separa los canales de color RGB de la imagen en imágenes individuales.

    Parámetros:
    1. imagen: Imagen de entrada.

    Devuelve:
    1. Tres imágenes cada una representando un canal de color (R, G, B).
    '''
    imagen = imagen.copy().convert("RGB")   

    # Crear imágenes vacías para cada canal de color
    imagen_roja = Image.new("RGB", imagen.size)      
    imagen_verde = Image.new("RGB", imagen.size)      
    imagen_azul = Image.new("RGB", imagen.size)      

    # Obtenemos los píxeles de la imagen original y de las nuevas imágenes
    pixeles = imagen.load()
    pixeles_rojo = imagen_roja.load()
    pixeles_verde = imagen_verde.load()
    pixeles_azul = imagen_azul.load()
    
    ancho, altura = imagen.size  

    # Recorrer la imagen y extraer cada canal
    for i in range(ancho):
        for j in range(altura):
    
            r, g, b = pixeles[i, j]
            pixeles_rojo[i, j] = (r, 0, 0)   #Asignamos el color rojo y los demás en 0
            pixeles_verde[i, j] = (0, g, 0)  #Asginamos el color verde y los demás en 0
            pixeles_azul[i, j] = (0, 0, b)   #Asignamos el color azul y los demás en 0
            
    return imagen_azul


def filtro_mica_combinado(imagen):
    '''
    Intercambia los canales de color RGB de la imagen de forma combinada de RGB a GBR.

    Parámetros:
    1. imagen: Imagen de entrada.

    Devuelve:
    1. Imagen con los colores intercambiados.
    '''
    imagen = imagen.copy()
    pixeles = imagen.load()
    ancho, altura = imagen.size  

    for i in range(ancho):
        for j in range(altura):
            r, g, b = pixeles[i, j]     #Recuperamos los colores RGB
            pixeles[i, j] = (g, b, r)   #Combinamos los colores RGB a GBR
            
    return imagen


def filtro_brillo(imagen, ajuste=50):
    '''
    Ajusta el brillo de la imagen sumando o restando un valor a cada componente RGB.

    Parámetros:
    1. imagen : Imagen de entrada.
    2. ajuste: Valor de ajuste de brillo.

    Devuelve:
    1. Imagen con el brillo modificado.
    '''
    imagen = imagen.convert("RGB")
    pixeles = imagen.load()
    ancho,altura = imagen.size

    for i in range(ancho):
        for j in range(altura):
            r, g, b = pixeles[i, j]

            # Ajustamos el brillo sumando o restando el valor de ajuste
            r = r + ajuste
            g = g + ajuste
            b = b + ajuste

            # Nos aseguramos de que los valores no superen 255 ni bajen de 0
            r = min(255, max(0, r))
            g = min(255, max(0, g))
            b = min(255, max(0, b))

            # Asignar el nuevo valor al píxel
            pixeles[i, j] = (r, g, b)

    return imagen

