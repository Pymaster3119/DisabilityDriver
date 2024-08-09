import tkinter as tk
import random
import threading
import main
import speech_recognition as sr

def on_focus_in(event):
    global update
    problem.delete(0, tk.END)
    problem.config(fg='black')
    update = False

index = 1
typingiteration = 0
direction = 1
update = True
def typeoutplaceholders():
    global index, typingiteration, placeholder_text, direction, update
    if not update and (leftbuttonpressed and accepttts):
        update = False
    else:
        partoffillertext = False
        for i in placeholdertexts:
            if problem.get() in i:
                partoffillertext = True
        if partoffillertext:
            try:
                typingiteration += direction
                if typingiteration != len(placeholdertexts[index]):
                    text = (placeholdertexts[index][:typingiteration])
                    problem.delete(0, tk.END)
                    problem.insert(0, text)
                    problem.config(fg='grey')
                    if typingiteration <= 0:
                        index = placeholdertexts.index(random.choice(placeholdertexts))
                        direction = 1
                else:
                    direction = -1
            except:
                pass
        root.after(50, typeoutplaceholders)
root = tk.Tk()
problem = None
accepttts = False
leftbuttonpressed = False
placeholdertexts = ['Play me "Never Gonna Give You Up" by Rick Astley on YouTube.', 'Compose an email to my boss telling him that I have a doctors appointment tomorrow and send it to him.', 'Find the form for Montville taxes.']

def start_thread():
    pblm = problem.get()
    task_thread = threading.Thread(target=lambda:main.process(pblm))
    task_thread.start()
    drawWorkingUI()


def process(audio, recognizer):
    try:
        text = recognizer.recognize_google(audio)
        problem.insert(tk.END, text)
    except sr.UnknownValueError:
        pass


recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5
recognizer.dynamic_energy_threshold = True

def listenfortts():
    while True:
        global recognizer
        if accepttts and leftbuttonpressed:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic)
                try:
                    audio = recognizer.listen(mic, timeout=100000,phrase_time_limit=1)
                    threading.Thread(target=lambda: process(audio, recognizer)).start()
                except:
                    pass

def drawStartingUI():
    global problem, accepttts
    accepttts = True

    for child in root.winfo_children():
        child.destroy()
    tk.Label(root, text= "What would you like to do today?").pack(fill=tk.X, expand=True)
    problem = tk.Entry(root, fg='grey')
    problem.bind('<FocusIn>', on_focus_in)
    problem.pack(fill=tk.X, expand=True)
    tk.Button(root, text = "Send request",command=start_thread).pack(fill=tk.X, expand=True)
    root.after(10, typeoutplaceholders)
    threading.Thread(target=listenfortts).start()

def drawWorkingUI():
    accepttts = False
    for child in root.winfo_children():
        child.destroy()
    tk.Label(root, text= "Working...").pack()

drawStartingUI()

def updateanswer(answervar):
    main.answer = answervar.get()
answervar = tk.StringVar()
def askquestion(question):
    for child in root.winfo_children():
        child.destroy()
    answervar.set("")
    tk.Label(root, text=question).pack()
    tk.Entry(root, textvariable=answervar).pack()
    tk.Button(root, text="Submit Answer", command=lambda:updateanswer(answervar)).pack()

def leftButtonUpdated(pressed):
    global leftbuttonpressed, update
    leftbuttonpressed = pressed
    if pressed:
        problem.delete(0, tk.END)
        problem.config(fg='black')
        update = False
root.bind("<ButtonPress-1>", lambda x: leftButtonUpdated (True))
root.bind("<ButtonRelease-1>", lambda x: leftButtonUpdated (False))
root.mainloop()