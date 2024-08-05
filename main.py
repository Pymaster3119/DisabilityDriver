import seleniumworker
import queryGPT
import time
import ui

answer = None
answers = {}
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
            seleniumworker.type(action.argument, answers)
        elif action.command == "press":
            seleniumworker.press(action.argument)
        elif action.command == "wait":
            time.sleep(5)
        elif action.command == "returnhtml":
            print("RETURNING HTML")
            actions = queryGPT.resendHTML(problem, seleniumworker.driver.page_source, answers)
        elif action.command == "askquestion":
            ui.askquestion(action.argument)
            while True:
                if answer != None:
                    print("HHERE")
                    break
            answers[action.argument] = answer
            print("done")
        elif action.command == "clickinteligent":
            seleniumworker.intelliclick(action.argument, answers)
        else:
            raise Exception("Unidentified command")
    ui.drawStartingUI()