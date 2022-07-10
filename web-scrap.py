'''
This document contains scaping codes for Tatoli that can also be used to scrap other online news portal that have similar structure.
It scarps the news articles text contents based on pre-defined list of categories for 2022.
We first defined the maximum pages for the set categories and then collect and save all the links in those categories in a list.
After that, the duplicate links are removed and then extract the content for for each link and save in a text file.
'''


import html
from bs4 import BeautifulSoup as tl
import requests
import re


#TATOLI - www.tatoli.tl
tatoli_news = 'files/dataset_tetun_tatoli.txt'

categories = ['politika', 'edukasaun', 'saude', 'eleisaun', 'ekonomia', 'defeza', 'seguransa', 'justisa', 'lei', 'kapital', 'inkluzaun-sosial', 'internasional', 'desportu']
# #less than 20 news articles: ['sosiedade-sivil', 'mensajen-estadu']

page_num = range(1, 101) # limit to 10 pages
pages_links = []
for category in categories:
    for p_num in page_num:
        url = "http://www.tatoli.tl/category/" + category + "/page/" + str(p_num) + '/'
        pages_links.append(url)

lists_news = []
for page_links in pages_links:
    print(page_links)
    page = requests.get(page_links)
    soup = tl(page.content, "html.parser")
    # find all links for each page then exctracting it for 2022
    for link in soup.find_all('a'):
        if '2022' in link.get('href'):
            lists_news.append(link.get("href"))

lists_news = list(set(lists_news))
for list_news in lists_news:
    print(list_news)
    news_page = requests.get(str(list_news))
    news_content =tl(news_page.content, "html.parser")
    initial_content = news_content.get_text()
    # split if it contains word "(TATOLI)—" otherwise skip
    if "(TATOLI)—" in initial_content:
        initial_split = initial_content.split("(TATOLI)—")
        if "Jornalista" in initial_split[1]: # split if it contains word "Jornalista" otherwise skip
            final_split = initial_split[1].split("Jornalista")
            news = final_split[0].lower() # get the text contents before "Jornalista" and after "(TATOLI)—"
            # remove related news and image labels
            filter_list = ['notísia relevante:', 'imajen tatoli/']
            filter = '|'.join(filter_list)
            filter_news = re.sub(filter, '', news)

            with open(tatoli_news, 'a', encoding='utf-8') as file:
                file.writelines(str(filter_news))
            file.close()
        else:
            continue
    else:
        continue
