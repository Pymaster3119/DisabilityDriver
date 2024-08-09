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
    gpt_response = "Indian classical music or smth" #querygpt(system_text, prompt, [])
    print(gpt_response)
    #Message 2 - Get a link
    results = search(gpt_response)
    prompt2 = ""
    for j in results:
        prompt2 += j
    gpt_response = "https://www.youtube.com/results?search_query=indian+classical+music"#querygpt(system_text, prompt2,[(prompt, gpt_response)])
    print(gpt_response)
    return gpt_response

drivingmessages = []
links = []
import seleniumworker
def queryKeystrokes(HTML, prompt):
    global drivingmessages
    HTML = cleanhtml(HTML)
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
    HTML = cleanhtml(HTML)
    with open("WebNavigationGPT", "r") as txt:
        system_text = txt.read()
    prompt= "Prompt: " + prompt + "\nHTML: " + HTML + "\nCurrentURL: " + seleniumworker.driver.current_url + "\npastURLs: " + str(links) + "\nquestions:" + str(questions)
    links.append(seleniumworker.driver.current_url)
    gpt_response = querygpt(system_text, prompt, drivingmessages)
    print(gpt_response)
    drivingmessages.append((prompt, gpt_response))
    pattern = re.compile(r'(click|type|press|wait|returnhtml|askquestion|clickintelligent)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]
    print(actions)
    return actions

def cleanhtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    tagdict = {}
    
    body = soup.find('body')
    
    if body:
        for i in range(10):
            for tag in body.find_all(['style', 'link', 'script', 'img', 'svg', 'css', 'path', 'video']):
                tag.decompose()
        svgs = body.find_all('svg')
        for svg in svgs:
            for child in svg.find_all(True, recursive=True):
                child.decompose()
            svg.decompose()
        for i in soup.find_all():
            if i.name in tagdict.keys():
                tagdict[i.name] += 1
            else:
                tagdict[i.name] = 1
        print(tagdict)
        htmlhalfcleaned = str(body)
        htmlhalfcleaned = re.sub(r'class="[^"]*"', '', htmlhalfcleaned)
        htmlhalfcleaned = re.sub(r'style="[^"]*"', '', htmlhalfcleaned)
        return htmlhalfcleaned
    else:
        return ''

if __name__ == "__main__":
    response = querygpt("You are a helpful assistant", "Write an essay about ice cream on a summer's day", [])
    print(response)