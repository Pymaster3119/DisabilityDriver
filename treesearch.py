import queryGPT
from bs4 import *
import bs4
import tokenizer
import random

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
    print(str(element) + "\nPrompt:" + prompt)
    response = queryGPT.querygpt(systemtext, str(element) + "\nPrompt:" + prompt, [])
    print(response)
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
        result = tokenizer.num_tokens_from_string(str(element))
        resultlist[depth].append(result)
    if not isinstance(element, bs4.NavigableString):
        for child in element.children:
            if child.name:
                findtokens(child, depth + 1, resultlist)
    
    return resultlist
elementsofinterest = ['p', 'button', 'form', 'input']


def findscores(element):
    output = []
    parent = element.parent
    while parent is not None:
        currentscore = 0
        for i in elementsofinterest:
            num_elements = len(parent.find_all(element))
            currentscore += num_elements
        parent = parent.parent
    return output

    
tokens = []
scores = []

def fitness(index, alpha=0.5):
    return alpha * tokens[index] - (1 - alpha) * scores[index]


def selectparents(population, alpha):
    tournamentsize = 3
    selected = random.sample(population, tournamentsize)
    selected.sort(key=lambda x: fitness(x, alpha))
    return selected[0], selected[1]


def crossover(parent1, parent2):
    return random.choice([parent1, parent2])


def mutate(child, mutationrate=0.1):
    if random.random() < mutationrate:
        return random.randint(0, len(tokens) - 1)
    return child

def countmatchingdescendants(element):
    count = 0
    for descendant in element.descendants:
        if descendant.name in elementsofinterest:
            count += 1
    return count

def geneticalgorithm(populationsize=10, generations=50, alpha=0.5, mutationrate=0.1):
    population = [random.randint(0, len(tokens) - 1) for i in range(populationsize)]
    for generation in range(generations):
        newpopulation = []
        for i in range(populationsize):
            parent1, parent2 = selectparents(population, alpha)
            child = crossover(parent1, parent2)
            child = mutate(child, mutationrate)
            newpopulation.append(child)
        population = newpopulation
    bestindex = min(population, key=lambda x: fitness(x, alpha))
    return bestindex

tokill = []
def treesearch(html, problem):
    problem += " Select relevant fields, links and buttons necessary to fullfil the user's prompt. Remember to keep as little HTML as possible while still making the user's prompt possible based on the trimmed HTML you produce alone."
    if html.strip().lower().startswith('<!doctype'):
        html = html.split('>', 1)[1]
    soup = BeautifulSoup(html, 'html.parser')
    for forbidden in ['meta', 'script', 'head']:
        for elem in soup.find_all(forbidden):
            if isinstance(elem, bs4.Tag):
                elem.decompose()
    soup = removeads(soup)
    comments = soup.find_all(text=lambda text: isinstance(text, bs4.Comment))
    for comment in comments:
        comment.extract()
    print(soup)
    
    
    #Find levels list
    levels = []
    current_level = [soup]
    
    while current_level:
        next_level = []
        level_tags = []
        for element in current_level:
            if element.name:
                level_tags.append(element.name)
            for child in element.find_all(recursive=False):
                next_level.append(child)
        levels.append(level_tags)
        current_level = next_level
    
    print('\n\n\n\n\n\n\n')
    print(levels)
    return soup

if __name__ == "__main__":
    with open("HTML.html", 'r') as txt:
        treesearch(txt.read(), "Pay my taxes to Montviille New Jersey")