import re
from googlesearch import search
import openai
from bs4 import BeautifulSoup
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
    gpt_response = querygpt(system_text, prompt, [])
    print(gpt_response)
    #Message 2 - Make GPT give you a link
    results = search(gpt_response)
    prompt2 = ""
    for x in results:
        prompt2 += x
    gpt_response = querygpt(system_text, prompt2, [(prompt, gpt_response)])
    print(gpt_response)
    url_pattern = re.compile(r'(https?://\S+)')
    match = url_pattern.search(gpt_response)
    if match:
        return match.group(0)
    raise Exception("URL not found")

drivingmessages = []
links = []
import seleniumworker
def queryKeystrokes(HTML, prompt):
    global drivingmessages
    HTML = cleanhtml(HTML)
    #Filler code - replace later
    with open("WebNavigationGPT", "r") as txt:
        system_text = txt.read()
    prompt = "Prompt: " + prompt + "\nHTML: \n" + HTML + "\n\nCurrent URL: " + seleniumworker.driver.current_url + "\nPast URLs: " + str(links)
    links.append(seleniumworker.driver.current_url)
    gpt_response = querygpt(system_text, prompt, [])
    print(gpt_response)
    drivingmessages.append((prompt, gpt_response))
    pattern = re.compile(r'(click|type|press|wait|returnhtml|askquestion|clickintelligent)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]      
    return actions

def querygpt(system_text, user_input, past_messages):
    global client
    messages = [{"role": "system", "content": system_text}]
    for user_msg, gpt_response in past_messages:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": gpt_response})
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
    print(prompt)
    links.append(seleniumworker.driver.current_url)
    gpt_response = querygpt(system_text, prompt, drivingmessages)
    drivingmessages.append((prompt, gpt_response))
    pattern = re.compile(r'(click|type|press|wait|returnhtml|askquestion|clickintelligent)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]
    return actions

tagstokeep = [
    'html', 'head', 'body', 'div', 'header', 'footer', 'main', 'section',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'strong', 'em',
    'ul', 'ol', 'li', 'a', 'form', 'input', 'textarea', 'button', 'label', 'select', 'option', 'img'
]

def cleansoup(soup):
        for tag in soup.find_all(True):
            if tag.name not in tagstokeep:
                tag.decompose()
            else:
                cleansoup(tag)

def cleanhtml(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    cleansoup(soup)
    print(soup.prettify())
    return soup.prettify()

if __name__ == "__main__":
    response = querygpt("You are a helpful assistant", "Write an essay about ice cream on a summer's day", [])
    print(response)