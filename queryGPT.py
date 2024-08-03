import re
from googlesearch import search
import openai

class Action:
    def __init__(self, command, argument):
        self.command = command
        self.argument = argument

def queryURL(prompt):
    #Message 1 - Make GPT give you a search prompt
    with open("URLGPTSource", "r") as txt:
        system_text = txt.read()
    gpt_response = querygpt(system_text, prompt, [])
    gpt_response = "Montville NJ pay taxes online" #REMOVE

    #Message 2 - Make GPT give you a link
    results = search(gpt_response)
    prompt2 = ""
    for x in results:
        prompt2 += x
    querygpt(system_text, prompt2, [(prompt, gpt_response)])
    gpt_response = "https://www.cit-e.net/montville-nj/cn/TaxBill_Std/?tpid=9078" #REMOVE
    url_pattern = re.compile(r'(https?://\S+)')
    match = url_pattern.search(gpt_response)
    if match:
        return match.group(0)
    raise Exception("URL not found")

drivingmessages = []

def queryKeystrokes(HTML, prompt):
    global drivingmessages
    #Filler code - replace later
    with open("WebNavigatonGPT", "r") as txt:
        system_text = txt.read()
    prompt = "Prompt: " + prompt + "\nHTML: \n" + HTML
    gpt_response = querygpt(system_text, prompt, [])
    gpt_response = "Given your beautiful HTML-bs, you must do the following:\n1.click(\"ytd-searchbox\")\n2.type(\"never gonna give you up - rick astley\")\n3.press(\"ENTER\")\n4.wait(\"ukfdaskhkhjkl\")\n5.click(\"Rick Astley - Never Gonna Give You Up (Official Music Video)\")" #REMOVE
    drivingmessages.append((prompt, gpt_response))
    pattern = re.compile(r'(click|type|press|wait|returnhtml)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]
    return actions

def querygpt(system_text, input, past_messages):
    messages = [{"role": "system", "content": system_text}]
    for user_msg, gpt_response in past_messages:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": gpt_response})
    messages.append({"role": "user", "content": input})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    assistant_response = response['choices'][0]['message']['content']
    
    return assistant_response

def resendHTML(HTML):
    global drivingmessages
    with open("WebNavigatonGPT", "r") as txt:
        system_text = txt.read()
    prompt= "The new webpage has the following HTML: " + HTML
    gpt_response = querygpt(system_text, prompt, drivingmessages)
    drivingmessages.append((prompt, gpt_response))
    gpt_response = "Given your beautiful HTML-bs, you must do the following:\n1.click(\"ytd-searchbox\")\n2.type(\"never gonna give you up - rick astley\")\n3.press(\"ENTER\")\n4.wait(\"ukfdaskhkhjkl\")\n5.click(\"Rick Astley - Never Gonna Give You Up (Official Music Video)\")" #REMOVE
    pattern = re.compile(r'(click|type|press|wait|returnhtml)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]
    return actions
