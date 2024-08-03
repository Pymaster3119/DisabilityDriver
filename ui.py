import tkinter as tk
import random
import threading
import main

def on_focus_in(event):
    global update
    if True:
        problem.delete(0, tk.END)
        problem.config(fg='black')
        update = False

def on_focus_out(event):
    global update, typingiteration
    if problem.get() == '':
        problem.config(fg='grey')
        typingiteration = 0
        update = True

index = 1
typingiteration = 0
direction = 1
update = True
def typeoutplaceholders():
    global index, typingiteration, placeholder_text, direction, update
    if not update:
        root.after(50, typeoutplaceholders)
        print("Here")
        return
    else:
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
placeholdertexts = ['Play me "Never Gonna Give You Up" by Rick Astley on YouTube.', 'Compose an email to my boss telling him that I have a doctors appointment tomorrow and send it to him.', 'Find the form for Montville taxes.']

def start_thread():
    pblm = problem.get()
    task_thread = threading.Thread(target=lambda:main.process(pblm))
    task_thread.start()
    drawWorkingUI()

def drawStartingUI():
    global problem
    for child in root.winfo_children():
        child.destroy()
    tk.Label(root, text= "What would you like to do today?").pack(fill=tk.X, expand=True)
    problem = tk.Entry(root, fg='grey')
    problem.bind('<FocusIn>', on_focus_in)
    problem.bind('<FocusOut>', on_focus_out)
    problem.pack(fill=tk.X, expand=True)
    tk.Button(root, text = "Send request",command=start_thread).pack(fill=tk.X, expand=True)
    root.after(10, typeoutplaceholders)

def drawWorkingUI():
    for child in root.winfo_children():
        child.destroy()
    tk.Label(root, text= "Working...").pack()

drawStartingUI()

def updateanswer(answervar):
    main.answer = answervar.get()
    print(main.answer)
    print("Here")
answervar = tk.StringVar()
def askquestion(question):
    for child in root.winfo_children():
        child.destroy()
    answervar.set("")
    tk.Label(root, text=question).pack()
    tk.Entry(root, textvariable=answervar).pack()
    tk.Button(root, text="Submit Answer", command=lambda:updateanswer(answervar)).pack()

root.mainloop()
