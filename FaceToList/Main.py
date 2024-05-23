import tkinter as tk
from PIL import Image, ImageTk
from Registro_Docente import mostrar_ventana_registro
from Registro_Estudiante import mostrar_ventana_registro_estudiante
from Login import Loggin

# Crear la ventana principal
root = tk.Tk()

# Configurar el tamaño de la ventana
root.geometry("800x600")

# Título de la ventana
root.title("Face To List")

# Cargar la imagen de fondo
bg_image = Image.open("assets/Fondo1.jpg")  # Reemplaza con la ruta a tu imagen de fondo
bg_image = bg_image.resize((800, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Crear un widget Canvas
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Añadir la imagen de fondo al Canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Cargar la imagen PNG con transparencia
overlay_image = Image.open("assets/Logo.png")  # Reemplaza con la ruta a tu imagen PNG
overlay_image = overlay_image.resize((350, 350), Image.LANCZOS)
overlay_photo = ImageTk.PhotoImage(overlay_image)

# Añadir la imagen transparente sobre el fondo
canvas.create_image(40, 110, image=overlay_photo, anchor="nw")  # Ajusta las coordenadas según sea necesario


# Cargar banner PNG con transparencia
overlay_imageB = Image.open("assets/Banner.png")  # Reemplaza con la ruta a tu imagen PNG
#overlay_imageB = overlay_image.resize((350, 350), Image.LANCZOS)
overlay_photoB = ImageTk.PhotoImage(overlay_imageB)

# Añadir la imagen transparente sobre el fondo
canvas.create_image(100, 0, image=overlay_photoB, anchor="nw")  # Ajusta las coordenadas según sea necesario


# Mantener una referencia de las imágenes
canvas.image_bg = bg_photo
canvas.image_overlay = overlay_photo
canvas.image_overlayB = overlay_photoB



# Botón para abrir la ventana de registro de docente
imageBtnDocente = tk.PhotoImage(file="C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/BtnDocente.png")
boton_registroD = tk.Button(root, image=imageBtnDocente, command=lambda: mostrar_ventana_registro(root))
boton_registroD.place(x=420, y=180)

# Botón para abrir la ventana de registro de estudiante
imageBtnEstudiante = tk.PhotoImage(file="C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/BtnEstudiante.png")
boton_registroE = tk.Button(root, image=imageBtnEstudiante, command=lambda: mostrar_ventana_registro_estudiante(root))
boton_registroE.place(x=420, y=280)

#boton login docente
imageBtnLogin = tk.PhotoImage(file="C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/BtnLogin.png")
boton_loginD = tk.Button(root, image=imageBtnLogin, command=lambda: Loggin(root))
boton_loginD.place(x=420, y=380)



# Iniciar el bucle principal de la aplicación
root.mainloop()


