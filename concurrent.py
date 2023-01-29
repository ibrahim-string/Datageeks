import speech_TO_txt
import objectDetetction
import distance
from text_to_speech import speak
import speech_recognition


while True:
    try:
        choice=speech_TO_txt.speechtotext()
        speak("Where would you like to go today. say short  for short distance Navigation Or say long for Path guide.")
        if choice=='1' or choice=='short' or choice=='shoort' :
            objectDetetction.new()
        elif choice=='2' or choice=='long' or choice=='loong':
            distance.lastry()
        else:
            pass
    except speech_recognition.UnknownValueError:
            speak("Pardon me, Could grasp it. Could you please repeat")
button = tk.Button(root ,text=" TAP ME", command=main)
button["bg"]="red"
button["font"]=("Times New Roman",25)
button.config(width=30,height= 30)
button.pack()
root.mainloop()
