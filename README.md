# Abfrage von Metadaten zu veröffentlichen Bundesgesetzblättern

Aktuelles Resultat als [CSV](https://github.com/ahubmann/bgbl/blob/main/data/bgbl.csv) (vom 23. Oktober 11:00 Uhr)

* `retrieve-bgbl.py` lädt PDF und HTML Version nach `data/bgbl` und Metadaten nach `data/metadata`
* `extract-info.py` extrahiert Metadaten aus PDF (Signatur-Zeitpunkt und Erstellungsdatum) nach `data/extracted`
* `retrieve-history.py` sucht alle Änderungen des BGBl im konsolidierten Bundesrecht und schreibt sie nach `data/history`
* `create-csv.py` erstellt den Output aus obigen Daten

## Bemerkungen

* In `retrieve-bgbl.py` ist der Zeitraum für 2020 derzeit hard-coded.
* `extract-info.py` benötigt `pdfsig` für das Auslesen der Signatur-Daten und `pdfinfo` für die sonstigen Metadaten.
* `create-csv.py` versucht, aus *Inkraft-* und *Ausserkrafttretedatum* in Verbindung mit dem *Ausgabedatum* sinnvolle Werte zu extrahieren.
* Der reguläre Ausdruck in `extract-info.py` für das Erkennen der Textstellen ist - wie sag' ich's - *verbesserungsfähig*.

Danke an https://twitter.com/MartinThuer für die willkommene Ablenkung.
