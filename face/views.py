from distutils.util import execute

from django.shortcuts import render,redirect

from django.http import HttpResponse

import cv2

import numpy as np

import os

def detection(request):

    from os import listdir

    from os.path import isfile, join

    import sqlite3

    cap= cv2.VideoCapture(0)

    cap.read()

    conn = sqlite3.connect('db.sqlite3')

    cur=conn.cursor()

    requete="select cin,id_patient from patient"

    res=cur.execute(requete)

    result = cur.fetchall()

    for j in result:

        print(j[0])

        data_path = 'C:/Users/hp/projet_python_reconaissance/image/'

        data_path = data_path[0:len(data_path)]+j[0]+'/'

        # lister toutes les images dans une liste (isfile pour tester que le file est une image)

        onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]

        # Create arrays for training data and labels

        Training_Data, Labels = [], []

        # Opening training images in our datapath

        # Creating a numpy array for training data

        for i, files in enumerate(onlyfiles):
            
            image_path = data_path + onlyfiles[i]
            
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            # pour charger l'image en mode niveau de gris
            
            # asarray() pour convertire chaque image en un tableau

            Training_Data.append(np.asarray(images, dtype=np.uint8))

            # pour chaque image on stock son indice dans un tableau labels

            Labels.append(i)

        Labels = np.asarray(Labels, dtype=np.int32)

        # LBPH (Local Binary Pattern Histogram) est un algorithme de reconnaissance faciale utilisé 
        # pour reconnaître le visage d’une personne. Il est connu pour ses performances et sa capacité 
        # à reconnaître le visage d’une personne à la fois de face avant et de face.

        model = cv2.face.LBPHFaceRecognizer_create()

        model.train(np.asarray(Training_Data), np.asarray(Labels))
    
        face_classifier = cv2.CascadeClassifier('C:/Users/hp/projet_python_reconaissance/face/haarcascade_frontalface_default.xml')

        def face_detector(img, size = 0.5):

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_classifier.detectMultiScale(gray,1.3,5)

            if faces is():

                return img,[]

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)

                roi = img[y:y+h, x:x+w]

                roi = cv2.resize(roi, (200,200))

            return img,roi
        
        while True:

            ret, frame = cap.read()

            image, face = face_detector(frame)

            try:

                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                result = model.predict(face)

                if result[1] < 500:

                    confidence = int(100*(1-(result[1])/300))

                if confidence > 82:

                    request.session['id'] = j[1]
                    
                    return redirect("/recup_infos/recherche_detect")

                else:

                    break

            except:

                cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

                cv2.imshow('Face Cropper', image)

                pass

            if cv2.waitKey(1)==ord('q'):
        
                break
       
    cap.release()

    cv2.destroyAllWindows()
    
    return redirect("/ajouter")



def Dataset(request):
    
    face_classifier = cv2.CascadeClassifier('C:/Users/hp/projet_python_reconaissance/face/haarcascade_frontalface_default.xml')

    def face_extractor(img):

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = face_classifier.detectMultiScale(gray,1.3,5)

        if  faces is():

            return None

        for(x,y,w,h) in faces:

            # Nous allons parcourir chaque rectangle (chaque face détectée) en utilisant ses coordonnées générées par la fonction.

            cropped_face = img[y:y+h, x:x+w]

        return cropped_face
    
    cap = cv2.VideoCapture(0)

    count = 0

    nameID=request.session['cin'].lower()
    
    path='C:/Users/hp/projet_python_reconaissance/image/'+nameID

    os.makedirs(path)
            
    while True:

        ret, frame = cap.read()

        if face_extractor(frame) is not None:

            count+=1

            face = cv2.resize(face_extractor(frame),(200,200))

            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_name_path ='C:/Users/hp/projet_python_reconaissance/image/'+nameID+'/'+ str(count) + '.jpg'

            cv2.imwrite(file_name_path,face)

        else:

            print("Face not found")

            pass

            # lorsque le nombre de photos depasse 100 on arrete la processus de detection ,

        if cv2.waitKey(1)==ord('q') or count==100:

            break

    cap.release()

    cv2.destroyAllWindows()

    return redirect("/sec")