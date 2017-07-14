from collections import namedtuple
import simplekml

def parse_grid(text):
    lat = int(text[0:3]) + int(text[4:6])/60 + int(text[7:9])/3600
    lon = int(text[10:14]) + int(text[15:17])/60 + int(text[18:20])/3600
    return lat, lon

def in_area(lat, lon):
    latl = 40
    latu = 49
    lonl = 7
    lonu = 30
    if latl <= lat and lat <= latu:
        if lonl <= lon and lon <= lonu:
            return True
    return False


path = 'stations.txt'
Station = namedtuple('Station', ['name', 'cty', 'lat', 'lon', 'el'])
dct_station = {}

with open(path, 'r') as f:
    for _ in range(19):
        next(f)
    for line in f:
        cty = line[47:49]
        lat, lon = parse_grid(line[50:70])
        if in_area(lat, lon):
            s_id = line[0:5].strip().zfill(6)
            dct_station[s_id] = Station(name=line[6:45].strip(), 
                                        cty=line[47:49], lat=lat, lon=lon, 
                                        el=int(line[71:76]))
       
kml = simplekml.Kml(name='Meteo stations')
for key in dct_station.keys():
    st = dct_station[key]
    nm = st.name + ', ' + st.cty
    kml.newpoint(name=nm, description=key, coords=[(st.lon, st.lat, st.el)])

kml.save('stations.kml')