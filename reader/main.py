import cv2
import numpy as np
import glob
import os
import datetime
import pytesseract
import re
from bs4 import BeautifulSoup
from collections import Counter
import requests
from PIL import Image
from pytesseract import image_to_string

src_path = r"/Users/macbook/Desktop"  # Cambiar direccion en Windows


def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite(src_path + r"/removed_noise.png", img)  # Cambiar en Windows (el "/" creo)

    #  Apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + r"/thres.png", img)  # Cambiar en Windows (el "/" creo)

    # Recognize text with tesseract for python
    a = Image.open(src_path + r"/thres.png")  # Cambiar en Windows (el "/" creo)
    result = image_to_string(a, lang='eng')

    string2 = []
    for i in result.split("\n\n"):
        string2.append(i.replace('\n', ''))

    return string2


def search():
    # Contadores de palabras claves
    cont = 0
    cont2 = 0
    cont3 = 0

    # Devuelve una lista de path's del desktop
    list_of_files = glob.glob('/Users/macbook/Desktop/*')  # Cambiar direccion en Windows

    # Devuelve el path del ultimo archivo del desktop
    latest_file = max(list_of_files, key=os.path.getctime)

    # Obtiene el texto de la imagen
    string = get_string(latest_file)

    # Pregunta
    query = string[0]

    # Respuestas
    key = string[1]
    key2 = string[2]
    key3 = string[3]

    search = query.replace(" ", "+")

    # Se carga el enlace con la pregunta y palabras claves
    googleSearch = "https://www.google.cl/search?q=" + search + key + key2 + key3

    # Se realiza el request al enlace, retorna informacion de la pagina
    r = requests.get(googleSearch)

    # Devuelve el texto de la pagina con tag's
    soup = BeautifulSoup(r.text, "html.parser")

    # Se buscan todos los contenidos de la pagina que estan entre <span "class"="st"><span>
    url = soup.findAll('span', {"class": "st"})

    # Se analiza linea por linea el string url
    for i in url:

        # Entrega una linea obviando los tag's intermedios
        value = i.get_text()

        # Se contabilizan oncurrencias de palabras claves en una linea
        if (key in value):
            cont += 1
        if (key2 in value):
            cont2 += 1
        if (key3 in value):
            cont3 += 1

    # Suma total de ocurrencias
    contf = cont + cont2 + cont3

    # Evitar problema de division por 0
    if contf == 0:
        contf = 1

    # Muestra los resultados en porcentajes
    print(str(cont / contf * 100) + "% - " + key)
    print(str(cont2 / contf * 100) + "% - " + key2)
    print(str(cont3 / contf * 100) + "% - " + key3)


print('--- Start recognize text from image ---')
search()
print("------ Done -------")