import csv
import json
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

with open('bgbl.csv', mode='w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Bgblnr', 'Ausgabedatum', 'Erstellungsdatum', 'Signaturdatum', 'Kurztitel', 'Titel'])
    for filename in os.listdir('metadata'):
        print filename
        shorttitle = ''
        titel = ''
        ausgabedatum = ''
        bgblnr = ''
        creationdate = ''
        signdate = ''
        with open('metadata/' + filename) as json_file:
            data = json.load(json_file)
            title = data['Data']['Metadaten']['Bundesgesetzblaetter']['Titel']
            shorttitle = data['Data']['Metadaten']['Bundesgesetzblaetter']['Kurztitel']
            ausgabedatum = data['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['Ausgabedatum']
            bgblnr = data['Data']['Metadaten']['Bundesgesetzblaetter']['Bgbl-Auth']['Bgblnummer']
        with open('extracted/' + filename) as json_file:
            data = json.load(json_file)
            creationdate = data['CreationTimestamp']
            signdate = data['SignatureTimestamp']
            writer.writerow([bgblnr, ausgabedatum, creationdate, signdate, shorttitle, title])
