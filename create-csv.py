import csv
import json
import os

rows = []
for filename in os.listdir('data/metadata'):
    print(filename)
    shorttitle = ''
    titel = ''
    ausgabedatum = ''
    bgblnr = ''
    organ = ''
    typ = ''
    datumnationalrat = ''
    datumbundesrat = ''
    urlhtml = ''
    urlpdf = ''
    with open('data/metadata/' + filename) as json_file:
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
    creationdate = ''
    signdate = ''
    inkrafttext = ''
    with open('data/extracted/' + filename) as json_file:
        data = json.load(json_file)
        creationdate = data['CreationTimestamp']
        signdate = data['SignatureTimestamp']
        inkrafttext = [s.replace('\xa0', ' ') for s in data['LegalValidityTimestamp']]
    inkraftearliest = ''
    inkraftlatest = ''
    inkraftall = ''
    changeset = ''
    with open('data/history/' + filename) as json_file:
        data = json.load(json_file)
        dates = []
        changeset = []
        for date in data:
            changeset.append(date['url'])
            if 'inkraft' in date and not 'ausserkraft' in date:
                dates.append(date['inkraft'])
            if 'ausserkraft' in date and not 'inkraft' in date:
                dates.append(date['ausserkraft'])
            if 'ausserkraft' in date and 'inkraft' in date:
                if date['inkraft'] > ausgabedatum:
                    dates.append(date['inkraft'])
                else:
                    dates.append(date['ausserkraft'])
        if (dates):
            inkraftall = list(set(dates))
            inkraftearliest = min(dates)
            inkraftlatest = max(dates)

    rows.append([bgblnr, ausgabedatum, creationdate, signdate, datumnationalrat, datumbundesrat, inkraftearliest, inkraftlatest, inkraftall, inkrafttext, shorttitle, title, organ, typ, urlhtml, urlpdf, changeset])

rows.sort(key=lambda x:x[1] + ' ' + x[0], reverse = True)

with open('data/bgbl.csv', mode='w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Bgblnr', 'Ausgabedatum', 'Erstellungsdatum', 'Datum Signatur', 'Datum Nationalrat', 'Datum Bundesrat', 'Datum Inkraft-/Ausserkrafttreten frühestes', 'Datum Inkraft-/Ausserkrafttreten spätestes', 'Datum Inkraft-/Ausserkrafttreten alle', 'Datum Inkrafttreten Text', 'Kurztitel', 'Titel', 'Organ', 'Typ', 'URL HTML', 'URL PDF', 'Changeset'])
    for row in rows:
        writer.writerow(row)
