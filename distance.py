import urllib.request
import json
import pyttsx3
import requests
import json
import speech_TO_txt
import time
# json_data = json.dumps({})
# json_data["key"] = "value"

# print ('JSON: ', json_data)

def lastry():
    response = requests.get("http://ip-api.com/json/14.97.167.154").json()
    latitude=response['lat']
    longitude=response['lon']
    print(latitude)
    print(longitude)


    engine = pyttsx3.init()
    # Your Bing Maps Key 
    bingMapsKey = "ApFr1grOeMUw9DEV4sPm60bcgz1Ye6flK6FHfPqN97tDp0BsJVsf9uQxA1Myo2AF"

    itineraryItems = []

    destination = speech_TO_txt.speechtotext()
    encodedDest = urllib.parse.quote(destination, safe='')
    routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(latitude) + "," + str(longitude) + "&wp.1=" + encodedDest + "&key=" + bingMapsKey
    request = urllib.request.Request(routeUrl)
    response = urllib.request.urlopen(request)
    r = response.read().decode(encoding="utf-8")
    result = json.loads(r)
    itineraryItems = result["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]



    for item in itineraryItems:
        print(item)
        engine.say(item["instruction"]["text"])
        engine.runAndWait()
        time.sleep(1)

