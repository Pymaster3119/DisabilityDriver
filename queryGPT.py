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
#import seleniumworker
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
    current_tag = soup.find("html")
    with open("HTMLParser", "r") as file:
        system_text = file.read()

    command = ""
    messages = []
    minimap = ''
    for tag in soup.find_all(recursive=True):
        print(f"Tag: {tag.name}, Parent: {tag.parent.name if tag.parent else 'None'}")

    while 'done("fff")' not in command:
        print(f"Current tag: {current_tag.name}, Parent: {current_tag.parent.name if current_tag.parent else 'None'}")

    
        parent_tag = current_tag.parent
        if parent_tag:
            parent_tag.clear()
        children = list(current_tag.children)
        children_list = '\n'.join([f"{idx + 1}. {str(child)}" for idx, child in enumerate(children)])
        user_input = (
            f"Minimap: {minimap}\n"
            f"Problem: {problem}\n"
            f"Current tag: {current_tag.clear()}\n"
            f"Parent: {parent_tag}\n"
            f"Children:\n{children_list}"
        )

        response = 'down("0")' 
        match = re.match(r'(\w+)\("([^"]+)"\)', response)
        if match:
            command, argument = match.groups()
            if command == "up":
                current_tag = current_tag.parent
            elif command == "down" and children:
                current_tag = children[int(argument)]
            elif command == "add":
                messages.append(current_tag.clear())

        messages.append((user_input, response))

    return ""

if __name__ == "__main__":
    with open("HTML.html", "r") as txt:
        cleanhtml(txt.read(), "What is this website's title?")