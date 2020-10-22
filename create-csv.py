import csv
import json
import os

with open('bgbl.csv', mode='w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Bgblnr', 'Ausgabedatum', 'Erstellungsdatum', 'Signaturdatum', 'Datum Nationalrat', 'Datum Bundesrat', 'Datum des Inkrafttretens', 'Kurztitel', 'Titel', 'Organ', 'Typ', 'URL HTML', 'URL PDF'])
    for filename in os.listdir('metadata'):
        print(filename)
        shorttitle = ''
        titel = ''
        ausgabedatum = ''
        bgblnr = ''
        creationdate = ''
        signdate = ''
        organ = ''
        typ = ''
        datumnationalrat = ''
        datumbundesrat = ''
        urlhtml = ''
        urlpdf = ''
        with open('metadata/' + filename) as json_file:
            data = json.load(json_file)
            title = data['Data']['Metadaten']['Bundesgesetzblaetter']['Titel']
            shorttitle = data['Data']['Metadaten']['Bundesgesetzblaetter']['Kurztitel']
            ausgabedatum = data['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['Ausgabedatum']
            bgblnr = data['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['Bgblnummer']
            organ = data['Data']['Metadaten']['Technisch']['Organ']
            typ = data['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['Typ']
            if 'DatumNationalrat' in data['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']:
                datumnationalrat = data['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['DatumNationalrat']
            if 'DatumBundesrat' in data['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']:
                datumbundesrat = data['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['DatumBundesrat']
            contentref = data['Data']['Dokumentliste']['ContentReference']
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
        with open('extracted/' + filename) as json_file:
            data = json.load(json_file)
            creationdate = data['CreationTimestamp']
            signdate = data['SignatureTimestamp']
            validitydate = [s.replace('\xa0', ' ') for s in data['LegalValidityTimestamp']]
        writer.writerow([bgblnr, ausgabedatum, creationdate, signdate, datumnationalrat, datumbundesrat, validitydate, shorttitle, title, organ, typ, urlhtml, urlpdf])
