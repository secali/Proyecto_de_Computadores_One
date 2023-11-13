# pip install langdetect

import requests
import json
from bs4 import BeautifulSoup
from langdetect import detect


# We will store all methods and variables related to ShareGPT data extraction.


def batchOne():
    ENGLISH_TAG = 'en'
    url = "https://google.serper.dev/search"  # serper url
    extractedLinks = []  # links obtained from Serper
    humanGeneratedList = []  # text generated by human
    iAGeneratedList = []  # text generated by IA

    # method that extracts Serper links and visits them to extract Human and AI conversations.

    payload = json.dumps({
        "q": "site:sharegpt.com"
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
    print(extractedLinks)

    # Visit all links and GET clasify conversation in human or generated

    for thisLink in extractedLinks:
        thisResponse = requests.get(thisLink)
        # print(thisResponse.text)

        soup = BeautifulSoup(thisResponse.text, 'html.parser')
        humanGeneratedList = soup.findAll('p', class_='pb-2 whitespace-prewrap')

        # print(humanGeneratedList)

        soup = BeautifulSoup(thisResponse.text, 'html.parser')
        iAGeneratedList = soup.findAll('div', class_='utils_response__b5jEi')

        # print(AIGeneratedList)

    print('There are: ', len(humanGeneratedList), 'items in humanGeneratedList')
    print('There are: ', len(iAGeneratedList), 'items in AIGeneratedList')

    # Triying to clean html tags after human/AI filter, less than 20 character and
    # not english text

    cleanHumanGeneratedList = []
    cleanIaGeneratedList = []

    for item in humanGeneratedList:

        soup = BeautifulSoup(item.text, "html.parser")
        text = soup.text

        if len(text) > 20 and detect(text) == ENGLISH_TAG:
            cleanHumanGeneratedList.append(text.strip().replace('\t', '').replace('\n', ''))
            print(text.strip().replace('\t', '').replace('\n', ''))
        else:
            print('Removed text')

    for item in iAGeneratedList:

        soup = BeautifulSoup(item.text, "html.parser")
        text = soup.text

        if len(text) > 20 and detect(text) == ENGLISH_TAG:
            cleanIaGeneratedList.append(text.strip().replace('\t', '').replace('\n', ''))
            print(text.strip().replace('\t', '').replace('\n', ''))
        else:
            print('Removed text')

    humanGeneratedList = set(cleanHumanGeneratedList)
    iAGeneratedList = set(cleanIaGeneratedList)

    print('\nThere are: ', len(humanGeneratedList), 'items in humanGeneratedList')
    print('There are: ', len(iAGeneratedList), 'items in AIGeneratedList')
