from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


# Create your views here.
def index(reqest):
    site = 'https://yandex.ru/'

    try:
        print("Перехожу на сайт")
        full_page = requests.get(site)
        print('Перешла на сайт')
        print('Ищу информацию')
        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll("span", {"class": "inline-stocks__value_inner"}, )
        convert2 = soup.findAll("span", {
            "class": "inline-stocks__cell inline-stocks__cell_type_delta inline-stocks__cell_change_small"})

    except:
        pass
    data = {
        'usd': convert[0].text + " USD " + convert2[0].text,
        'eur': convert[1].text + " EUR " + convert2[1].text,
        'oil': convert[2].text + " НЕФТЬ " + convert2[2].text
    }
    return render(reqest, 'main/top.html', data)


def about(reqest):

    return render(reqest, 'main/about.html')
