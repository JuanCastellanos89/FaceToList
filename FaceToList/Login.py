import tkinter as tk
from PIL import Image, ImageTk
import math
import mediapipe as mp
import os
import cv2
import imutils
import numpy as np
import face_recognition as fr
import Lectura
from tkinter import filedialog, messagebox
import pandas as pd


def Profile():
    global step, conteo, UserName, OutFolderPathUser, imageBtnRegresar, pantalla4, imageBtnAsistencia, imageBtnExportar
    # reset variables
    conteo = 0
    step = 0

    # new window
    pantalla4 = tk.Toplevel()
    pantalla4.title("FaceToList Perfil")
    pantalla4.geometry("800x600")

    # Cargar la imagen de fondo
    bg_image = Image.open("assets/FondoPerfil.jpg")
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Crear un widget Canvas
    canvas = tk.Canvas(pantalla4, width=800, height=600)
    canvas.pack(fill="both", expand=True)

    # Añadir la imagen de fondo al Canvas
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Mantener una referencia de las imágenes
    canvas.image_bg = bg_photo

    # Botón para cerrar la ventana de registro y volver a la ventana principal
    imageBtnRegresar = tk.PhotoImage(
    file="C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/BtnRegresar.png")
    boton_cerrar = tk.Button(pantalla4, image=imageBtnRegresar, command=lambda: cerrar_ventana_loginD(pantalla4))
    boton_cerrar.place(x=300, y=300)

    imageBtnAsistencia = tk.PhotoImage(
        file="C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/BtnAsistencia.png")
    boton_Asistencia = tk.Button(pantalla4, image=imageBtnAsistencia, command=Lectura.mostrar_ventana)

    boton_Asistencia.place(x=300, y=200)

    imageBtnExportar = tk.PhotoImage(file="C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/BtnExportar.png")
    boton_exportar = tk.Button(pantalla4, image=imageBtnExportar, command=exportar_a_excel)
    boton_exportar.place(x=300, y=400)


    #extract file
    UserFile = open(f"{OutFolderPathUser}/{UserName}.txt", 'r')
    InfoUser = UserFile.read().split(',')
    Nombres = InfoUser[0]
    Apellidos = InfoUser[1]
    Documento = InfoUser[2]
    UserFile.close()

    #Check alredy exist user
    if Documento in clases:
        canvas.create_text(100, 100, text=f"WELCOME: {Nombres} {Apellidos}", fill="white", anchor="nw",
                           font=("Helvetica", 28, "bold"))


def exportar_a_excel():
    # Verificar si Registro.csv está vacío
    registro_path = "Registro.csv"
    if not os.path.exists(registro_path) or os.path.getsize(registro_path) == 0:
        messagebox.showinfo("Información", "No se ha tomado asistencia.")
        return

    # Leer el archivo CSV
    df = pd.read_csv(registro_path)

    # Pedir al usuario donde guardar el archivo Excel
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])

    if file_path:
        # Guardar DataFrame como archivo Excel
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Exportar a Excel", "El archivo ha sido exportado exitosamente.")

        # Borrar el contenido de Registro.csv
        open(registro_path, 'w').close()

def cerrar_ventana_loginD(pantalla4):
    # Destruye la ventana de registro
    pantalla4.destroy()

def Code_Face(images):
    # face code
    List_code = []
    # iterar imagenes
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        codings = fr.face_encodings(img)
        if len(codings) > 0:
            cod = codings[0]
            # save list
            List_code.append(cod)
        else:
            print(f"No se encontraron caras en una de las imágenes: {img}")
    return List_code


#def closeWindow2(pantalla3):
def closeWindow2():
    global step, conteo
    #reset variables
    conteo = 0
    step = 0
    pantalla3.destroy()


#loggin biometric function
def loggin_biometric():
    global LogUser, LogPass, capture, lblVideo, pantalla3, FaceCode, clases, images, step, parpadeo, conteo, UserName
    # check capture
    if capture is not None:
        ret, frame = capture.read()

        # frame save
        frameSave = frame.copy()

        # resize
        frame = imutils.resize(frame, width=1280)

        # frame rgb
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # frame show
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret == True:
            # inference mech facial
            result = FaceMesh.process(frameRGB)
            # result list
            px = []
            py = []
            lista = []

            if result.multi_face_landmarks is not None:
                for rostros in result.multi_face_landmarks:
                    # draw
                    mpDraw.draw_landmarks(frame, rostros, FaceMeshObject.FACEMESH_CONTOURS, ConfigDraw, ConfigDraw)
                    # exrtact points
                    for id, points in enumerate(rostros.landmark):
                        # info img
                        h, w, c = frame.shape
                        cx, cy = int(points.x * w), int(points.y * h)
                        px.append(cx)
                        py.append(cy)
                        lista.append([id, cx, cy])
                        # validate 468 points
                        if len(lista) == 468:
                            # ojo derecho
                            cx1, cy1 = lista[145][1:]
                            cx2, cy2 = lista[159][1:]
                            longitud1 = math.hypot(cx2 - cx1, cy2 - cy1)

                            # ojo izquierdo
                            cx3, cy3 = lista[374][1:]
                            cx4, cy4 = lista[386][1:]
                            longitud2 = math.hypot(cx4 - cx3, cy4 - cy3)

                            # parietal derecho
                            cx5, cy5 = lista[139][1:]
                            # parietal Izquierdo
                            cx6, cy6 = lista[368][1:]

                            # Ceja derecha
                            cx7, cy7 = lista[70][1:]
                            # ceja izquierda
                            cx8, cy8 = lista[300][1:]

                            # face detect
                            resultFace = FaceDetectObject.process(frameRGB)
                            if resultFace.detections is not None:
                                for face in resultFace.detections:
                                    # recuadro bbox id score
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box
                                    # trheshold
                                    if score > confThreeshold:
                                        # convert to pixels coord bbox
                                        xi, yi, w1, h1 = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, w1, h1 = int(xi * w), int(yi * h), int(w1 * w), int(h1 * h)

                                        # offset
                                        offsetW = (offsetX / 100) * w1
                                        xi = int(xi - int(offsetW / 2))
                                        w1 = int(w1 + offsetW)
                                        xf = xi + w1

                                        offsetH = (offsetY / 100) * h1
                                        yi = int(yi - offsetH)
                                        h1 = int(h1 + offsetH)
                                        yf = yi + h1

                                        # Error
                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if w1 < 0: w1 = 0
                                        if h1 < 0: h1 = 0

                                        # steps verification
                                        if step == 0:
                                            # draw rectanlge
                                            cv2.rectangle(frame, (xi, yi, w1, h1), (0, 0, 255), 2)
                                            # step 0
                                            hs0, ws0, c = img_step0.shape
                                            frame[50:50 + hs0, 50:50 + ws0] = img_step0
                                            # step 1
                                            hs1, ws1, c = img_step1.shape
                                            frame[50:50 + hs1, 1030:1030 + ws1] = img_step1
                                            # step 2
                                            hs2, ws2, c = img_step2.shape
                                            frame[270:270 + hs2, 1030:1030 + ws2] = img_step2
                                            # Center face
                                            if cx7 > cx5 and cx8 < cx6:
                                                # IMG check
                                                hCheck, wCheck, c = img_check.shape
                                                frame[165:165 + hCheck, 1105:1105 + wCheck] = img_check
                                                # count parpadeo
                                                if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False:
                                                    conteo += 1
                                                    parpadeo = True
                                                elif longitud1 > 10 and longitud2 > 10 and parpadeo == True:
                                                    parpadeo = False
                                                cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070, 375),
                                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                                                if conteo >= 3:
                                                    hCheck, wCheck, c = img_check.shape
                                                    frame[385:385 + hCheck, 1105:1105 + wCheck] = img_check
                                                    # screen capture if open eyes
                                                    if longitud1 > 15 and longitud2 > 15:
                                                        step = 1
                                            else:
                                                conteo = 0
                                        if step == 1:
                                            # draw rectanlge
                                            cv2.rectangle(frame, (xi, yi, w1, h1), (0, 255, 0), 2)
                                            # img liveness
                                            hliv, wliv, c = img_liveness.shape
                                            frame[50:50 + hliv, 50:50 + wliv] = img_liveness

                                            #find faces
                                            facess = fr.face_locations(frameRGB)
                                            facesCod = fr.face_encodings(frameRGB, facess)

                                            # itereacion
                                            for faceCod, faceloc in zip(facesCod, facess):
                                                #match
                                                Match = fr.compare_faces(FaceCode, faceCod)
                                                #extract similitud
                                                simil = fr.face_distance(FaceCode, faceCod)

                                                #min error %
                                                minimo = np.argmin(simil)
                                                if Match[minimo]:
                                                    #extract username
                                                    UserName = clases[minimo].upper()
                                                    Profile()
                                                    #print("Aqui entra a profile")
                                                    #pantalla3.after(2000, lambda: closeWindow2(pantalla3))
                                                    pantalla3.protocol("WM_DELETE_WINDOW", closeWindow2)
        # converter video
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)
        # show video
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, loggin_biometric)

    else:
        capture.release()


def Loggin(root):
    global OutFolderPathFaces, capture, lblVideo, pantalla3, FaceCode, clases, images
    #root.withdraw()


    #DB faces
    images =[]
    clases =[]
    lista =os.listdir(OutFolderPathFaces)

    #read faces
    for lis in lista:
        #read img
        imgdb = cv2.imread(f"{OutFolderPathFaces}/{lis}")
        # save img DB
        images.append(imgdb)
        clases.append(os.path.splitext(lis)[0])
    FaceCode = Code_Face(images)
    # new window
    pantalla3 = tk.Toplevel(root)
    pantalla3.title("FaceToList login")
    pantalla3.geometry("1280x720")
    x_pos = root.winfo_x()
    y_pos = root.winfo_y()
    pantalla3.geometry(f"{1280}x{720}+{x_pos}+{y_pos}")

    # lblVideo
    lblVideo = tk.Label(pantalla3)
    lblVideo.place(x=0, y=0)

    # capture
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture.set(3, 1280)
    capture.set(4, 720)
    loggin_biometric()

# path
OutFolderPathUser = 'C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/DB_FACES_DIR/Docentes/Users'
PathUserCheck = 'C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/DB_FACES_DIR/Docentes/Users/'
OutFolderPathFaces = 'C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/DB_FACES_DIR/Docentes/Faces'


#variables
parpadeo = False
conteo = 0
muestra = 0
step = 0
#offset
offsetX = 15
offsetY = 44
#umbral
confThreeshold = 0.5
#tool drawing
mpDraw = mp.solutions.drawing_utils
ConfigDraw = mpDraw.DrawingSpec(thickness=1, circle_radius=1)
#malla facial mesh faces
FaceMeshObject = mp.solutions.face_mesh
FaceMesh = FaceMeshObject.FaceMesh(max_num_faces=1)
#object face detector
FaceDetect = mp.solutions.face_detection
FaceDetectObject = FaceDetect.FaceDetection(min_detection_confidence=0.5, model_selection=1)


# read img
img_info = cv2.imread('C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/Info.png')
img_check = cv2.imread('C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/Check.png')
img_step0 = cv2.imread('C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/Step0.png')
img_step1 = cv2.imread('C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/Step1.png')
img_step2 = cv2.imread('C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/Step2.png')
img_liveness = cv2.imread('C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/LivenessCheck.png')


# List
info = []

