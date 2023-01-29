# Importing required modules
from flask import Flask, request, render_template, Response
import cv2
import cv2
import numpy as np
from text_to_speech import speak
import time
import speech_TO_txt
import speech_recognition as sr
import urllib.request
import json
import pyttsx3
import requests
import json
import speech_TO_txt
import time
import distance


# Initializing the speech recognition
sr_init = sr.Recognizer()


# Initiating flash 
app = Flask(__name__)

# Starting to cap
cap = cv2.VideoCapture(0)


# def speechtotext():
#     with sr.Microphone() as mic:
#         print("\n [ INFO ] Say something ")
#         speech_data = sr_init.listen(source=mic, timeout=2)
#         speech_text = sr_init.recognize_google(speech_data, language='en-US')
#         # print(f" [ REPLIED ] You said {speech_text}")
#         # speak(speech_text)
#         return speech_text


# def navigationDirections():
#     response = requests.get("http://ip-api.com/json/14.97.167.154").json()
#     latitude=response['lat']
#     longitude=response['lon']
#     print(latitude)
#     print(longitude)


#     engine = pyttsx3.init()
#     # Your Bing Maps Key 
#     bingMapsKey = "ApFr1grOeMUw9DEV4sPm60bcgz1Ye6flK6FHfPqN97tDp0BsJVsf9uQxA1Myo2AF"

#     itineraryItems = []

#     destination = speech_TO_txt.speechtotext()
#     encodedDest = urllib.parse.quote(destination, safe='')
#     routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(latitude) + "," + str(longitude) + "&wp.1=" + encodedDest + "&key=" + bingMapsKey
#     request = urllib.request.Request(routeUrl)
#     response = urllib.request.urlopen(request)
#     r = response.read().decode(encoding="utf-8")
#     result = json.loads(r)
#     itineraryItems = result["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]



#     for item in itineraryItems:
#         print(item)
#         engine.say(item["instruction"]["text"])
#         engine.runAndWait()
#         time.sleep(1)


def ObjectDetection():
    count = 0

    net = cv2.dnn.readNet("./yolov3.weights", "./yolov3.cfg")
    mic = 0

    # Colors for each object frame
    colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255], [255, 0, 255]]
    color = []

    # Calculates the distance between camera and object
    def calculate_distance(width):
        # Known width of the object
        KNOWN_WIDTH = 100.0
        # Focal length of the camera
        FOCAL_LENGTH = 8.0
        # Calculate the distance
        distance = (KNOWN_WIDTH * FOCAL_LENGTH) / width
        return distance


    # Importing class text files
    with open("classes.txt", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    while cap.isOpened() :
        _, frame = cap.read()
        height, width, _ = frame.shape

        # Perform object detection
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)

        # Draw bounding boxes on the detected objects
        boxes = []
        confidences = []
        class_ids = []
        
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype("int")
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, int(w), int(h)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                
                # distance.dir() 
                # distance.destination()
                # distance.directions()
            
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN

        for i in range(len(boxes)):
            distance_list = []
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                
                distance_list.append(str(int(calculate_distance(w))))
                if min(map(int, distance_list)) < 2:
                    speak("Object approximately one meter away. Turn left or right.")
                print(min(distance_list))
                # time.sleep(5)

                if i < len(colors):
                    color = colors[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + f" {min(distance_list)}", (x, y + 30), font, 3, color, 2)
        cv2.imshow("Image", frame)
        count += 1
        if count%20 == 0:
            speak("Do u wish to contiune the journey? Yes or No")
            cmd = speech_TO_txt.speechtotext()
            if cmd == "yes":
                continue
            elif cmd == "no":
                return
        key = cv2.waitKey(1)
        if cv2.waitKey(30) == 27:
            break



#     cap.release()
#     cv2.destroyAllWindows()









# Home route
@app.route("/")
def index():
    return render_template("index.html")




# Function to generate the frame
def gen():
    while True:
        success, frame = cap.read()
        if success:
            try:
                net = cv2.dnn.readNet("./yolov3.weights", "./yolov3.cfg")
                mic = 0

                # Colors for each object frame
                colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255], [255, 0, 255]]
                color = []

                # Calculates the distance between camera and object
                def calculate_distance(width):
                    # Known width of the object
                    KNOWN_WIDTH = 100.0
                    # Focal length of the camera
                    FOCAL_LENGTH = 8.0
                    # Calculate the distance
                    distance = (KNOWN_WIDTH * FOCAL_LENGTH) / width
                    return distance


                # Importing class text files
                with open("classes.txt", "r") as f:
                    classes = [line.strip() for line in f.readlines()]

                while cap.isOpened() :
                    _, frame = cap.read()
                    height, width, _ = frame.shape

                    # Perform object detection
                    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
                    net.setInput(blob)
                    output_layers_names = net.getUnconnectedOutLayersNames()
                    layerOutputs = net.forward(output_layers_names)

                    # Draw bounding boxes on the detected objects
                    boxes = []
                    confidences = []
                    class_ids = []
                    
                    for output in layerOutputs:
                        for detection in output:
                            scores = detection[5:]
                            class_id = np.argmax(scores)
                            confidence = scores[class_id]
                            if confidence > 0.5:
                                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype("int")
                                x = int(center_x - w / 2)
                                y = int(center_y - h / 2)
                                boxes.append([x, y, int(w), int(h)])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)
                        
                    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                    font = cv2.FONT_HERSHEY_PLAIN

                    for i in range(len(boxes)):
                        distance_list = []
                        if i in indexes:
                            x, y, w, h = boxes[i]
                            label = str(classes[class_ids[i]])
                            
                            distance_list.append(str(int(calculate_distance(w))))
                            if min(map(int, distance_list)) < 2:
                                speak("Object approximately one meter away. Turn left or right.")
                            print(min(distance_list))
                            # time.sleep(5)

                            if i < len(colors):
                                color = colors[i]
                            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                            cv2.putText(frame, label + f" {min(distance_list)}", (x, y + 30), font, 3, color, 2)
                cv2.imshow("Test", frame)
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            except Exception as e:
                pass   
        else:
            continue
        


# Path to feed the video to the html
@app.route('/object_detect')
def object_detect():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route("/navigate_direction")
def navigate_direction():
    distance.lastry()
    return render_template("index.html")








# Some extra stuffs
@app.route("/requests", methods=['POST', 'GET'])
def tasks():
    return "<h1>Ariyal</h1>"





# To start the server
app.run()


cap.release()
cv2.destroyAllWindows()