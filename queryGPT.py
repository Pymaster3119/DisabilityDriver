import re
from googlesearch import search
import openai

class Action:
    def __init__(self, command, argument):
        self.command = command
        self.argument = argument

def queryURL(prompt):
    #Message 1 - Make GPT give you a search prompt
    system_text = '''
You are URL GPT, an AI model made to retrieve a URL that could be used to solve a user's problem. When prompted with a user's problem, you are to follow this structure:

1. Respond with an optimized search query to find the website that can be used to fulfil the user's request. When responding in this phase, simply respond with the search query, and no other text.

2. When provided search results, you must take these results and find the result that will most suit the user's application.

Always say the most you can with the least number of words possible'''
    gpt_response = querygpt(system_text, prompt, [])
    gpt_response = "Montville NJ pay taxes online"

    #Message 2 - Make GPT give you a link
    results = search(gpt_response)
    prompt2 = ""
    for x in results:
        prompt2 += x
    querygpt(system_text, prompt2, [(prompt, gpt_response)])
    gpt_response = "https://www.cit-e.net/montville-nj/cn/TaxBill_Std/?tpid=9078"
    url_pattern = re.compile(r'(https?://\S+)')
    match = url_pattern.search(gpt_response)
    if match:
        return match.group(0)
    raise Exception("URL not found")

def queryKeystrokes(HTML):
    #Filler code - replace later
    system_text ='''
You are Web Navigation GPT, an AI model trained to take in a prompt and a website's HTML and produce a series of commands that can be used to navigate websites. You have access to the following commands:

click("<element>") - clicks an element by identifier
type("<phrase>") - use the keyboard to type a phrase
press("<button>") - press a singular button on the keyboard (e.g. enter, tab, etc.)
wait("") - wait 5 seconds for a website to load
returnhtml("") - return the new website's HTML to you for another round of analysis

These are the identifiers that can be used to access an element with the click command: classname, cssselector, xpath, id, link text, tag name.

When the user gives you a prompt and a website's HTML, you are to use the above commands to preform the action described in the prompt. Whenever attempting to load a new webpage or expand some new HTML, you MUST call returnhtml("") and stop your response there.

Use only the commands in your response. Say what you can in the least number of words possible.
''' 
    gpt_response = "Given your beautiful HTML-bs, you must do the following:\n1.click(\"ytd-searchbox\")\n2.type(\"never gonna give you up - rick astley\")\n3.press(\"ENTER\")\n4.wait(\"ukfdaskhkhjkl\")\n5.click(\"Rick Astley - Never Gonna Give You Up (Official Music Video)\")"
    pattern = re.compile(r'(click|type|press|wait)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]
    return actions

#Filler code
def querygpt(system_text, input, past_messages):
    # Create the initial message list with the system message
    messages = [{"role": "system", "content": system_text}]
    
    # Append past messages to the conversation
    for user_msg, gpt_response in past_messages:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": gpt_response})
    
    # Add the current user input to the messages
    messages.append({"role": "user", "content": input_text})
    
    # Make the API call to the OpenAI GPT-4 model
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    
    # Extract the assistant's response from the API response
    assistant_response = response['choices'][0]['message']['content']
    
    return assistant_response