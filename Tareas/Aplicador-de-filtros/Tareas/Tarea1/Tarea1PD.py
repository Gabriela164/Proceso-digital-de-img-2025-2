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
    imagen = imagen.convert("RGBA")  
    pixels = imagen.load()
    ancho, altura = imagen.size

    for y in range(0, altura, tamano_bloque):
        for x in range(0, ancho, tamano_bloque):
            # Se inicializan los acumuladores
            # r_total: suma del rojo
            # g_total: suma del verde
            # b_total: suma del azul
            # count: contador de píxeles en el bloque (para calcular el promedio)
            r_total, g_total, b_total, count = 0, 0, 0, 0

            # Calcular el color promedio del bloque
            for i in range(tamano_bloque):
                for j in range(tamano_bloque):
                    # Verificamos que no nos salgamos de los límites de la imagen
                    if x + j < ancho and y + i < altura:
                        # Tomamos los valores RGB del píxel
                        r, g, b, a = pixels[x + j, y + i]
                        r_total += r
                        g_total += g
                        b_total += b
                        count += 1
                        
            if count > 0:
                # Calculamos el color promedio de cada valor RGBA
                color_promedio = ( r_total // count, g_total // count, b_total // count, a)
            # Asignar el color promedio obtenido al bloque
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
    imagen = imagen.convert("RGBA")  
    ancho, altura = imagen.size 
    nueva_imagen = imagen.copy()

    for x in range(ancho):
        for y in range(altura):
            r, g, b, a = nueva_imagen.getpixel((x,y)) #Para cada pixel obtenemos sus valores en formato RGB
            # Obtenemos el promedio de los 3 valores para encontrar un nivel de gris
            gris = (r + g + b) // 3  
            nueva_imagen.putpixel((x, y), (gris,gris,gris,a)) #Colocamos el nuevo valor de gris a cada pixel 
    return nueva_imagen


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


def filtro_alto_contraste_inverso(imagen):
    '''
    Aplica un filtro de alto contraste inverso, convirtiendo los píxeles a blanco o negro según su intensidad.

    Parámetros:
    - imagen: Imagen de entrada.
    
    Devuelve:
    1. Imagen con alto contraste inverso.
    '''
    imagen = imagen.convert("RGBA")  
    ancho, altura = imagen.size    
    nueva_imagen = imagen.copy()

    # Recorremos cada pixel de la imagen
    for x in range(ancho):
        for y in range(altura):
            r, g, b, a = imagen.getpixel((x, y))
            gris = int(0.299 * r + 0.587 * g + 0.114 * b)
            # Realiza el proceso opuesto al método alto contraste 
            nuevo_color = (0, 0, 0, a) if gris > 128 else (255, 255, 255, a)
            nueva_imagen.putpixel((x, y), nuevo_color)
    return nueva_imagen


def filtro_mica_roja(imagen):
    '''
    Aplica una mica roja a la imagen, mostrando únicamente la intensidad del canal rojo
    y eliminando los valores de los canales verde y azul.

    Parámetros:
    - imagen: Imagen de entrada en modo RGB.

    Devuelve:
    - Imagen con la mica roja aplicada (solo el canal rojo visible).
    '''
    imagen = imagen.convert("RGBA")  
    imagen_roja = Image.new("RGBA", imagen.size)      #Creamos una nueva imagen con el mismo tamaño que la original (para pintar el canal rojo)

    #Obtenemos los pixeles de la imagen original y de la nueva imagen
    pixeles = imagen.load() 
    pixeles_rojo = imagen_roja.load()
    ancho, altura = imagen.size  

    #Recorremos cada pixel de la imagen
    for i in range(ancho):
        for j in range(altura):
            # Obtenemos los valores RGBA del pixel
            r, g, b, a = pixeles[i, j]
            # Asignamos el valor del canal rojo al nuevo pixel y los demás canales a 0 (apaga los demás canales)
            # Esto hace que la imagen resultante solo muestre el canal rojo
            pixeles_rojo[i, j] = (r, 0, 0, a)
            
    return imagen_roja


def filtro_mica_verde(imagen):
    '''
    Aplica una mica verde a la imagen, mostrando únicamente la intensidad del canal verde
    y eliminando los valores de los canales rojo y azul.

    Parámetros:
    - imagen: Imagen de entrada en modo RGB.

    Devuelve:
    - Imagen con la mica verde aplicada (solo el canal verde visible).
    ''' 
    imagen = imagen.copy().convert("RGBA")   #Realiza una copia y lo convierte a formato RGBA
    imagen_verde = Image.new("RGBA", imagen.size)  #Creamos una nueva imagen con el mismo tamaño que la original (para pintar el canal verde)

    #Obtenemos los pixeles de la imagen original y de la nueva imagen
    pixeles = imagen.load()
    pixeles_verde = imagen_verde.load()
    ancho, altura = imagen.size

    #Recorremos cada pixel de la imagen
    for i in range(ancho):
        for j in range(altura):
            # Obtenemos los valores RGB del pixel
            r, g, b, a = pixeles[i, j]
            # Asignamos el valor del canal verde al nuevo pixel y los demás canales a 0 (apaga los demás canales)
            # Esto hace que la imagen resultante solo muestre el canal verde
            pixeles_verde[i, j] = (0, g, 0, a)

    return imagen_verde


def filtro_mica_azul(imagen):
    '''
    Aplica una mica azul a la imagen, mostrando únicamente la intensidad del canal azul
    y eliminando los valores de los canales rojo y verde.

    Parámetros:
    - imagen: Imagen de entrada en modo RGB.

    Devuelve:
    - Imagen con la mica azul aplicada (solo el canal azul visible).
    '''
    imagen = imagen.copy().convert("RGBA")  #Realiza una copia y lo convierte a formato RGB
    imagen_azul = Image.new("RGBA", imagen.size) #Creamos una nueva imagen con el mismo tamaño que la original (para pintar el canal azul)

    #Obtenemos los pixeles de la imagen original y de la nueva imagen
    pixeles = imagen.load()
    pixeles_azul = imagen_azul.load()
    ancho, altura = imagen.size

    for i in range(ancho):
        for j in range(altura):
            # Obtenemos los valores RGB del pixel
            r, g, b, a = pixeles[i, j]
            # Asignamos el valor del canal azul al nuevo pixel y los demás canales a 0 (apaga los demás canales)
            # Esto hace que la imagen resultante solo muestre el canal azul
            pixeles_azul[i, j] = (0, 0, b, a)

    return imagen_azul


def filtro_mica_combinado(imagen):
    '''
    Intercambia los canales de color RGB de la imagen de forma combinada de RGB a GBR.

    Parámetros:
    1. imagen: Imagen de entrada.

    Devuelve:
    1. Imagen con los colores intercambiados.
    '''
    imagen = imagen.copy().convert("RGBA")   #Realiza una copia y lo convierte a formato RGBA
    imagen = imagen.copy()
    pixeles = imagen.load()
    ancho, altura = imagen.size  

    for i in range(ancho):
        for j in range(altura):
            r, g, b, a = pixeles[i, j]     #Recuperamos los colores RGB
            pixeles[i, j] = (g, b, r, a)   #Combinamos los colores RGB a GBR
            
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
    imagen = imagen.convert("RGBA")   #Nos aseguramos de que la imagen esté en formato RGB
    pixeles = imagen.load()          #Obtenemos los pixeles de la imagen
    ancho,altura = imagen.size

    #Recorremos cada pixel de la imagen
    for i in range(ancho):
        for j in range(altura):
            r, g, b, a = pixeles[i, j]    #Obtenemos los valores RGB del pixel

            # Ajustamos el brillo sumando el valor de ajuste
            r = r + ajuste
            g = g + ajuste
            b = b + ajuste

            # Nos aseguramos de que los valores no superen 255 ni bajen de 0
            r = min(255, max(0, r))
            g = min(255, max(0, g))
            b = min(255, max(0, b))

            # Asignamos los nuevos valores RGB al pixel
            pixeles[i, j] = (r, g, b, a)

    return imagen

