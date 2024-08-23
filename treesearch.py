import queryGPT
from bs4 import *

elements = []
with open("treesearchsystemtext", "r") as txt:
    systemtext = txt.read()

def removeattributes(tag):
    
    for tag in tag.find_all(True):
        attrs = tag.attrs
        if 'id' in attrs:
            tag.attrs = {'id': attrs['id']}
        else:
            tag.attrs = {}
    
    return str(tag)

def decideonelement(element,prompt):
    response = queryGPT.querygpt(systemtext, removeattributes(element) + "\nPrompt:" + prompt, [])
    if "keep" in response:
        try:
            for i in element.children:
                if not isinstance(i, str) and not isinstance(i, NavigableString): 
                    decideonelement(i,prompt)
        except:
            if not hasattr(element, "children"):
                elements.append(element)

def removeads(soup):
    ad_keywords = ['ad', 'ads', 'advertisement', 'banner', 'sponsor', 'sponsored', 'promo']
    def isad(element):
        for attr in ['id', 'class']:
            if element.has_attr(attr):
                values = element[attr] if isinstance(element[attr], list) else [element[attr]]
                for value in values:
                    if any(keyword in value.lower() for keyword in ad_keywords):
                        return True
        return False
    ads = soup.find_all(isad)
    for ad in ads:
        ad.decompose()
    return soup

def treesearch(html, prompt):
    problem += "Select relevant fields, links and buttons necessary to fullfil thd prompt provided."
    if html.strip().lower().startswith('<!doctype'):
        html = html.split('>', 1)[1]
    soup = BeautifulSoup(html, 'html.parser')

    for forbidden in ['meta', 'script', 'head']:
        for elem in soup.find_all(forbidden):
            if isinstance(elem, Tag):
                    elem.decompose()
    soup = removeads(soup)
    for i in soup.children:
        decideonelement(soup, prompt)