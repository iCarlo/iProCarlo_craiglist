import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
# Create your views here.

BASE_CRAIGLIST_URL = 'https://manila.craigslist.org/search/jjj?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search_text=search)

    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_date = post.find(class_='result-date').text

        if post.find(class_='result-hood'):
            post_place = post.find(class_='result-hood').text
        else:
            post_place = "N/A"

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://www.craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_place, post_image_url, post_date))

    items_searched = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'list_app/new_search.html', items_searched)
