import seleniumworker
import queryGPT
import time
import ui

answer = None
answers = []
def process(problem):
    global answer, answers
    #Extract URL
    response = queryGPT.queryURL(problem)
    seleniumworker.driver.get(response)
    time.sleep(5)
    #Extract information
    actions = queryGPT.queryKeystrokes(seleniumworker.driver.page_source, problem)
    print(actions)
    for action in actions:
        print(action.command)
        if action.command == "click":
            seleniumworker.clickElement(action.argument)
        elif action.command == "type":
            seleniumworker.type(action.argument)
        elif action.command == "press":
            seleniumworker.press(action.argument)
        elif action.command == "wait":
            time.sleep(5)
        elif action.command == "returnhtml":
            answers = []
            actions = queryGPT.resendHTML(seleniumworker.driver.page_source)
        elif action.command == "askquestion":
            ui.askquestion(action.argument)
            while True:
                if answer != None:
                    break
                time.sleep(0.25)
            answers.append(answer)
        else:
            raise Exception("Unidentified command - something is wrong with if statements from lines 15-22")