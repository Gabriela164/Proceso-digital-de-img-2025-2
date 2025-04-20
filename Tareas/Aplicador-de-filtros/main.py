import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Importar funciones de los filtros
from Tareas.Tarea1.Tarea1PD import *
from Tareas.Tarea2.Tarea2PD import *
from Tareas.Tarea2.Fuentes import * 
from Tareas.MarcaDeAgua.Tarea_marca_de_agua import *
from Tareas.Tarea3.Tarea_img_recursivas import *
from Tareas.Tarea3.CSV import *
from Tareas.Tarea_dithering.tarea_dithering import *
from Tareas.Tarea_semitonos_dados.semitonos_dados import dices_filter, semitones
from Tareas.Tarea_oleo.tarea_oleo import watercolor, grey_scale
from Tareas.Tarea_ATT.ATT import *
from Tareas.Tarea_mosaicos_redondos_estrellas.circle_star import *

def load_image():
    '''
    Funcion para cargar la imagen del directorio del usuario
    '''
    global original_image, filtered_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg"), ("Image Files", "*.jpeg"), ("Image Files", "*.png")])
    if file_path:
        original_image = Image.open(file_path)
        filtered_image = original_image.copy()
        show_images()

# Función para aplicar los filtros
def apply_filter(filter_type):
        
    global filtered_image # Variable donde guardaremos la imagen despues de aplicarle el filtro 
    global current_filter # Variable para mostrar el filtro actual
    
    # Aplicar el filtro seleccionado
    if filter_type == "Random dithering":
        filtered_image = dithering_version(original_image,1)
    elif filter_type == "Clustered dithering":
        filtered_image = dithering_version(original_image, 2)
    elif filter_type == "Dispersed dithering":
        filtered_image = dithering_version(original_image, 3)
    elif filter_type == "Dispersed 2x2":
        filtered_image = dithering_version(original_image, 4)
    elif filter_type == "Dispersed 4x4":
        filtered_image = dithering_version(original_image, 5)
    elif filter_type == "Floyd-Steinberg Dithering":
        filtered_image = dithering_version(original_image, 6)
    elif filter_type == "Fake Floyd-Steinberg Dithering":
        filtered_image = dithering_version(original_image, 7)
    elif filter_type == "Jarvis, Judice, Ninke":
        filtered_image = dithering_version(original_image, 8)
    elif filter_type == "mosaico":
        filtered_image = filtro_mosaico(original_image)
    elif filter_type == "ponderado":
        filtered_image = filtro_gris_ponderado(original_image)
    elif filter_type == "promedio":
        filtered_image = filtro_gris_promedio(original_image)
    elif filter_type == "alto contraste":
        filtered_image = filtro_alto_contraste(original_image)
    elif filter_type == "inverso contraste":
        filtered_image = filtro_alto_contraste_inverso(original_image)
    elif filter_type == "mica roja":
        filtered_image = filtro_mica_roja(original_image) 
    elif filter_type == "mica verde":
        filtered_image = filtro_mica_verde(original_image) 
    elif filter_type == "mica azul":
        filtered_image = filtro_mica_azul(original_image) 
    elif filter_type == "RGB combinado":
        filtered_image = filtro_mica_combinado(original_image) 
    elif filter_type == "brillo":
        filtered_image = filtro_brillo(original_image)
    elif filter_type == "letras color":
        filtered_image = letter_with_color(original_image, letra="M")
    elif filter_type == "letras gris":
        filtered_image = letter_with_grayscale(original_image, letra="M")
    elif filter_type == "letras bn":
        filtered_image = letters_bn(original_image)
    elif filter_type == "texto con color":
        filtered_image = color_with_text(original_image, texto="PROCESO DIGITAL DE IMAGENES 2025")
    elif filter_type == "domino blanco":
        filtered_image = domino(original_image, fuente="blanco")
    elif filter_type == "domino negro":
        filtered_image = domino(original_image, fuente="negro")
    elif filter_type == "naipes":
        filtered_image = naipes(original_image)
    elif filter_type == "recursivas":
        filtered_image = recursive_image_generation(original_image, original_image, 25, 25)
    elif filter_type == "marca de agua":
        filtered_image = apply_watermark(original_image)
    elif filter_type == "semitonos":
        filtered_image = semitones(original_image, 6, "white", "black")
    elif filter_type == "dados":
        filtered_image = dices_filter(original_image, 7, (0,0,0), (255,255,255))
    elif filter_type == "oleo color":
        filtered_image = watercolor(original_image, 15, 1)
    elif filter_type == "oleo blanco y negro":
        filtered_image = watercolor(original_image, 15, 2)
    elif filter_type == "efecto att":
        filtered_image = filter_att(original_image, stripe_thickness=4)
    elif filter_type == "mosaico circulo":
        filtered_image = mosaics_with_shape(original_image, "Tareas/Tarea_mosaicos_redondos_estrellas/shapes/circle_white.png", 15, 1)
    elif filter_type == "mosaico estrella":
        filtered_image = mosaics_with_shape(original_image, "Tareas/Tarea_mosaicos_redondos_estrellas/shapes/star_white.png", 25, 0)
    else:
        filtered_image = "Filtro NO reconocido"
        
    # Guardamos el filtro actual aplicado
    current_filter.set(f"Filtro aplicado: {filter_type}") 
    show_images()

# Función para mostrar las imágenes en la interfaz
def show_images():
    global original_image, filtered_image
    
    # Redimensionar las imágenes
    original_image_resized = original_image.resize((550, 550))
    filtered_image_resized = filtered_image.resize((550, 550))

    # Convertir las imágenes a formato que Tkinter pueda mostrar
    original_image_tk = ImageTk.PhotoImage(original_image_resized)
    filtered_image_tk = ImageTk.PhotoImage(filtered_image_resized)

    # Mostrar las imágenes en las etiquetas correspondientes
    img_label_right.config(image=filtered_image_tk)
    img_label_right.image = filtered_image_tk
    
    img_label_left.config(image=original_image_tk)
    img_label_left.image = original_image_tk
    

# Función para guardar la imagen filtrada
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
    if file_path:
        filtered_image.save(file_path)

# Crear la ventana principal
root = tk.Tk()
root.title("Filtros en imágenes")

# Variables globales
original_image = None
filtered_image = None
current_filter = tk.StringVar() # Variable para mostrar el filtro actual
current_filter.set("Filtro aplicado: Ninguno")  # Valor por defecto

# Crear etiquetas para los títulos sobre las imágenes
title_left = tk.Label(root, text="Imagen original", font=("Arial", 12, "bold"))
title_left.grid(row=0, column=0, padx=10, pady=5, sticky="n")

title_right = tk.Label(root, textvariable=current_filter, font=("Arial", 12, "bold"))
title_right.grid(row=0, column=1, padx=10, pady=5, sticky="n")

# Crear las etiquetas para mostrar las imágenes
img_label_left = tk.Label(root)
img_label_left.grid(row=1, column=0, padx=10, pady=10)

img_label_right = tk.Label(root)
img_label_right.grid(row=1, column=1, padx=10, pady=10)

# Crear botones para cargar la imagen, aplicar filtros y guardar
btn_load = tk.Button(root, text="Cargar Imagen", command=load_image)
btn_load.grid(row=2, column=0, pady=10, padx=10)

btn_save = tk.Button(root, text="Guardar Imagen", command=save_image)
btn_save.grid(row=2, column=1, pady=10, padx=10)

# Crear menu principal superior
filter_menu = tk.Menu(root)
root.config(menu=filter_menu)

#Opción filtros tarea 1 y lo agregamos al menu
tarea1_menu = tk.Menu(filter_menu, tearoff=0)
filter_menu.add_cascade(label="Filtros tarea 1", menu=tarea1_menu)

#Opción filtros tarea 2 y lo agregamos al menu
tarea2_menu = tk.Menu(filter_menu, tearoff=0)
filter_menu.add_cascade(label="Filtros tarea 2", menu=tarea2_menu)

#Opción filtros tarea 3 img recursivas y lo agregamos al menu
tarea_recursiva_menu = tk.Menu(filter_menu, tearoff=0)
filter_menu.add_cascade(label="Filtros tarea 3", menu=tarea_recursiva_menu)

#Opción filtros dithering y lo agregamos al menu
filters_dithering = tk.Menu(filter_menu, tearoff=0)
filter_menu.add_cascade(label="Filtros dithering", menu=filters_dithering)

#Opción filtros semitonos y dados y lo agregamos al menu
filters_semitones_dice = tk.Menu(filter_menu, tearoff=0)
filter_menu.add_cascade(label="Filtros semitonos y dados", menu=filters_semitones_dice)

#Opción filtros oleo con color y oleo en blanco y negro
filters_oleo = tk.Menu(filter_menu, tearoff=0)
filter_menu.add_cascade(label="Filtros oleo", menu=filters_oleo)

#Opción filtros ATT y lo agregamos al menu
filters_ATT = tk.Menu(filter_menu, tearoff=0)
filter_menu.add_cascade(label="Filtro ATT", menu=filters_ATT)

#Opción filtros mosaicos figuras y lo agregamos al menu
filters_mosaicos_figuras = tk.Menu(filter_menu, tearoff=0)
filter_menu.add_cascade(label="Filtros mosaicos figuras", menu=filters_mosaicos_figuras)

'''
Agregamos opciones a la sección de filtros tarea 1
1. Filtro mosaico
2. Filtro escala de grises (Promedio RGB)
3. Filtro escala de grises (Ponderado (.30*r + .70*g + .10*b))
4. Filtro alto contraste 
5. Filtro inverso contraste 
6. Filtro mica RGB por separado 
7. Filtro mica RGB combinados
8. Filtro brillo
'''
tarea1_menu.add_command(label="Mosaico", command=lambda: apply_filter("mosaico"))
tarea1_menu.add_command(label="Escala de grises ponderado", command=lambda: apply_filter("ponderado"))
tarea1_menu.add_command(label="Escala de grises promedio", command=lambda: apply_filter("promedio"))
tarea1_menu.add_command(label="Alto contraste", command=lambda: apply_filter("alto contraste"))
tarea1_menu.add_command(label="Inverso contraste", command=lambda: apply_filter("inverso contraste"))
tarea1_menu.add_command(label="Mica roja", command=lambda: apply_filter("mica roja"))
tarea1_menu.add_command(label="Mica verde", command=lambda: apply_filter("mica verde"))
tarea1_menu.add_command(label="Mica azul", command=lambda: apply_filter("mica azul"))
tarea1_menu.add_command(label="Mica combinado", command=lambda: apply_filter("RGB combinado"))
tarea1_menu.add_command(label="Brillo", command=lambda: apply_filter("brillo"))

'''
Agregamos opciones a la sección de filtros tarea 2
'''
tarea2_menu.add_command(label="Letras con color", command=lambda: apply_filter("letras color"))
tarea2_menu.add_command(label="Letras en escala de grises", command=lambda: apply_filter("letras gris"))
tarea2_menu.add_command(label="Letras y signos en blanco y negro", command=lambda: apply_filter("letras bn"))
tarea2_menu.add_command(label="Texto con color", command=lambda: apply_filter("texto con color"))
tarea2_menu.add_command(label="Domino blanco", command=lambda: apply_filter("domino blanco"))
tarea2_menu.add_command(label="Domino negro", command=lambda: apply_filter("domino negro"))
tarea2_menu.add_command(label="Naipes", command=lambda: apply_filter("naipes"))

'''Argeamos las opciones a la sección de la tarea 3'''
tarea_recursiva_menu.add_command(label="Imagenes recursivas", command=lambda: apply_filter("recursivas"))
tarea_recursiva_menu.add_command(label="Marca de agua", command=lambda: apply_filter("marca de agua"))

'''
Agregamos opciones en la sección de filtros dithering 
Opcion 1: Random dithering
Opcion 2: Clustered dithering
Opcion 3: Dispersed dithering
Opcion 4; Dispersed 2x2 dithering
Opcion 5: Dispersed 4x4 dithering
Opcion 6: Floyd-Steinberg dithering
Opcion 7: Fake Floyd-Steinberg dithering
Opción 8: Jarvis, Judice, Ninke dithering
'''
filters_dithering.add_command(label="Random Dithering", command=lambda: apply_filter("Random dithering"))
filters_dithering.add_command(label="Clustered Dithering", command=lambda: apply_filter("Clustered dithering")) 
filters_dithering.add_command(label="Dispersed Dithering", command=lambda: apply_filter("Dispersed dithering")) 
filters_dithering.add_command(label="Dispersed 2x2", command=lambda: apply_filter("Dispersed 2x2"))
filters_dithering.add_command(label="Dispersed 4x4", command=lambda: apply_filter("Dispersed 4x4"))
filters_dithering.add_command(label="Floyd-Steinberg Dithering", command=lambda: apply_filter("Floyd-Steinberg Dithering"))
filters_dithering.add_command(label="Fake Floyd-Steinberg Dithering", command=lambda: apply_filter("Fake Floyd-Steinberg Dithering"))
filters_dithering.add_command(label="Jarvis, Judice, Ninke", command=lambda: apply_filter("Jarvis, Judice, Ninke"))

'''
Agregamos las dos opciones de semitonos y dados dentro de la sección de filtros semitonos y dados
Opción 1: Semitonos
Opción 2: Dados
'''
filters_semitones_dice.add_command(label="Semitonos", command=lambda: apply_filter("semitonos"))
filters_semitones_dice.add_command(label="Dados", command=lambda: apply_filter("dados"))

'''
Agregamos la opción de oleo 
Opción 1: Oleo color
Opción 2: Oleo blanco y negro
'''
filters_oleo.add_command(label="Oleo color", command=lambda: apply_filter("oleo color"))
filters_oleo.add_command(label="Oleo blanco y negro", command=lambda: apply_filter("oleo blanco y negro"))

'''
Agregamos la opción de filtro ATT
Opción 1: Efecto AT&T
'''
filters_ATT.add_command(label="Efecto AT&T", command=lambda: apply_filter("efecto att"))

'''
Agregamos las opciones de mosaicos con figuras
Opción 1: Mosaico circulo
Opción 2: Mosaico estrella
'''
filters_mosaicos_figuras.add_command(label="Mosaico circulo", command=lambda: apply_filter("mosaico circulo"))
filters_mosaicos_figuras.add_command(label="Mosaico estrella", command=lambda: apply_filter("mosaico estrella"))

# Ejecuta la interfaz de usuario
root.mainloop()
