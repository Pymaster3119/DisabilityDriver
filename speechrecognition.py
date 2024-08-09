import speech_recognition as sr
import threading
def process(audio, recognizer):
    try:
        text = recognizer.recognize_google(audio)
        displayCaption(text)
    except sr.UnknownValueError:
        pass

    
def live_caption():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.5
    recognizer.dynamic_energy_threshold = True
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        while True:
            try:
                audio = recognizer.listen(mic, timeout=100000,phrase_time_limit=1)
                threading.Thread(target=lambda: process(audio, recognizer)).start()
            except Exception as e:
                print(e)

#Filler function for stuff in the UI
def displayCaption(caption):
    print(caption)