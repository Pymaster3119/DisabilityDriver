import speech_recognition as sr
recognizer = sr.Recognizer()
microphone = sr.Microphone()

with microphone as source:
    print("Adjusting for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")

    while True:
        print("Listening for input...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(text)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))