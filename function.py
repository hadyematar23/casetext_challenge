import requests
from bs4 import BeautifulSoup
from openaicall import query_openai

def extract_negative_treatments(slug):
    url = f"https://casetext.com/api/search-api/doc/{slug}/html"

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    case_text = soup.get_text()   
    
    results = query_openai(case_text)

    content_list = []

    for key, value in results.items():
        if key != 'response1':
            content = value['choices'][0]['message']['content']
            content_list.append(content)
    
    return content_list