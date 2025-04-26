from PIL import Image
'''
Script para eliminar marcas de agua de imágenes.
Este script utiliza técnicas de procesamiento de imágenes para identificar y eliminar marcas de agua de imágenes originales.

Cumple con el reto dejado en el curso de Procesamiento Digital de Imágenes 2025-2

Autor: Lopez Diego Gabriela
Fecha: Abril 2025
'''

def extraer_rojo(imagen_fondo):
    '''
    Funcion que extrae los píxeles rojos de la imagen de fondo.
    Parametros:
    - imagen_fondo: Imagen de fondo de la que se extraerán los píxeles rojos.
    Retorna:
    - marcas_agua: Imagen que contiene los píxeles rojos extraídos de la imagen de fondo.
    '''
    ancho, alto = imagen_fondo.size
    marcas_agua = Image.new("RGB", imagen_fondo.size) 
    pixeles_marca_agua = marcas_agua.load()
    pixeles_fondo = imagen_fondo.load() 

    for i in range(ancho):
        for j in range(alto):            
            r, g, b = pixeles_fondo[i, j] 

            if r > g and r > b: 
                pixeles_marca_agua[i, j] = (r, g , b)                           
            else:
                pixeles_marca_agua[i, j] = (255, 255, 255)   
   
    return marcas_agua


def eliminar_pixeles_grises(imagen, umbral_tolerancia):    
    '''
    Funcion que elimina los píxeles grises de la imagen cuyo rango de diferencia entre los valores RGB es menor que un umbral.
    Parametros:
    - imagen: Imagen de entrada.
    - umbral_tolerancia: Umbral de tolerancia para considerar un píxel como gris.
    Retorna:
    - imagen: Imagen con los píxeles grises eliminados.
    '''
    imagen = imagen.convert('RGB')    
    pixeles = imagen.load()
    ancho, alto = imagen.size
    
    for x in range(ancho):
        for y in range(alto):
            r, g, b = pixeles[x, y]
            
            if abs(r - g) < umbral_tolerancia and abs(r - b) < umbral_tolerancia and abs(g - b) < umbral_tolerancia:                
                pixeles[x, y] = (255, 255, 255)
    
    return imagen


def barrer_marca_agua(imagen_original, imagen_marca_agua, tamano_matriz): 
    '''
    Metodo que realiza una operacion de barrido sobre la imagen con marca de agua, 
    reemplazando los pixeles marcados con colores (no rojos) de su vecindad.
    Parametros:
    - imagen_original: Imagen original.
    - imagen_marca_agua: Imagen de la marca de agua.
    - tamano_matriz: Tamaño de la matriz de búsqueda.
    Retorna:
    - imagen_resultado: Imagen resultante con la marca de agua eliminada.
    '''   
    imagen_original = imagen_original.convert('RGB')
    imagen_marca_agua = imagen_marca_agua.convert('RGB')    
    ancho, alto = imagen_original.size  
    imagen_resultado = imagen_original.copy()
    pixeles_resultado = imagen_resultado.load()
    pixeles_original = imagen_original.load()
    pixeles_marca_agua = imagen_marca_agua.load()
       
    for x in range(ancho):
        for y in range(alto):
            r_marca, g_marca, b_marca = pixeles_marca_agua[x, y]            
            if (r_marca, g_marca, b_marca) != (255, 255, 255):               
                color_reemplazo = obtener_color_vecinos(ancho, alto, pixeles_original, x, y, tamano_matriz)
                if color_reemplazo:
                    pixeles_resultado[x, y] = color_reemplazo
                else:
                    pixeles_resultado[x, y] = pixeles_original[x, y]
            else:
                pixeles_resultado[x, y] = pixeles_original[x, y]

    return imagen_resultado
        

def obtener_color_vecinos(ancho_imagen, alto_imagen, pixeles, x, y, tamano_matriz):    
    '''
    Metodo que obtiene el color promedio de los vecinos en torno a un píxel dado, si no es rojo dominante.
    Parametros:
    - ancho_imagen: Ancho de la imagen.
    - alto_imagen: Alto de la imagen.
    - pixeles: Píxeles de la imagen.
    - x: Coordenada x del píxel.
    - y: Coordenada y del píxel.
    - tamano_matriz: Tamaño de la matriz de búsqueda.
    Retorna:
    - color_adecuado: Color promedio de los vecinos.
    '''
    colores = []
    
    for i in range(tamano_matriz):
        for j in range(tamano_matriz):
            posicion_vecino_x = (x - (tamano_matriz // 2) + i) % ancho_imagen
            posicion_vecino_y = (y - (tamano_matriz // 2) + j) % alto_imagen            
            r, g, b = pixeles[posicion_vecino_x, posicion_vecino_y]           
            if r <= g or r <= b:
                colores.append((r, g, b))
    no_colores = len(colores)    
    if no_colores > 0:   
        r, g, b = 0, 0, 0     
        for color in colores:
            r += color[0]
            g += color[1]
            b += color[2]
        color_adecuado = (r // no_colores, g // no_colores, b // no_colores)

        return color_adecuado
   

    return None 


def get_rojo_promedio(imagen):
    '''
    Calcula el promedio del color rojo dominante en la imagen.
    Parametros:
    - imagen: Imagen de entrada.
    Retorna:
    - rojo_promedio: Tupla con el promedio de los componentes RGB.
    '''
    imagen = imagen.convert('RGB')
    ancho, alto = imagen.size    
    pixeles = imagen.load()
    sum_r = 0
    sum_g = 0
    sum_b = 0
    contador = 0 
    for i in range(ancho):
        for j in range(alto):            
            r, g, b = pixeles[i, j] 

            if r > g and r > b:
                sum_r += r
                sum_g += g
                sum_b += b 
                contador += 1  
    rojo_promedio = (sum_r // contador, sum_g // contador, sum_b // contador)    
    return rojo_promedio           


def demezclar_marca_agua(imagen_con_marca, solo_marca, color_prom, factor):
    '''
    Metodo que aplica un proceso inverso para separar la marca de agua de la imagen, ajustando el color según un promedio.
    Parametros:
    - imagen_con_marca: Imagen con la marca de agua.
    - solo_marca: Imagen de la marca de agua.
    - color_prom: Color promedio de la marca de agua.
    - factor: Factor de ajuste.
    Retorna:
    - imagen_resultante: Imagen resultante con la marca de agua separada.
    '''
    imagen_con_marca = imagen_con_marca.convert('RGB')
    solo_marca = solo_marca.convert('RGB')   
    ancho, alto = imagen_con_marca.size   
    imagen_resultante = Image.new('RGB', (ancho, alto))
    pixeles_resultante = imagen_resultante.load()    
    pixeles_con_marca = imagen_con_marca.load()
    pixeles_solo_marca = solo_marca.load()
    r_prom = color_prom[0]
    g_prom = color_prom[1]
    b_prom = color_prom[2]
   
    for x in range(ancho):
        for y in range(alto):
            r_con_marca, g_con_marca, b_con_marca = pixeles_con_marca[x, y]
            r_solo_marca, g_solo_marca, b_solo_marca = pixeles_solo_marca[x, y]

            if  (r_solo_marca == 255 and g_solo_marca == 255 and b_solo_marca == 255):
                pixeles_resultante[x, y] = (r_con_marca, g_con_marca, b_con_marca)
            else:                
                r_resultante = min(255, int((r_con_marca - factor*r_prom) / (1 - factor)))
                g_resultante = min(255, int((g_con_marca - factor*g_prom) / (1 - factor)))
                b_resultante = min(255, int((b_con_marca - factor*b_prom) / (1 - factor)))
                gris = (r_resultante + g_resultante + b_resultante)//3                
                pixeles_resultante[x, y] = (gris, gris, gris)
    
    return imagen_resultante


def convolucion_paralela(imagen_base, marca_agua, matriz_conv, factor, bias):
    '''
    Metodo que ejecuta convolución sobre una imagen base utilizando una matriz de convolución.
    Parametros:
    - imagen_base: Imagen base sobre la que se aplicará la convolución.
    - marca_agua: Imagen de la marca de agua.
    - matriz_conv: Matriz de convolución a aplicar.
    - factor: Factor de ajuste para la convolución.
    - bias: Sesgo a aplicar en la convolución.
    Retorna:
    - imagen_resultante: Imagen resultante después de aplicar la convolución.
    '''
    if imagen_base and marca_agua:                     
        pixeles_base = imagen_base.load()
        marca_pixeles = marca_agua.load()
        altura_matriz = len(matriz_conv)
        ancho_matriz = len(matriz_conv[0])       
        imagen_resultante = Image.new("RGB", imagen_base.size)   
        pixeles_resultantes = imagen_resultante.load()

        for columna_imagen in range(imagen_base.width):
            for fila_imagen in range(imagen_base.height):

                sum_r, sum_g, sum_b = 0, 0, 0  
                if marca_pixeles[columna_imagen, fila_imagen] != (255, 255, 255):

                    for fila_matriz in range(altura_matriz):
                        for columna_matriz in range(ancho_matriz):                        
                            columna_resultante = (columna_imagen - (ancho_matriz // 2) + columna_matriz) % imagen_base.width
                            fila_resultante = (fila_imagen - (altura_matriz // 2) + fila_matriz) % imagen_base.height
                            r, g, b = pixeles_base[columna_resultante, fila_resultante]
                            sum_r += r * matriz_conv[fila_matriz][columna_matriz]
                            sum_g += g * matriz_conv[fila_matriz][columna_matriz]
                            sum_b += b * matriz_conv[fila_matriz][columna_matriz]

                    sum_r = min(max(int(factor*sum_r + bias), 0), 255)
                    sum_g = min(max(int(factor*sum_g + bias), 0), 255)
                    sum_b = min(max(int(factor*sum_b + bias), 0), 255)
                    pixeles_resultantes[columna_imagen, fila_imagen] = (sum_r, sum_g, sum_b)

                else:                  

                    pixeles_resultantes[columna_imagen, fila_imagen]  = pixeles_base[columna_imagen, fila_imagen]       

        return imagen_resultante


def aumentar_brillo(r, g, b, factor):
    '''
    Metodo que aumenta el brillo de un color RGB.
    Parametros:
    - r: Componente roja del color.
    - g: Componente verde del color.
    - b: Componente azul del color.
    - factor: Factor de incremento de brillo.
    Retorna:
    - r, g, b: Componentes del color con brillo incrementado.
    '''
    r = min(int(r * factor), 255)
    g = min(int(g * factor), 255)
    b = min(int(b * factor), 255)
    return r, g, b

def incrementar_brillo_marca_agua(imagen_original, imagen_marca_agua, factor): 
    '''
    Metodo que incrementa el brillo de la imagen original en la zona de la marca de agua.
    Parametros:
    - imagen_original: Imagen original.
    - imagen_marca_agua: Imagen de la marca de agua.
    - factor: Factor de incremento de brillo.
    
    Retorna:
    - imagen_resultado: Imagen resultante con el brillo incrementado.
    '''   
    imagen_original = imagen_original.convert('RGB')
    imagen_marca_agua = imagen_marca_agua.convert('RGB')   
    ancho, alto = imagen_original.size
    imagen_resultado = imagen_original.copy()
    pixeles_resultado = imagen_resultado.load()
    pixeles_original = imagen_original.load()
    pixeles_marca_agua = imagen_marca_agua.load()
 
    for x in range(ancho):
        for y in range(alto):
            
            r_marca, g_marca, b_marca = pixeles_marca_agua[x, y]            
            if (r_marca, g_marca, b_marca) != (255, 255, 255):              
                r, g, b = pixeles_original[x, y]                
                pixeles_resultado[x, y] = aumentar_brillo(r, g, b, factor)
    
    return imagen_resultado


def fusionar_imagenes_por_marca(imagen1, imagen2, imagen_marca_agua):
    '''
    Metodo que fusiona dos imagenes en la zona de la marca de agua.
    Parametros:
    - imagen1: Imagen original.
    - imagen2: Imagen de la marca de agua.
    - imagen_marca_agua: Imagen de la marca de agua.
    Retorna:
    - imagen_resultado: Imagen resultante de la fusión.
    '''
    imagen1 = imagen1.convert('RGB')
    imagen2 = imagen2.convert('RGB')
    imagen_marca_agua = imagen_marca_agua.convert('RGB')
    ancho, alto = imagen1.size
    imagen_resultado = Image.new('RGB', (ancho, alto))
    pixeles_resultado = imagen_resultado.load()
    pixeles1 = imagen1.load()
    pixeles2 = imagen2.load()
    pixeles_marca_agua = imagen_marca_agua.load()
    
    for x in range(ancho):
        for y in range(alto):            
            r_marca, g_marca, b_marca = pixeles_marca_agua[x, y] 

            if (r_marca, g_marca, b_marca) != (255, 255, 255):                
                r1, g1, b1 = pixeles1[x, y]
                r2, g2, b2 = pixeles2[x, y]               
                r_promedio = (r1 + r2) // 2
                g_promedio = (g1 + g2) // 2
                b_promedio = (b1 + b2) // 2
                pixeles_resultado[x, y] = (r_promedio, g_promedio, b_promedio)
            else:                
                pixeles_resultado[x, y] = pixeles1[x, y]
    
    return imagen_resultado

#Matrices para convolución
matriz_media= [            
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
    ]   
fact_m = 1.0 / 9.0;
bias_m = 0.0; 

matriz_bsharp = [
    [-1, -1, -1, -1, -1],
    [-1,  2,  2,  2, -1],
    [-1,  2,  8,  2, -1],
    [-1,  2,  2,  2, -1],
    [-1, -1, -1, -1, -1],
    ]
fact_bsharp = 1.0 / 8.0
bias_bsharp = 0.0


def reemplazar_por_gris_mas_cercano(imagen, marca):
    '''
    Funcion que reemplaza los píxeles de la imagen con la marca de agua por el gris más cercano.
    Parametros:
    - imagen: Imagen original con la marca de agua.
    - marca: Imagen de la marca de agua.
    Retorna:
    - nueva_imagen: Imagen con la marca de agua reemplazada por el gris más cercano.
    '''
    nueva_imagen = imagen.copy()
    pixeles = nueva_imagen.load()
    marca_px = marca.load()
    ancho, alto = imagen.size

    for y in range(alto):
        for x in range(ancho):
            r, g, b = marca_px[x, y]
            if r > g + 40 and r > b + 40:
                # Buscar el gris más cercano
                gris = int((g + b) / 2)
                pixeles[x, y] = (gris, gris, gris)
    return nueva_imagen

def reemplazar_por_vecinos_dominantes(imagen, marca, tamano_matriz):
    '''
    Funcion que reemplaza los píxeles de la imagen con la marca de agua por el color más común
    de su vecindad.
    Parametros:
    - imagen: Imagen original con la marca de agua.
    - marca: Imagen de la marca de agua.
    - tamano_matriz: Tamaño de la matriz de búsqueda.
    Retorna:
    - nueva_imagen: Imagen con la marca de agua reemplazada por el color más común.
    '''
    nueva_imagen = imagen.copy()
    pixeles = nueva_imagen.load()
    marca_px = marca.load()
    ancho, alto = imagen.size

    radio = tamano_matriz // 2

    for y in range(alto):
        for x in range(ancho):
            r, g, b = marca_px[x, y]
            if (r, g, b) != (255, 255, 255):  # Solo pixeles con marca
                vecinos = {}
                for dy in range(-radio, radio + 1):
                    for dx in range(-radio, radio + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < ancho and 0 <= ny < alto:
                            pr, pg, pb = pixeles[nx, ny]
                            if not (pr > pg + 40 and pr > pb + 40):  # evitar rojos
                                color = (pr, pg, pb)
                                if color in vecinos:
                                    vecinos[color] += 1
                                else:
                                    vecinos[color] = 1
                if vecinos:
                    # Buscar el color con mayor frecuencia manualmente
                    color_mas_comun = None
                    max_repeticiones = 0
                    for color, conteo in vecinos.items():
                        if conteo > max_repeticiones:
                            color_mas_comun = color
                            max_repeticiones = conteo
                    pixeles[x, y] = color_mas_comun
    return nueva_imagen


def distancia_rgb(c1, c2):
    '''
    Calcula la distancia euclidiana entre dos colores RGB.
    :param c1: Primer color (r, g, b)
    :param c2: Segundo color (r, g, b)
    :return: Distancia euclidiana entre los dos colores.
    '''
    return sum((a - b) ** 2 for a, b in zip(c1, c2))

def reemplazar_por_vecino_mas_cercano(imagen, marca, tamano_matriz):
    '''
    Funcion que reemplaza los píxeles de la imagen con la marca de agua por el color más cercano
    de su vecindad.
    Parametros:
    imagen: Imagen original con la marca de agua.
    marca: Imagen de la marca de agua.
    tamano_matriz: Tamaño de la matriz de búsqueda.
    
    Retorna:
    nueva_imagen: Imagen con la marca de agua reemplazada por el color más cercano.
    '''
    nueva_imagen = imagen.copy()
    pixeles = nueva_imagen.load()
    marca_px = marca.load()
    ancho, alto = imagen.size
    radio = tamano_matriz // 2
    for y in range(alto):
        for x in range(ancho):
            r, g, b = marca_px[x, y]
            if r > g + 40 and r > b + 40:
                color_original = pixeles[x, y]
                mejor_color = None
                menor_distancia = float('inf')
                for dy in range(-radio, radio + 1):
                    for dx in range(-radio, radio + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < ancho and 0 <= ny < alto:
                            pr, pg, pb = pixeles[nx, ny]
                            if not (pr > pg + 40 and pr > pb + 40):
                                dist = distancia_rgb(color_original, (pr, pg, pb))
                                if dist < menor_distancia:
                                    menor_distancia = dist
                                    mejor_color = (pr, pg, pb)
                if mejor_color:
                    pixeles[x, y] = mejor_color
    return nueva_imagen



if __name__ == '__main__':
    '''
    Primera imagen:
    Se retiro la marca de agua de la imagen 1.jpg
    Se guardo la imagen sin marca de agua como 1_sin_ma.png
    '''    
    imagen1 = Image.open("img_con_ma/1.jpg")
    primer_marca = extraer_rojo(imagen1)    
    primer_marca = eliminar_pixeles_grises(primer_marca, 25)
    
    imagen1_temporal = barrer_marca_agua(imagen1, primer_marca, 3)
    imagen1_temporal = barrer_marca_agua(imagen1_temporal, primer_marca, 3)

    primer_marca = extraer_rojo(imagen1_temporal)    
    primer_marca = eliminar_pixeles_grises(primer_marca, 15)

    rojo_prom = get_rojo_promedio(primer_marca)
    imagen1_temporal = demezclar_marca_agua(imagen1_temporal, primer_marca, rojo_prom, 0.4)
    imagen1_temporal = incrementar_brillo_marca_agua(imagen1_temporal, primer_marca, 1.3)

    for i in range (5):
        imagen1_temporal = reemplazar_por_vecino_mas_cercano(imagen1_temporal, primer_marca, 3)
        
    copia_para_mezcla = imagen1_temporal.copy()
    copia_para_mezcla = convolucion_paralela(copia_para_mezcla, primer_marca, matriz_bsharp, fact_bsharp, bias_bsharp)
    imagen1_temporal = fusionar_imagenes_por_marca(imagen1_temporal, copia_para_mezcla, primer_marca)
    imagen1_temporal = barrer_marca_agua(imagen1_temporal, primer_marca, 3)

    imagen1_temporal.save("img_sin_ma/1_sin_ma.png")
    

    '''
    Segunda imagen:
    Se retiro la marca de agua de la imagen 6.jpg
    Se guardo la imagen sin marca de agua como 6_sin_ma.png
    '''
    imagen2 = Image.open("img_con_ma/6.jpg")
    segunda_marca = extraer_rojo(imagen2)   
    segunda_marca = eliminar_pixeles_grises(segunda_marca, 20)
    imagen2_temporal = barrer_marca_agua(imagen2, segunda_marca, 7)

    for i in range(2):
        segunda_marca = extraer_rojo(imagen2)   
        segunda_marca = eliminar_pixeles_grises(segunda_marca, 20)
        imagen2_temporal = barrer_marca_agua(imagen2, segunda_marca, 5)
    
    segunda_marca = extraer_rojo(imagen2_temporal)    
    segunda_marca = eliminar_pixeles_grises(segunda_marca, 18)
    
    rojo_prom2 = get_rojo_promedio(segunda_marca)

    imagen2_temporal = demezclar_marca_agua(imagen2_temporal, segunda_marca, rojo_prom2, 0.8)
    imagen2_temporal = incrementar_brillo_marca_agua(imagen2_temporal, segunda_marca, 2.2)

    copia_mezcla2 = imagen2_temporal.copy()
    copia_mezcla2 = convolucion_paralela(copia_mezcla2, segunda_marca, matriz_bsharp, fact_bsharp, bias_bsharp)
    
    
    imagen2_temporal = convolucion_paralela(imagen2_temporal, segunda_marca, matriz_media, fact_m, bias_m)
    imagen2_temporal = fusionar_imagenes_por_marca(imagen2_temporal, copia_mezcla2, segunda_marca)

          
    for i in range(5):
        segunda_marca = extraer_rojo(imagen2_temporal)    
        segunda_marca = eliminar_pixeles_grises(segunda_marca, 18)
        imagen2_temporal = barrer_marca_agua(imagen2_temporal, segunda_marca, 3)  

    imagen2_temporal = fusionar_imagenes_por_marca(imagen2_temporal, copia_mezcla2, segunda_marca)
    imagen2_temporal = incrementar_brillo_marca_agua(imagen2_temporal, segunda_marca, 1.5)

    for i in range (5):
        imagen2_temporal = reemplazar_por_gris_mas_cercano(imagen2_temporal, segunda_marca)   

    copia_mezcla2 = imagen2_temporal.copy()
    copia_mezcla2 = convolucion_paralela(copia_mezcla2, segunda_marca, matriz_bsharp, fact_bsharp, bias_bsharp)
    imagen2_temporal = barrer_marca_agua(imagen2_temporal, segunda_marca, 3)
    imagen2_temporal = fusionar_imagenes_por_marca(imagen2_temporal, copia_mezcla2, segunda_marca)
    
    imagen2_temporal.save("img_sin_ma/6_sin_ma.png")
       

    '''
    Tercera imagen:
    Se retiro la marca de agua de la imagen 8.jpg
    Se guardo la imagen sin marca de agua como 8_sin_ma.png
    '''
    imagen3 = Image.open("img_con_ma/8.jpg")
    tercera_marca = extraer_rojo(imagen3)    
    tercera_marca = eliminar_pixeles_grises(tercera_marca, 20)
    tercera_marca = convolucion_paralela(tercera_marca, tercera_marca, matriz_media, fact_m, bias_m)
    imagen3_temporal = barrer_marca_agua(imagen3, tercera_marca, 3)

    for i in range(1):
        imagen3_temporal = barrer_marca_agua(imagen3_temporal, tercera_marca, 3)

    tercera_marca = extraer_rojo(imagen3_temporal)
    tercera_marca = eliminar_pixeles_grises(tercera_marca, 20)    
    

    rojo_prom3 = get_rojo_promedio(tercera_marca)
    imagen3_temporal = demezclar_marca_agua(imagen3_temporal, tercera_marca, rojo_prom3, 0.5)
    imagen3_temporal = incrementar_brillo_marca_agua(imagen3_temporal, tercera_marca, 1.7)
    copia_mezcla3 = imagen3_temporal.copy()
    copia_mezcla3 = convolucion_paralela(copia_mezcla3, tercera_marca, matriz_bsharp, fact_bsharp, bias_bsharp)
    imagen3_temporal = fusionar_imagenes_por_marca(imagen3_temporal, copia_mezcla3, tercera_marca)
    imagen3_temporal = convolucion_paralela(imagen3_temporal, tercera_marca, matriz_media, fact_m, bias_m)
    imagen3_temporal = fusionar_imagenes_por_marca(imagen3_temporal, copia_mezcla3, tercera_marca)
    imagen3_temporal = convolucion_paralela(imagen3_temporal, tercera_marca, matriz_media, fact_m, bias_m)
    imagen3_temporal.save("img_sin_ma/8_sin_ma.png")      


    '''
    Cuarta imagen:
    Se retiro la marca de agua de la imagen 3.jpg
    Se guardo la imagen sin marca de agua como 3_sin_ma.png
    '''
    imagen4 = Image.open("img_con_ma/3.jpg")
    cuarta_marca = extraer_rojo(imagen4) 
    cuarta_marca = eliminar_pixeles_grises(cuarta_marca, 15)
    imagen4_temporal = barrer_marca_agua(imagen4,cuarta_marca, 7) 
    
    for i in range (10):
        cuarta_marca = extraer_rojo(imagen4_temporal) 
        cuarta_marca = eliminar_pixeles_grises(cuarta_marca, 75)
        imagen4_temporal = barrer_marca_agua(imagen4_temporal, cuarta_marca, 7)  
    
    cuarta_marca = extraer_rojo(imagen4_temporal) 
    cuarta_marca = eliminar_pixeles_grises(cuarta_marca, 15)
    imagen4_temporal = barrer_marca_agua(imagen4_temporal,cuarta_marca, 7) 

    imagen4_temporal = reemplazar_por_vecinos_dominantes(imagen4_temporal, cuarta_marca, 3)
    imagen4_temporal = reemplazar_por_vecinos_dominantes(imagen4_temporal, cuarta_marca, 3)
    imagen4_temporal = convolucion_paralela(imagen4_temporal, cuarta_marca, matriz_bsharp, fact_bsharp, bias_bsharp)
    
    for i in range (5):
        imagen4_temporal = reemplazar_por_vecino_mas_cercano(imagen4_temporal, cuarta_marca, 3)  

    imagen4_temporal.save("img_sin_ma/3_sin_ma.png")
    
    print("Se ha eliminado las marcas de agua de las imagenes 1.jpg, 6.jpg, 8.jpg y 3.jpg")
    print("Las imagenes sin marcas de agua se guardaron como 1_sin_ma.png, 6_sin_ma.png, 8_sin_ma.png y 3_sin_ma.png en la carpeta img_sin_ma")
    