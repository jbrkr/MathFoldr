from bs4 import BeautifulSoup
import requests
 
def get_wiki(term):
    # term ~= /wiki/category_theory
    qry = "https://en.wikipedia.org"+term
    page = requests.get(qry)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    link_list = list(set(links))
    clean_list = [i for i in link_list if i[:6] == '/wiki/' and ':' not in i and 'ISBN' not in i]
    title = soup.select("title")[0].text
    paragraphs = soup.select("p")
    text_content = []
    for para in paragraphs:
        text_content.append(para.text)
    output = {
        'title':title,
        'url':qry,
        'links':clean_list,
        'content':text_content
    }
    
    return output