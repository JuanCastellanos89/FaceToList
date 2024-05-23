import cv2
import imutils
import numpy as np
import face_recognition as fr
import os
import random
from datetime import datetime
import tkinter as tk

# Access to the folder
path = 'DB_FACES_DIR/Estudiantes/Faces'
images = []
clases = []
lista = os.listdir(path)

# Read the faces from the database
for lis in lista:
    imgdb = cv2.imread(f'{path}/{lis}')
    images.append(imgdb)
    clases.append(os.path.splitext(lis)[0])

print(clases)

# Encode the faces
def codRostros(images):
    listaCod = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(img)[0]
        listaCod.append(cod)
    return listaCod

def horarioEntrada(nombre):
    with open('Registro.csv', 'r+') as f:
        data = f.readlines()
        listaNombres = [line.split(',')[0] for line in data]

        if nombre not in listaNombres:
            info = datetime.now()
            fecha = info.strftime('%Y-%m-%d')
            hora = info.strftime('%H:%M:%S')
            f.write(f'{nombre},{fecha},{hora}\n')
            print(info)

def mostrar_ventana():
    rostrosCod = codRostros(images)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Cambia el backend a DirectShow

    if not cap.isOpened():
        print("Error: No se puede abrir la cámara.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede capturar el cuadro.")
            continue  # Si no se puede capturar el cuadro, continúa al siguiente ciclo

        if frame is None:
            print("Advertencia: El frame capturado es None.")
            continue  # Si el frame es None, continúa al siguiente ciclo

        frame2 = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        faces = fr.face_locations(rgb)
        facesCod = fr.face_encodings(rgb, faces)

        for faceCod, faceLoc in zip(facesCod, faces):
            comp = fr.compare_faces(rostrosCod, faceCod)
            faceDist = fr.face_distance(rostrosCod, faceCod)
            minIndex = np.argmin(faceDist)

            if comp[minIndex]:
                nombre = clases[minIndex].upper()
                print(nombre)
                yi, xi, yf, xf = faceLoc
                xi, yi, xf, yf = xi * 4, yi * 4, xf * 4, yf * 4

                r, g, b = random.randrange(0, 255, 50), random.randrange(0, 255, 50), random.randrange(0, 255, 50)
                cv2.rectangle(frame, (xi, yi), (xf, yf), (r, g, b), 1)
                cv2.rectangle(frame, (xi, yf - 35), (xf, yf), (r, g, b), cv2.FILLED)
                cv2.putText(frame, nombre, (xi + 6, yf - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                horarioEntrada(nombre)

        cv2.imshow('Reconocimiento de Estudiantes en VIVO', frame)
        k = cv2.waitKey(1) & 0xFF  # Use bitwise AND for cross-platform compatibility
        if k == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()