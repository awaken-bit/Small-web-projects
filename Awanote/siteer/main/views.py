from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


# Create your views here.
def index(reqest):

    return render(reqest, 'main/top.html')


def about(reqest):

    return render(reqest, 'main/about.html')
