import seleniumworker
import queryGPT
import time
import ui

answer = None
answers = []
questions = {}
answerindex = 0
def process(problem):
    global answer, answers
    #Extract URL
    response = queryGPT.queryURL(problem)
    seleniumworker.driver.get(response)
    time.sleep(5)
    #Extract information
    actions = queryGPT.queryKeystrokes(seleniumworker.driver.page_source, problem)
    print(actions)
    for idx, action in enumerate(actions):
        print(action.command)
        if action.command == "click":
            seleniumworker.clickElement(action.argument)
        elif action.command == "type":
            seleniumworker.type(action.argument, questions)
        elif action.command == "press":
            seleniumworker.press(action.argument)
        elif action.command == "wait":
            time.sleep(5)
        elif action.command == "returnhtml":
            if idx == len(action) - 1:
                print("RETURNING HTML")
                answers = []
                actions = queryGPT.resendHTML(seleniumworker.driver.page_source)
        elif action.command == "askquestion":
            ui.askquestion(action.argument)
            while True:
                if answer != None:
                    print("HHERE")
                    break
            answerindex += 1
            answers["answer" + str(answerindex)] = answer
        elif action.command == "clickinteligent":
            seleniumworker.intelliclick(action.argument, questions)
        else:
            raise Exception("Unidentified command - something is wrong with if statements from lines 15-22")