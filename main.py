import seleniumworker
import queryGPT
import time

def process(problem):
    #Extract URL
    response = queryGPT.queryURL(problem)
    seleniumworker.driver.get(response)
    time.sleep(5)
    #Extract information
    actions = queryGPT.queryKeystrokes(seleniumworker.driver.page_source)
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
        else:
            raise Exception("Unidentified command - something is wrong with if statements from lines 15-22")