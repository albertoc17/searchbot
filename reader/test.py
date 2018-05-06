import glob
import os
from bs4 import BeautifulSoup
import requests
import json

src_path = r"C:\Users\acart\Desktop"

# API that Recognize characters from image


def ocr_space_file(filename, overlay=False, api_key='af599d01d888957', language='eng'):

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode().replace("'", '"')
# search the results.


def search():
    strApi = []
    queryStr = []
    flag = False

    # Contadores de palabras claves
    cont = 0
    cont2 = 0
    cont3 = 0

    # Devuelve una lista de path's del desktop
    list_of_files = glob.glob(r'C:\Users\acart\Desktop\*')

    # Devuelve el path del último archivo del desktop
    latest_file = max(list_of_files, key=os.path.getctime)

    # Devuelve un string con el texto de la imagen
    dict_file = ocr_space_file(filename=latest_file, language='eng')

    # Devuelve un diccionario con el contenido de la imagen
    data = json.loads(dict_file)

    # Retorna el contenido exacto requerido como un array
    filter = (data['ParsedResults'][0]['ParsedText']).split(' ')
    print("Printing the contents of the api..\n")
    print(filter)

    # Loop utilizado para filtrar palabras clave
    for i in filter:
        # Si el flag sea False, almecenará cada string en queryStr
        if not flag:
            queryStr.append(i.replace('\r\n', ''))
        # Si se llega al signo de interrogación, se salta el loop
        if '?' in i:
            flag = True
            continue
        # Si ya se paso el signo de interrogación, empieza a guardar en strApi
        if flag:
            # Condición para no guardar el último espacio vacío
            if i == '\r\n':
                break
            strApi.append(i.replace('\r\n', ''))


    # Pregunta
    query = queryStr
    q_string = " ".join(query)
    print("Printing question...\n")
    print(q_string)
    # Si el array string no llega a tener 4 valores, arroja una excepcion
    try:

        # Respuestas
        key = strApi[0]
        key2 = strApi[1]
        key3 = strApi[2]
    except IndexError:
        print("No se cargaron las palabras clave")
        exit(1)

    search = q_string.replace(" ", "+")

    # Se carga el enlace con la pregunta y palabras claves
    google_search = "https://www.google.cl/search?q="+search+" "+key+" "+key2+" "+key3

    # Se realiza el request al enlace, retorna informacion de la pagina
    r = requests.get(google_search )

    # Devuelve el texto de la pagina con tag's
    soup = BeautifulSoup(r.text, "html.parser")

    # Se buscan todos los contenidos de la pagina que estan entre <span "class"="st"><span>
    url = soup.findAll('span', {"class": "st"})

    # Se analiza linea por linea el string url
    for i in url:

        # Entrega una linea obviando los tag's intermedios
        value = i.get_text()

        # Se contabilizan concurrencias de palabras claves en una linea
        if key in value:
            cont += 1
        if key2 in value:
            cont2 += 1
        if key3 in value:
            cont3 += 1

    # Suma total de ocurrencias
    contf = cont + cont2 + cont3

    # Evitar problema de division por 0
    if contf == 0:
        contf = 1

    # Muestra los resultados en porcentajes
    print("Printing the results..\n")
    print(str(cont / contf * 100) + "% - " + key)
    print(str(cont2 / contf * 100) + "% - " + key2)
    print(str(cont3 / contf * 100) + "% - " + key3)


if __name__ == "__main__":
    print('--- Start recognize text from image ---')
    search()
    print("------ Done -------")

