import queryGPT
from bs4 import *

elements = []
with open("treesearchsystemtext", "r") as txt:
    systemtext = txt.read()

def decideonelement(element):
    response = queryGPT.querygpt(systemtext, str(element), [])
    if "keep" in response:
        try:
            for i in element.children:
                if not isinstance(i, str) and not isinstance(i, NavigableString): 
                    decideonelement(i)
        except:
            if not hasattr(element, "children"):
                elements.append(element)

def treesearch(HTML):
    problem += "Select relevant fields, links and buttons."
    if html.strip().lower().startswith('<!doctype'):
        html = html.split('>', 1)[1]
    soup = BeautifulSoup(html, 'html.parser')

    for forbidden in ['meta', 'script']:
        for elem in soup.find_all(forbidden):
            if isinstance(elem, Tag):
                    elem.decompose()
    for i in soup.children:
        decideonelement(soup)