import numpy as np
from PIL import Image

'''
Script que ecualiza el histograma de una imagen en escala de grises.
Es decir, mejora el contraste de la imagen al redistribuir los niveles de gris.

Autor: Gabriela López Diego
Fecha: Mayo 2025
'''

def ecualizar_histograma(imagen):
    """
    Función para ecualizar el histograma de una imagen en escala de grises.
    """
    # Convertir la imagen a escala de grises
    imagen = imagen.convert('L')
    imagen = np.array(imagen) # Utiliza un arreglo numpy para facilitar el procesamiento

    # Calcular el histograma, es decir, la frecuencia de cada nivel de gris
    histograma, bins = np.histogram(imagen.flatten(), bins=256, range=[0, 256])

    # Calcular la función de distribución acumulativa (CDF)
    cdf = histograma.cumsum()  # Suma acumulativa
    cdf_normalizada = cdf * histograma.max() / cdf.max()  # Normalización para visualizar

    # Ecualizar usando la CDF
    cdf_m = np.ma.masked_equal(cdf, 0)  # Enmascarar valores 0 para evitar divisiones
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())  # Normalización
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')  # Rellenar valores enmascarados con 0

    # Aplicar la transformación a la imagen
    imagen_ecualizada = cdf[imagen]
    imagen_ecualizada = Image.fromarray(imagen_ecualizada)  # Convertir a imagen
    
    return imagen_ecualizada
    