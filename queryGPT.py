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

def produceminimap(element, selected):
    minimap = ''
    if element.name:
        minimap += f"<{element.name}>"
    if isinstance(element, (str, bs4.NavigableString)):
        minimap += element.strip() + ""
    if hasattr(element, 'children'):
        for child in element.children:
            minimap += produceminimap(child, selected)
    if element.name:
        minimap += f"</{element.name}>"
    
    if element == selected:
        minimap += "<---------"
    if not isinstance(element, (str, bs4.NavigableString)):
        minimap += "\n"
    
    return minimap

def processnode(soup, element, tags):
    if element in tags:
        element.keepme = True
        return True
    if hasattr(element, 'children'):
        for c in element.children:
            if processnode(soup, c, tags):
                element.keepme = True
                return True
    return False

def deleteunmarked(soup, element):
    if hasattr(element, 'children'):
        for c in element.children:
            if isinstance(c, bs4.Tag):
                if c.keepme != True:
                    c.decompose()
                else:
                    deleteunmarked(soup, c)
            

def addelement(tags_list, soup):
    processnode(soup, soup.find("html"), tags_list)
    deleteunmarked(soup, soup.find("html"))
    return soup.prettify()

def printSolo(elem):
    attrs = ' '.join([ f"{k}='{v}'" for (k,v) in elem.attrs.items()])
    text = [x.strip() for x in elem.children if isinstance(x, bs4.NavigableString)]
    text = [x for x in text if len(x)>0]
    text = ' '.join(text)
    output = f"<{elem.name} {attrs}>{text}</{elem.name}>"
    return output

def cleanhtml(html, problem):
    if html.strip().lower().startswith('<!doctype'):
        html = html.split('>', 1)[1]
    
    soup = BeautifulSoup(html, 'html.parser')
    current_tag = soup.find("html")
    
    with open("HTMLParser", "r") as file:
        system_text = file.read()
    
    output = []
    messages = []
    idx = 0
    response = ''
    while 'done' not in response:
        minimap = produceminimap(soup, current_tag)
        parent_tag = current_tag.parent
        children = [child for child in current_tag.children if not isinstance(child, str)]
        user_input = f"Minimap: {minimap}\nProblem: {problem}\nCurrent tag: {current_tag.name}\nParent: {parent_tag.name if parent_tag else 'None'}\nChildren:\n" + '\n'.join([f"{idx + 1}. {printSolo(child)}" for idx, child in enumerate(children)])
        with open('inputs.txt', "a") as txt:
            txt.write(user_input + "\n\n\n")
        response = querygpt(system_text, user_input, messages)
        with open('responses.txt', "a") as txt:
            txt.write(response + "\n\n\n")
        idx += 1
        if "up" in response:
            current_tag = current_tag.parent
        elif "select" in response:
            output.append(current_tag)
        elif "down" in response:
            match = re.match(r'down\("([^"]+)"\)', response)
            if match:
                argument = match.group(1)
                if 1 <= int(argument) <= len(children):
                    current_tag = children[int(argument) - 1]
        elif "done" in response:
            break
        messages.append((user_input, response))

    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(idx)
    return addelement(output, soup)

if __name__ == "__main__":
    with open("HTML.html", "r") as txt:
        print(cleanhtml(txt.read(), input("Question?: ")))