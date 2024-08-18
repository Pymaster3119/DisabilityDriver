import re
from googlesearch import search
import openai
from bs4 import BeautifulSoup
import bs4
with open("key.txt", "r") as txt:
    client = openai.OpenAI(api_key=txt.read())
class Action:
    def __init__(self, command, argument):
        self.command = command
        self.argument = argument

def queryURL(prompt):
    #Message 1 - Make GPT give you a search prompt
    with open("URLGPTSource", "r") as txt:
        system_text = txt.read()
    print(prompt)
    gpt_response = querygpt(system_text, prompt, [])
    print("GPT RESPONSE:" + gpt_response)
    #Message 2 - Get a link
    results = search(gpt_response)
    prompt2 = ""
    searchresults = 0
    for j in results:
        if searchresults < 10:
            prompt2 += j + "\n"
            searchresults += 1
        else:
            break
    with open("totokenize", "w") as txt:
        txt.write(prompt2)
    gpt_response = querygpt(system_text, prompt2,[(prompt, gpt_response)])
    print(gpt_response)
    return gpt_response

drivingmessages = []
links = []
import seleniumworker
def queryKeystrokes(HTML, prompt):
    global drivingmessages
    HTML = cleanhtml(HTML, prompt)
    with open("WebNavigationGPT", "r") as txt:
        system_text = txt.read()
    prompt = "Prompt:" + prompt + "\nHTML:\n" + HTML + "\n\nCurrent URL: " + seleniumworker.driver.current_url
    with open("prompt.txt", "w") as txt:
        txt.write(prompt)
    for i in links:
        prompt += i + "\n"
    links.append(seleniumworker.driver.current_url)
    gpt_response = querygpt(system_text, prompt, [])
    print(gpt_response)
    drivingmessages.append((prompt, gpt_response))
    pattern = re.compile(r'(click|type|press|wait|returnhtml|askquestion|clickintelligent)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]      
    return actions

def querygpt(system_text, user_input, past_messages, gpt_model = "gpt-4o-mini"):
    global client
    messages = [{"role": "system", "content": system_text}]
    for user_msg, gpt_response in past_messages:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": gpt_response})
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model=gpt_model,
            messages=messages
        )
        assistant_response = response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        assistant_response = f"An error occurred: {str(e)}"
    return assistant_response


def resendHTML(prompt, HTML, questions):
    global drivingmessages
    HTML = cleanhtml(HTML, prompt)
    with open("WebNavigationGPT", "r") as txt:
        system_text = txt.read()
    prompt= "Prompt: " + prompt + "\nHTML: " + HTML + "\nCurrentURL: " + seleniumworker.driver.current_url + "\nPast URLs: " + str(links) + "\nQuestions:" + str(questions) + "\nPast Responses and Summaries:\n"
    for idx, i in enumerate(drivingmessages):
        prompt += '\t' + str(idx) + ". " + "\n\t\tDirections:"
        directions = ""
        message = i[1]
        matches = re.finditer(r'(click|type|press|wait|returnhtml|askquestion|clickintelligent)\s*\(\s*"([^"]+)"\s*\)', message)
        
        for match in matches:
            directions += "\n\t\t\t" + match
            message = re.sub(match.re, '', message, count=1)
        prompt += "\t\tSummary:\n" + message
    links.append(seleniumworker.driver.current_url)
    gpt_response = querygpt(system_text, prompt, [])
    print(gpt_response)
    drivingmessages.append((prompt, gpt_response))
    pattern = re.compile(r'(click|type|press|wait|returnhtml|askquestion|clickintelligent)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]
    print(actions)
    return actions

def produceMinimap(element):
    minimap = ''
    
    if element.name:
        minimap += f"<{element.name}>\n"
    if isinstance(element, str) or isinstance(element, bs4.NavigableString):
        minimap += element.strip() + "\n"
    if hasattr(element, 'children'):
        for child in element.children:
            minimap += produceMinimap(child)
    
    if element.name:
        minimap += f"</{element.name}>\n"
    
    return minimap

def cleanhtml(html, problem):
    if html.strip().lower().startswith('<!doctype'):
        html = html.split('>', 1)[1]
    soup = BeautifulSoup(html, 'html.parser')
    taglist = []
    currentlevel = soup.find("html")
    command = ""
    with open("HTMLParser", "r") as txt:
        systemtext = txt.read()
    messages = []

    minimap = produceMinimap(soup)
    print(minimap)
    while not 'done("fff")' in command:
        parent = currentlevel.parent().clear()
        print(parent)
        children = currentlevel.find_all(recursive=False)
        childrenstring = ""
        for idx,i in enumerate(children):
            i.clear()
            childrenstring += f"{idx + 1}. {i}"

        print(currentlevel.clear())
        userinput = f'Problem; {problem}\nCurrent tag: {currentlevel.clear()}\nParent: {parent}\nChildren:\n{children}'
        print(userinput)
        response = querygpt(systemtext, userinput, messages)
        print(response)
        match = re.match(r'<(\w+)>\("([^"]+)"\)', response)
        command = match.group(1)
        argument = match.group(2)
        if command == "up":
            currentlevel = currentlevel.parent
        elif command == "down":
            currentlevel = currentlevel.find_all(recursive=False)[int(argument)]
        elif command == "add":
            taglist.append(currentlevel.clear())
        messages.append((userinput, response))
    return ""

if __name__ == "__main__":
    with open("HTML.html", "r") as txt:
        cleanhtml(txt.read(), "What does this webpage say?")