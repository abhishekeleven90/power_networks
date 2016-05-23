#process address, location of entities for better resolution

from geolocation.main import GoogleMaps

def getCityState(address):
    if type(address) !=str:
        print "Non string argument"
        exit(3)

    gmaps = GoogleMaps(api_key="AIzaSyCPrZzfBD4vpdjkulq2u62CloyZMsAojRQ")
    loc = gmaps.search(location=address)
    myloc = loc.first()

    city = myloc.city
    for area in myloc.administrative_area:
        if area.name.lower() != city.lower():
            state = area.name
            break

    return (city,state)



