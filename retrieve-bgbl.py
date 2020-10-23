import json
import os
import re
import requests

date_from='2020-01-01'
date_to='2020-12-31'

for page in range(1,1000):
    r = requests.post('https://data.bka.gv.at/ris/api/v2.5/bundesgesetzblaetter', data = {'Seitennummer':page, 'Kundmachung.Von':date_from, 'Kundmachung.Bis':date_to})
    j = r.json()
    if ('OgdDocumentResults' not in j['OgdSearchResult']):
        break
    for i in  j['OgdSearchResult']['OgdDocumentResults']['OgdDocumentReference']:
        bgbl = i['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['Bgblnummer']
        urlpdf = ''
        urlhtml = ''
        contentref = i['Data']['Dokumentliste']['ContentReference']
        if type(contentref) is list:
            for doc in contentref:
                if doc['ContentType'] == 'MainDocument':
                    for url in doc['Urls']['ContentUrl']:
                        if url['DataType'] == 'Authentisch':
                            urlpdf = url['Url']
                        if url['DataType'] == 'Html':
                            urlhtml = url['Url']
        else:
            for url in contentref['Urls']['ContentUrl']:
                if url['DataType'] == 'Authentisch':
                    urlpdf = url['Url']
                if url['DataType'] == 'Html':
                    urlhtml = url['Url']
        if urlpdf != '':
            print(urlpdf)
            filename = urlpdf.rsplit('/', 1)[1]
            if (not os.path.exists('data/bgbl/' + filename)):
                r = requests.get(urlpdf, allow_redirects = True)
                open('data/bgbl/' + filename, mode='wb').write(r.content)
        if urlhtml != '':
            print(urlhtml)
            filename = urlhtml.rsplit('/', 1)[1]
            if (not os.path.exists('data/bgbl/' + filename)):
                r = requests.get(urlhtml, allow_redirects = True)
                open('data/bgbl/' + filename, mode='wb').write(r.content)
        open('data/metadata/' + os.path.splitext(filename)[0], mode='w').write(json.dumps(i, ensure_ascii=False))
