import queryGPT
from bs4 import *
import tokenizer

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

def findtokens(element, depth=0, resultlist=None):
    if resultlist is None:
        resultlist = []
    if depth >= len(resultlist):
        resultlist.append([])
    if element.name:
        result = tokenizer.num_tokens_from_string(element)
        resultlist[depth].append(result)
    for child in element.children:
        if child.name:
            findtokens(child, depth + 1, resultlist)
    
    return resultlist
elementsofinterest = ['p', 'button', 'form']
def findscores(element, depth=0, scorelist=None):
    if scorelist is None:
        scorelist = []
    if depth >= len(scorelist):
        scorelist.append(0)
    if element.name in elementsofinterest:
        scorelist[depth] += 1
    for child in element.children:
        if child.name:
            findscores(child, depth + 1, scorelist)
    
    return scorelist
    

def treesearch(html, prompt):
    problem += "Select relevant fields, links and buttons necessary to fullfil the user's prompt. Remember to keep as little HTML as possible while still making the user's prompt possible based on the trimmed HTML you produce alone."
    if html.strip().lower().startswith('<!doctype'):
        html = html.split('>', 1)[1]
    soup = BeautifulSoup(html, 'html.parser')

    for forbidden in ['meta', 'script', 'head']:
        for elem in soup.find_all(forbidden):
            if isinstance(elem, Tag):
                    elem.decompose()
    soup = removeads(soup)
    '''
    for i in soup.children:
        decideonelement(soup, prompt)'''
    
    #One subtree for each child to body
    for subtree in soup.find("body").children:
        tokens = findtokens(subtree)
        scores = findscores(subtree)