#process address, location of entities for better resolution
#Using Google geolocation api
import googlemaps
import requests
import json
from termcolor import colored
from googlemaps.exceptions import Timeout, TransportError, ApiError
from time import sleep


def getCityState(address):
    if type(address) != str:
        print colored("Non string argument",'red')
        exit(3)

    # API KEY OLD AIzaSyALThUkSSrl0qMGPnaewBghOhkA81vDQHk"
    gmaps = googlemaps.Client(key="AIzaSyAbkl28DtvWs2WCaOUzt7d383my26Invvw")
    i = 0
    while (i < 3):
        try:
            loc = gmaps.geocode(address)
        except (TransportError, Timeout, ApiError) as e:
            print colored("Error - {}".format(e),'red')
            print colored("Trying to reconnect",'green')
            sleep(5)
            i += 1
        else:
            break

    if i >= 3:
        print colored("fatal: Network Error!", 'red')
        exit(1)

    #print loc
    results = loc[0]["address_components"]
    print results
    try:
        city = [r["long_name"] for r in results if ("administrative_area_level_2" in r["types"])][0]
    except IndexError:
        print colored("Not enough info to infer city", 'red')
        city = ""

    try:
        state = [r["long_name"] for r in results if "administrative_area_level_1" in r["types"] ][0]
    except IndexError:
        print colored("Not enough info to infer state", 'red')
        state = ""

    return city, state


def getCityStateByPin(pincode):
    url = "https://www.whizapi.com/api/v2/util/ui/in/indian-city-by-postal-code"
    querystring = {"pin": pincode, "project-app-key": "sd6u15esx571r9kndndlib17"}
    headers = {
              'cache-control': "no-cache",
              'postman-token': "e162eb01-9cb6-6845-0dea-5b24c33e2232"
              }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)["Data"]
    city = response[0]["City"]
    state = response[0]["State"]

    return city, state


if __name__ == "__main__":
    c, s = getCityState('Andaman and Nicobar Islands South Andaman')
    #c, s = getCityStateByPin('700065')
    print c
    print s
