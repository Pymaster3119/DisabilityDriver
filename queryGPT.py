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
links = []
import seleniumworker
def queryKeystrokes(HTML, prompt):
    global drivingmessages
    #Filler code - replace later
    with open("WebNavigationGPT", "r") as txt:
        system_text = txt.read()
    prompt = "Prompt: " + prompt + "\nHTML: \n" + HTML + "\n\nCurrent URL: " + seleniumworker.driver.current_url + "\nPast URLs: " + str(links)
    links.append(seleniumworker.driver.current_url)
    gpt_response = querygpt(system_text, prompt, [])
    gpt_response = 'click("On-line Tax Payment")\naskquestion("Hello question here")\nreturnhtml("")' #REMOVE
    drivingmessages.append((prompt, gpt_response))
    pattern = re.compile(r'(click|type|press|wait|returnhtml|askquestion)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]
    return actions

def querygpt(system_text, input, past_messages):
    messages = [{"role": "system", "content": system_text}]
    for user_msg, gpt_response in past_messages:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": gpt_response})
    messages.append({"role": "user", "content": input})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        assistant_response = response['choices'][0]['message']['content']
    except openai.OpenAIError as e:
        assistant_response = f"An error occurred: {str(e)}"
    return assistant_response


def resendHTML(HTML):
    global drivingmessages
    with open("WebNavigationGPT", "r") as txt:
        system_text = txt.read()
    prompt= "The new webpage has the following HTML: " + HTML
    gpt_response = querygpt(system_text, prompt, drivingmessages)
    drivingmessages.append((prompt, gpt_response))
    gpt_response = "Given your beautiful HTML-bs, you must do the following:\n1.click(\"ytd-searchbox\")\n2.type(\"never gonna give you up - rick astley\")\n3.press(\"ENTER\")\n4.wait(\"ukfdaskhkhjkl\")\n5.click(\"Rick Astley - Never Gonna Give You Up (Official Music Video)\")" #REMOVE
    pattern = re.compile(r'(click|type|press|wait|returnhtml|askquestion)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]
    return actions

#CODE TO TEST STUFF OUT
querygpt('''
         <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Positioned Text</title>
    <style>
        html, body {
            height: 100%;
            margin: 0;
            display: grid;
            place-items: center;
        }
        .grid-container {
            display: grid;
            grid-template-columns: 1fr auto;
            grid-template-rows: auto 1fr;
            width: 100%;
            height: 100%;
        }
        .spacer-x {
            grid-column: 1;
        }
        .spacer-y {
            grid-row: 1;
        }
        .text {
            grid-column: 2;
            grid-row: 2;
            align-self: start;
            justify-self: start;
        }
    </style>
</head>
<body>
    <div class="grid-container">
        <div class="spacer-x"></div>
        <div class="spacer-y"></div>
        <div class="text">flag</div>
    </div>
</body>
</html>
''', "What is the position of the text 'Flag' on this HTML website, given that it is viewed on a 1000x1000 screen?", past_messages=[])