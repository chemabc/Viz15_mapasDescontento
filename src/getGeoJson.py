import csv
from geopy.geocoders import Nominatim
#import unicodedata

geoJsonList = []
with open ('../data/places.csv', 'r') as csvfileRead:
    csvRead = csv.reader(csvfileRead, delimiter = ' ')
    for line in csvRead:
        geoJsonList.append({'place': " ".join(line)})
        print(line)


print(geoJsonList)

geolocator = Nominatim()
loc = geolocator.geocode("Spain", timeout = 10)
print("Lat: ", loc.latitude, "; Lon: ", loc.longitude)


for line in geoJsonList:
    pl = line['place']
    loc = geolocator.geocode(pl, timeout = 10)
    try:
        print("Place: ", pl, ": Lat: ", loc.latitude, "; Lon: ", loc.longitude)
        line["lat"] = loc.latitude
        line["lng"] = loc.longitude
        #print(line)
    except:
        print("ERROR: Algun error ha ocurrido en " , pl)


print(geoJsonList)
with open ('../data/placesOutput.csv', 'wb') as csvfileWrite:
    dictKeys = ['place', 'lat', 'lng']
    csvWrite = csv.DictWriter(csvfileWrite, dictKeys)
    csvWrite.writerows(geoJsonList)
csvfileWrite.close()