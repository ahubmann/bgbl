import json
import os
import re
import requests

for filename in os.listdir('data/metadata'):
    if (os.path.exists('data/history/' + filename)):
        continue
    metadata = json.load(open('data/metadata/' + filename))
    bgblnr = metadata['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['Bgblnummer']
    ausgabedatum = metadata['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['Ausgabedatum']
    m = re.search('(BGBl. .* Nr.) (.*)', bgblnr)
    bgblteil = ''
    bgbl = ''
    if m:
        bgblteil = m.group(1)
        bgbl = m.group(2)
    
    print(bgblnr)
    history = []
    for page in range(1,1000):
        r = requests.post(' https://data.bka.gv.at/ris/api/v2.5/Bundesnormen', data = {'Seitennummer':page, 'Kundmachungsorgan':bgblteil, 'Kundmachungsorgannummer':bgbl})
        j = r.json()
        if ('OgdDocumentResults' not in j['OgdSearchResult']):
            break
        if 'OgdDocumentReference' in j['OgdSearchResult']['OgdDocumentResults']:
            docref = j['OgdSearchResult']['OgdDocumentResults']['OgdDocumentReference']
            if not type(docref) is list:
                docref = [docref]

            for i in docref:
                item  = {}
                item['url'] = i['Data']['Metadaten']['Allgemein']['DokumentUrl']
                if ('Inkrafttretedatum' in i['Data']['Metadaten']['Bundes-Landesnormen']):
                    item['inkraft'] = i['Data']['Metadaten']['Bundes-Landesnormen']['Inkrafttretedatum']
                item['paragraph'] = i['Data']['Metadaten']['Bundes-Landesnormen']['ArtikelParagraphAnlage']
                if 'Ausserkrafttretedatum' in i['Data']['Metadaten']['Bundes-Landesnormen']:
                    item['ausserkraft'] = i['Data']['Metadaten']['Bundes-Landesnormen']['Ausserkrafttretedatum']
                history.append(item)
    open('data/history/' + filename, mode='w').write(json.dumps(history, ensure_ascii=False))
