import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import imutils
import math
import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os



def mostrar_ventana_registro_estudiante(root):
    global ventana_registroE, InputNombresReg, InputApellidosReg, InputDocumentoReg, InputCursoReg, imageBtnRegistrar, imageBtnRegresar
    # Oculta la ventana principal
    root.withdraw()

    # Crea la ventana de registro
    ventana_registroE = tk.Toplevel(root)
    ventana_registroE.title("Registro Estudiante")
    x_pos = root.winfo_x()
    y_pos = root.winfo_y()
    ventana_registroE.geometry(f"{800}x{600}+{x_pos}+{y_pos}")

    # Cargar la imagen de fondo
    bg_image = Image.open("assets/FondoEstudiante.jpg")
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Crear un widget Canvas
    canvas = tk.Canvas(ventana_registroE, width=800, height=600)
    canvas.pack(fill="both", expand=True)

    # Añadir la imagen de fondo al Canvas
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Mantener una referencia de las imágenes
    canvas.image_bg = bg_photo

    # input text loggin
    # nombre
    InputNombresReg = tk.Entry(ventana_registroE, width=26)
    InputNombresReg.place(x=60, y=200)
    # apellidos
    InputApellidosReg = tk.Entry(ventana_registroE, width=26)
    InputApellidosReg.place(x=60, y=300)
    # Documento registro unico
    InputDocumentoReg = tk.Entry(ventana_registroE, width=26)
    InputDocumentoReg.place(x=60, y=400)
    # curso del estudiante
    InputCursoReg = tk.Entry(ventana_registroE, width=26)
    InputCursoReg.place(x=60, y=500)

    imageBtnRegistrar= tk.PhotoImage(file="C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/BtnRegistrar.png")
    boton_Registrar = tk.Button(ventana_registroE, image=imageBtnRegistrar, command=Register)
    boton_Registrar.place(x=550, y=400)

    # Botón para cerrar la ventana de registro y volver a la ventana principal
    imageBtnRegresar = tk.PhotoImage(file="C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/Assets/BtnRegresar.png")
    boton_cerrar = tk.Button(ventana_registroE, image=imageBtnRegresar, command=lambda: cerrar_ventana_registroE(root, ventana_registroE))
    boton_cerrar.place(x=550, y=500)


def cerrar_ventana_registroE(root, ventana_registroE):
    # Destruye la ventana de registro
    ventana_registroE.destroy()

    # Muestra de nuevo la ventana principal
    root.deiconify()

def closeWindow():
    global step, conteo, capture, pantalla2
    # Reset variables
    if capture:
        capture.release()
    conteo = 0
    step = 0
    # Destruye la pantalla2 si existe
    if pantalla2:
        pantalla2.destroy()



#register biometric function
def register_biometric():
    global pantalla2, conteo, parpadeo, img_info, step, capture, lblVideo, RegDocumento, RegNombres, RegApellidos, RegCurso
    #check capture
    if capture is not None:
        ret, frame = capture.read()

        # frame save
        frameSave = frame.copy()

        #resize
        frame = imutils.resize(frame, width=1280)

        #frame rgb
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # frame show
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret == True:
            #inference mech facial
            result = FaceMesh.process(frameRGB)
            # result list
            px = []
            py = []
            lista = []

            if result.multi_face_landmarks is not None:
                for rostros in result.multi_face_landmarks:
                    #draw
                    mpDraw.draw_landmarks(frame, rostros, FaceMeshObject.FACEMESH_CONTOURS, ConfigDraw, ConfigDraw)
                    #exrtact points
                    for id, points in enumerate(rostros.landmark):
                        #info img
                        h, w, c = frame.shape
                        cx, cy = int(points.x * w), int(points.y *h)
                        px.append(cx)
                        py.append(cy)
                        lista.append([id, cx, cy])
                        #validate 468 points
                        if len(lista) == 468:
                            #ojo derecho
                            cx1, cy1 = lista[145][1:]
                            cx2, cy2 = lista[159][1:]
                            longitud1 = math.hypot(cx2-cx1, cy2-cy1)

                            #ojo izquierdo
                            cx3, cy3 = lista[374][1:]
                            cx4, cy4 = lista[386][1:]
                            longitud2 = math.hypot(cx4-cx3, cy4-cy3)

                            #parietal derecho
                            cx5, cy5 = lista[139][1:]
                            #parietal Izquierdo
                            cx6, cy6 = lista[368][1:]

                            #Ceja derecha
                            cx7, cy7 = lista[70][1:]
                            #ceja izquierda
                            cx8, cy8 = lista[300][1:]

                            #face detect
                            resultFace = FaceDetectObject.process(frameRGB)
                            if resultFace.detections is not None:
                                for face in resultFace.detections:
                                #recuadro bbox id score
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box
                                    #trheshold
                                    if score > confThreeshold:
                                        #convert to pixels coord bbox
                                        xi, yi, w1, h1 = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, w1, h1 = int(xi * w), int(yi * h), int(w1 * w), int(h1 * h)


                                        #offset
                                        offsetW = (offsetX / 100) * w1
                                        xi = int(xi - int(offsetW/2))
                                        w1 = int(w1 + offsetW)
                                        xf = xi + w1

                                        offsetH = (offsetY/100) * h1
                                        yi = int(yi - offsetH)
                                        h1 = int(h1 + offsetH)
                                        yf = yi + h1

                                        # Error
                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if w1 < 0: w1 = 0
                                        if h1 < 0: h1 = 0

                                        #steps verification
                                        if step == 0:
                                            #draw rectanlge
                                            cv2.rectangle(frame, (xi, yi, w1, h1), (0, 0, 255), 2)
                                            #step 0
                                            hs0, ws0, c = img_step0.shape
                                            frame[50:50 + hs0, 50:50 + ws0] = img_step0
                                            #step 1
                                            hs1, ws1, c = img_step1.shape
                                            frame[50:50 + hs1, 1030:1030 + ws1] = img_step1
                                            #step 2
                                            hs2, ws2, c = img_step2.shape
                                            frame[270:270 + hs2, 1030:1030 + ws2] = img_step2
                                            #Center face
                                            if cx7 > cx5 and cx8 < cx6:
                                                #IMG check
                                                hCheck, wCheck, c = img_check.shape
                                                frame[165:165 + hCheck, 1105:1105 + wCheck] = img_check
                                                #count parpadeo
                                                if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False:
                                                    conteo += 1
                                                    parpadeo = True
                                                elif longitud1 > 10 and longitud2 > 10 and parpadeo == True:
                                                    parpadeo = False
                                                cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070,375), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                                                if conteo >= 3:
                                                    hCheck, wCheck, c = img_check.shape
                                                    frame[385:385 + hCheck, 1105:1105 + wCheck] = img_check
                                                    #screen capture if open eyes
                                                    if longitud1 > 15 and longitud2 > 15:
                                                        #cut pixels of image face
                                                        faceCut = frameSave[yi:yf, xi:xf]
                                                        #Save frame face
                                                        cv2.imwrite(f"{OutFolderPathFaces}/{RegDocumento}.png", faceCut)
                                                        step = 1
                                            else:
                                                conteo = 0
                                        if step == 1:
                                            # draw rectanlge
                                            cv2.rectangle(frame, (xi, yi, w1, h1), (0, 255, 0), 2)
                                            # img liveness
                                            hliv, wliv, c = img_liveness.shape
                                            frame[50:50 + hliv, 50:50 + wliv] = img_liveness
                                            #closeWindow()

                                            pantalla2.protocol("WM_DELETE_WINDOW", closeWindow)

                            #circle sirve para verificar los puntos
                            cv2.circle(frame, (cx1, cy1), 2, (0, 0, 255), cv2.FILLED)
                            cv2.circle(frame, (cx2, cy2), 2, (0, 0, 255), cv2.FILLED)
                            cv2.circle(frame, (cx3, cy3), 2, (0, 0, 255), cv2.FILLED)
                            cv2.circle(frame, (cx4, cy4), 2, (0, 0, 255), cv2.FILLED)
                            cv2.circle(frame, (cx5, cy5), 2, (0, 0, 255), cv2.FILLED)
                            cv2.circle(frame, (cx6, cy6), 2, (0, 0, 255), cv2.FILLED)
                            cv2.circle(frame, (cx7, cy7), 2, (0, 0, 255), cv2.FILLED)
                            cv2.circle(frame, (cx8, cy8), 2, (0, 0, 255), cv2.FILLED)

        # converter video
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)
        #show video
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, register_biometric)
    else:
        capture.release()




def Register():
    global capture, lblVideo, pantalla2, InputNombresReg, InputApellidosReg, InputDocumentoReg, InputCursoReg, RegNombres, RegApellidos, RegDocumento, RegCurso
    #extract: name user pass
    RegNombres, RegApellidos, RegDocumento, RegCurso = InputNombresReg.get(), InputApellidosReg.get(), InputDocumentoReg.get(), InputCursoReg.get()
    #incomplete form
    if len (RegNombres) == 0 or len(RegApellidos) == 0 or len(RegDocumento) == 0 or len(RegCurso) == 0:
        print("Formulario Incompleto")
        messagebox.showwarning("Formulario Incompleto", "Por favor, completa todos los campos del formulario.")
    else:
        #check if user exists
        UsersList = os.listdir(PathUserCheck)
        UserDocumento = []

        for list in UsersList:
            User = list
            User = User.split('.')
            UserDocumento.append(User[0])

        if RegDocumento in UserDocumento:
            print("Documento ya existe")
            messagebox.showerror("Usuario ya registrado",
                                 "El documento ya existe. Por favor, usa un documento diferente.")
        else:
            # no registrado
            info.append(RegNombres)
            info.append(RegApellidos)
            info.append(RegDocumento)
            info.append(RegCurso)
        #exportar informacion a txt
        f = open(f"{OutFolderPathUser}/{RegDocumento}.txt", 'w')
        f.write(RegNombres + ',')
        f.write(RegApellidos + ',')
        f.write(RegDocumento + ',')
        f.write(RegCurso)
        f.close()

        #clean inputs
        InputNombresReg.delete(0, tk.END)
        InputApellidosReg.delete(0, tk.END)
        InputDocumentoReg.delete(0, tk.END)
        InputCursoReg.delete(0, tk.END)

        #pantalla2
        pantalla2 = tk.Toplevel()
        pantalla2.title("Registro Biometrico de Estudiante")
        pantalla2.geometry("1280x720")

        #lblVideo
        lblVideo = tk.Label(pantalla2)
        lblVideo.place(x=0, y=0)

        #capture
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        capture.set(3, 1280)
        capture.set(4, 720)
        register_biometric()


# path
OutFolderPathUser = 'C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/DB_FACES_DIR/Estudiantes/Users'
PathUserCheck = 'C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/DB_FACES_DIR/Estudiantes/Users/'
OutFolderPathFaces = 'C:/Users/MiniMonster/Desktop/FaceToList/FaceToList/DB_FACES_DIR/Estudiantes/Faces'


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





