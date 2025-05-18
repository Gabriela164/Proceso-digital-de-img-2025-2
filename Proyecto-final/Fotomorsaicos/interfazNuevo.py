import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from generadorMorsaicos import *


def load_image():
    '''
    Funcion para cargar la imagen del directorio del usuario
    '''
    # Original_image: imagen original
    # filtered_image: imagen filtrada (original despúes de aplicar el filtro)
    global original_image, filtered_image
    
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg"), ("Image Files", "*.jpeg"), ("Image Files", "*.png")])
    
    if file_path:
        original_image = Image.open(file_path)
        filtered_image = original_image.copy()
        show_images()


def apply_filter(filter_type):
    global filtered_image
    global current_filter
    
    colors = "./colores/colors.txt" 
    imagenes = "./imagenes"   

    if filter_type == "Morsaico imagen":
        # Mostrar mensaje de carga
        status_label.config(text="Generando morsaico en imagen, podría tardar unos minutos... por favor espere.", fg="#bf0079")
        root.update_idletasks()  # Fuerza la actualización de la UI
        
        filtered_image = img_mosaic(original_image, colors, 18, imagenes, 1) # Generamos la imagen morsaico
        status_label.config(text="Listo, el morsaico (IMAGEN) se ha generado.", fg="#258900")         # Actualizamos el estado al finalizar

    elif filter_type == "Morsaico html":
        # Mostrar mensaje de carga
        status_label.config(text="Generando morsaico en html, podría tardar unos minutos... por favor espere.", fg="#bf0079")
        root.update_idletasks()  # Fuerza la actualización de la UI
        
        # Generamos el HTML del morsaico
        with open(colors, "r") as file:
            mosaic = html_mosaic(original_image, colors, 18, imagenes,  1)   
                                
        with open("morsaicoHTML.html", "w", encoding="utf-8") as html_output:
            html_output.write(mosaic)
            
        filtered_image = original_image.copy()  # Mantener la imagen original para mostrarla
        status_label.config(text="Listo, el morsaico (HTML) se ha guardado en la misma carpeta del script interfaz.py", fg="#258900") # Actualizamos el estado al finalizar
    else:
        filtered_image = "Filtro NO reconocido"
        status_label.config(text="Filtro no reconocido", fg="red")
        
    current_filter.set(f"Filtro aplicado: {filter_type}")
    show_images()


# Función para mostrar las imágenes en la interfaz
def show_images():
    global original_image, filtered_image
    
    # Redimensionar las imágenes
    original_image_resized = original_image.resize((650, 650))
    filtered_image_resized = filtered_image.resize((650, 650))

    # Convertir las imágenes a formato que Tkinter pueda mostrar
    original_image_tk = ImageTk.PhotoImage(original_image_resized)
    filtered_image_tk = ImageTk.PhotoImage(filtered_image_resized)

    # Mostrar las imágenes en las etiquetas correspondientes
    img_label_right.config(image=filtered_image_tk)
    img_label_right.image = filtered_image_tk
    
    img_label_left.config(image=original_image_tk)
    img_label_left.image = original_image_tk
    
# Función para guardar la imagen resultante
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
    if file_path:
        filtered_image.save(file_path)

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------- Creamos la ventana principal------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
root = tk.Tk()
root.title("Proyecto Final: Generador de Morsaicos")

# Variables globales
original_image = None
filtered_image = None
current_filter = tk.StringVar() # Variable para mostrar el filtro actual
current_filter.set("Filtro aplicado: Ninguno")  # Valor por defecto

# Etiqueta para mostrar mensajes de estado (abajo del todo)
status_label = tk.Label(root, text="Esperando acción del usuario...", font=("Arial", 15), fg="#000000")
status_label.grid(row=3, column=0, columnspan=2, pady=(10, 15))

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
filter_menu.add_cascade(label="Proyecto final", menu=tarea1_menu)

#1. Filtro morsaico
tarea1_menu.add_command(label="Generar morsaico en formato IMAGEN", command=lambda: apply_filter("Morsaico imagen"))
tarea1_menu.add_command(label="Generar morsaico en formato HTML", command=lambda: apply_filter("Morsaico html"))

# Ejecuta la interfaz de usuario
root.mainloop()



