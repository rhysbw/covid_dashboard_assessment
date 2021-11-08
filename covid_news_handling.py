"""
Rhys Broughton - 710043307 - 03/11/2021
CA for ECM1400
this file is to handle all covid news data, it will need to find relevant articles, remove seen articles, and update the articles thru scheduling
"""

import requests
import json


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    url = ('https://newsapi.org/v2/everything?'
           f'q={covid_terms}&'
           'sortBy=popularity&'
           'apiKey=46629bb33d904db6b48d10638128d4c9')
    response = requests.get(url)

    response_as_json = response.json()
    # print(response_as_json['articles'])
    articles = response_as_json['articles']

    # gets needed data for the top 50 articles
    titles = []
    descriptions = []
    urls = []
    contents = []
    for i in range(20):
        current_article = articles[i]
        titles.append(current_article["title"])
        descriptions.append(current_article['description'])
        urls.append(current_article['url'])
        contents.append(current_article['content'])

    print(titles)
    news = {

        "title": titles,
        "description": descriptions,
        "url": urls,
        "content": contents

    }

    print(news)
    remove_article(0,news)


def remove_article(to_remove, news):
    del news["title"][to_remove]

    print(news)
