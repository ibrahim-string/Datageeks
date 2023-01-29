import speech_recognition as sr

sr_init = sr.Recognizer()


def speechtotext():
    with sr.Microphone() as mic:
        print("\n [ INFO ] Say something ")
        speech_data = sr_init.listen(source=mic, timeout=2)
        speech_text = sr_init.recognize_google(speech_data, language='en-US')
        # print(f" [ REPLIED ] You said {speech_text}")
        # speak(speech_text)
        return speech_text