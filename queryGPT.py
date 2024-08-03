import re
from googlesearch import search
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
    gpt_response = querygpt(system_text, prompt)
    gpt_response = "Montville NJ pay taxes online"

    #Message 2 - Make GPT give you a link
    results = search(gpt_response)
    prompt = ""
    for x in results:
        prompt += x
    print(prompt)
    gpt_response = "https://www.cit-e.net/montville-nj/cn/TaxBill_Std/?tpid=9078"
    url_pattern = re.compile(r'(https?://\S+)')
    match = url_pattern.search(gpt_response)
    if match:
        return match.group(0)
    raise Exception("URL not found")

def queryKeystrokes(HTML):
    #Filler code - replace later
    gpt_response = "Given your beautiful HTML-bs, you must do the following:\n1.click(\"ytd-searchbox\")\n2.type(\"never gonna give you up - rick astley\")\n3.press(\"ENTER\")\n4.wait(\"ukfdaskhkhjkl\")\n5.click(\"Rick Astley - Never Gonna Give You Up (Official Music Video)\")"
    pattern = re.compile(r'(click|type|press|wait)\s*\(\s*"([^"]+)"\s*\)')
    matches = pattern.findall(gpt_response)
    actions = [Action(command, argument) for command, argument in matches]
    return actions

#Filler code
def querygpt(system_text, input):
    print(input)
    return ""