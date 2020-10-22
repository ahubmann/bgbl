import json
import os
import re
import requests

date_from='2020-01-01'
date_to='2020-12-31'


for page in range(1,1000):
    r = requests.post('https://data.bka.gv.at/ris/api/v2.5/bundesgesetzblaetter', data = {'Seitennummer':page, 'Kundmachung.Von':date_from, 'Kundmachung.Bis':date_to})
    j = json.loads(r.text)
    if ('OgdDocumentResults' not in j['OgdSearchResult']):
        print "done"
        break
    for i in  j['OgdSearchResult']['OgdDocumentResults']['OgdDocumentReference']:
        bgbl = i['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['Bgblnummer']
        url = ''
        contentref = i['Data']['Dokumentliste']['ContentReference']
        if type(contentref) is list:
            for doc in contentref:
                if doc['ContentType'] == 'MainDocument':
                    for url in doc['Urls']['ContentUrl']:
                        if url['DataType'] == 'Authentisch':
                            url = url['Url']
        else:
            for url in contentref['Urls']['ContentUrl']:
                if url['DataType'] == 'Authentisch':
                    url = url['Url']
        if url != '':
            print url
            filename = url.rsplit('/', 1)[1]
            if (not os.path.exists('data/' + filename)):
                r = requests.get(url, allow_redirects = True)
                open('data/' + filename, 'wb').write(r.content)
                open('metadata/' + filename, 'wb').write(json.dumps(i))
