# Create your tasks here
from celery import shared_task
import random

import requests
from lxml import html

from .models import News, Politicon

def getAndParseHtml(content, lxmlStr):
    doc = html.document_fromstring(content)
    text = doc.xpath(lxmlStr)
    return text

@shared_task
def information_panel():
    content_news = requests.get('https://new-science.ru').content
    content = requests.get('https://broker.ru/brokerage/professionals').content

    changes = getAndParseHtml(content, '/html/body/section/section/section[3]/div/div/div/div[1]/div[2]/ul/li/div[2]/div[2]/div[1]/text()')
    cours = getAndParseHtml(content, '/html/body/section/section/section[3]/div/div/div/div[1]/div[2]/ul/li/div[1]/div/text()')

    path_title = '//*[@id="tie-block_1560"]/div/div/ul/li/div/h2/a/text()'
    path_comment = '//*[@id="tie-block_1560"]/div/div/ul/li/div/p/text()'
    path_href_news_content = '//*[@id="tie-block_1560"]/div/div/ul/li/div/a'
    path_news_content = '//*[@id="the-post"]/div[1]/p/text()'
    
    news_titles = getAndParseHtml(content_news, path_title)
    news_comments = getAndParseHtml(content_news, path_comment)
    href_news_content = [i.get('href') for i in getAndParseHtml(content_news, path_href_news_content)]
    news_content = [getAndParseHtml(requests.get(i).content, path_news_content) for i in href_news_content]
    
    
    data = {
        'oil': ' '.join([cours[0], changes[0]]),
        'usd': ' '.join([cours[3], changes[3]]),
        'euro': ' '.join([cours[4], changes[4]]),
    }

    # -------------
    Politicon.objects.all().delete()
    cours_object = Politicon(euro= data['euro'], dollar= data['usd'], oil= data['oil'])
    cours_object.save()
    # -------------
    len_news = len(news_titles)
    News.objects.all().delete()
    for i in range(len_news):
        new = News(
            id= i + 1,
            title= news_titles[i],
            subtitle= news_comments[i],
            content= ' '.join(news_content[i])
        ).save()
    
    return True