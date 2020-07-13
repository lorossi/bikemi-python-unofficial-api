# BikeMi-Python-Unofficial-API

## Italian (English below)
Scraper per la mappa del [BikeMi](https://www.bikemi.com/it/mappa-stazioni.aspx) fatta in Python3.

Il modulo *BikeMi.py* estrae:
1. Statistiche globali sul servizio:
  1. Statistiche sulle bici:
    1. Stalli liberi
    2. Bici disponibili
    3. Bici elettriche disponibili
    4. Bici elettriche con seggiolino disponibili
    5. Numero totale di bici disponibili
  2. Statistiche sulle stazioni:
    1. Stazioni piene
    2. Stazioni vuote
    3. Stazioni *probabilmente* piene
    4. Stazioni *probabilmente* piene
    5. Numero totale di stazioni
  3. Statistiche sulle icone usate:
    1. Nome dell'icona
    2. Numero di volte che è stata usata
    3. URL dell'icona
2. Statistiche per ogni stazione:
  1. Nome della stazione
  2. ID della stazione
  3. Coordinate della stazione
  4. Numero di bici nella stazione, a sua volta diviso in:
      1. Stalli liberi
      2. Bici disponibili
      3. Bici elettriche disponibili
      4. Bici elettriche con seggiolino disponibili
  5. Se la stazione è piena
  6. Se la stazione è vuota
  7. Se la stazione *potrebbe* essere piena
  8. Se la stazione *potrebbe* può essere vuota
  9. Il nome dell'icona che il sito mostra sulla mappa e il suo URL

I dati vengono restituiti tramite dizionario e possono essere salvati su file in formato JSON.

Nella repo viene anche fornito uno script *(BikeMi-example.py)* che mostra un uso di esempio.

### Stazione probabilmente piena / vuota
Ho provato, per esperienza mia diretta che le biciclette rotte non sono conteggiate dal sistema. Per questo, anche se la stazione mostra bici o stalli disponibili, ciò potrebbe non rispecchiare la realtà.
Lo script quindi indica se la stazione è *probabilmente vuota* o *probabilmente piena*. Il conteggio è arbitrario ed è basato sulla mia esperienza di utente BikeMi.

### Link ufficiali
[Sito BikeMi](https://www.bikemi.com/)  
[Mappa BikeMi](https://www.bikemi.com/it/mappa-stazioni.aspx)

### Codice di esempio

    import bikemi
    b = bikemi.BikeMi()
    bikes = b.getBikes()
    b.save("bikemi.json")

Un esempio più completo di codice è disponibile nello script *(BikeMi-example.py)*.

### Licenza
Questo progetto è distribuito sotto licenza *Attribuzione 4.0 Internazionale (CC BY 4.0)*
Il progetto è completamente indipendente da BikeMi.

## English
Scraper for [BikeMi](https://www.bikemi.com/it/mappa-stazioni.aspx) map. Made in Python3.

*BikeMy.pi* module extracts:
1. Global statistics on the service
  1. Bikes statistics:
    1. Free racks
    2. Available bikes
    3. Available electric bikes
    4. Available electric bikes with child seat
    5. Total number of available bikes
  2. Stations statistics:
    1. Empty stations
    2. Full stations
    3. Stations that *might* be empty
    4. Stations that *might* be full
    5. Total number of stations
  3. Icons statistics:
    1. Icon name
    2. Number of time it has been used
    3. Icon URL
2. Data for each station
  1. Station name
  2. Station ID
  3. Station coordinates
  4. Number of bikes available, divided in
      1. Free racks
      2. Available bikes
      3. Available electric bikes
      4. Available electric bikes with child seat
  5. If the station is empty
  6. If the station is full
  7. If the station *might* be empty
  8. If the station *might* be full
  9. Name and URL of the icon used on the map

All the data is provided in a dict and can be saved into a JSON file.

Inside this repo you will find a file called *(BikeMi-example.py)* that shows a use case.

### Probably empty/full station
By experience, I discovered that broken bycicles are not counted by the system. Because of this, even if the station shows free racks or available bikes, it might not be true.
This script acknowledges this and tells you if the bike station is *probably full* or *probably empty*. This stat is purerly arbitrary and it is based on my experience as a BikeMi user.

### Official links
[Bikemi website](https://www.bikemi.com/)  
[BikeMi map](https://www.bikemi.com/it/mappa-stazioni.aspx)


### Code example

    import bikemi
    b = bikemi.BikeMi()
    bikes = b.getBikes()
    b.save("bikemi.json")

A more complete example can be found inside the repo *(BikeMi-example.py)*.

### License
This project is distributed under *Attribution 4.0 International (CC BY 4.0)* license.
I do not claim any association with BikeMi.
