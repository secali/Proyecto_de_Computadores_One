# import required libraries

import requests
import json
from bs4 import BeautifulSoup
from langdetect import detect
import pandas as pd
import batch.module2
import batch.functions


# We will store all methods and variables related to ShareGPT data extraction.
def batchOne():
    print("\n############Ejecutando Batch 1: Scraping#############")
    ENGLISH_TAG = 'en'
    url = "https://google.serper.dev/search"  # serper url
    # extractedLinks = []  # links obtained from Serper
    humanGeneratedList = []  # text generated by human
    iAGeneratedList = []  # text generated by IA

    # method that extracts Serper links and visits them to extract Human and AI conversations.
    payload = json.dumps({
        "q": "site:sharegpt.com",
        "num": 100
    })
    headers = {
        'X-API-KEY': 'f89a56ab46725993c40a6939284b05fdfe7ecce4',
        'Content-Type': 'application/json'

    }

    # Get request from Serper
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.json())

    # Filter to obtain the links
    extractedLinks = [item['link'] for item in response.json()['organic']]
    print("Se ha encontrado ", len(extractedLinks), " links en Serper")

    i = 0
    # Visit all links and GET clasify conversation in human or generated
    for thisLink in extractedLinks:
        print("Cargando: ", i % 100, "%")
        i += 1
        thisResponse = requests.get(thisLink)
        # print(thisResponse.text)

        soup = BeautifulSoup(thisResponse.text, 'html.parser')
        humanGeneratedList.append(soup.findAll('p', class_='pb-2 whitespace-prewrap'))

        soup = BeautifulSoup(thisResponse.text, 'html.parser')
        iAGeneratedList.append(soup.findAll('div', class_='utils_response__b5jEi'))

    print('Hay: ', len(humanGeneratedList), 'items en humanGeneratedList')
    print('Hay: ', len(iAGeneratedList), 'items en AIGeneratedList')

    # Triying to clean html tags after human/AI filter, less than 20 character and
    # not english text

    cleanHumanGeneratedList = []
    typeHumanList = []
    cleanIaGeneratedList = []
    typeIAList = []

    for extractedResponses in humanGeneratedList:
        for item in extractedResponses:

            soup = BeautifulSoup(item.text, "html.parser")
            text = soup.text

            if len(text) > 20 and detect(text) == ENGLISH_TAG:
                # cleanHumanGeneratedList.append(text)
                cleanHumanGeneratedList.append(text.strip().replace('\t', '').replace('\n', ''))
                # print(text.strip().replace('\t', '').replace('\n', ''))
                typeHumanList.append('h')  # añadimos etiqueta de humano
            else:
                print('Texto Eliminado!')

    for extractedResponses in iAGeneratedList:
        for item in extractedResponses:

            soup = BeautifulSoup(item.text, "html.parser")
            text = soup.text

            if len(text) > 20 and detect(text) == ENGLISH_TAG:
                # cleanIaGeneratedList.append(text)
                cleanIaGeneratedList.append(text.strip().replace('\t', '').replace('\n', ''))
                # print(text.strip().replace('\t', '').replace('\n', ''))
                typeIAList.append('g')  # añadimos etiqueta de generado
            else:
                print('Texto Eliminado!')

    # generamos diccionarios con los arrais
    datosHuman = {
        'Text': cleanHumanGeneratedList,
        'Type': typeHumanList
    }
    datosIA = {
        'Text': cleanIaGeneratedList,
        'Type': typeIAList
    }
    # creamos los dataFrame y concatenamos.  Generamos un DataSet completo
    dfHuman = pd.DataFrame(datosHuman)
    dfIA = pd.DataFrame(datosIA)
    dfDataSet = pd.concat([dfHuman, dfIA], ignore_index=True)

    # eliminamos duplicados si existen
    dfDataSet.drop_duplicates()

    # imprimimos el DataSet
    print(dfDataSet)

    # guardamos el DataSet
    batch.functions.guardar_dataset(dfDataSet, 'DataFrame.tsv')
    batch.module2.batchTwo()
