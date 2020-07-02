from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models


# Create your views here.

Base_url = 'https://losangeles.craigslist.org/search/?query='
Base_image_url = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
	return render(request, 'home.html')


def new_search(request):
	search = request.POST.get('search')
	#models.Search.objects.create(search =search)
	a=quote_plus(search)
	#print(request.POST)
	#print(search)
	final_url = Base_url+a
	#print(final_url)
	respose = requests.get(final_url)
	data  = respose.text
	#print(data)
	soup = BeautifulSoup(data, features='html.parser')
	post_listings = soup.find_all('li',{'class':'result-row'})
	
	#post_title =post_listings[0].find(class_='result-title').text
	#post_url =post_listings[0].find('a').get('href')
	#post_price = post_listings[0].find(class_ = 'result-price').text


	final_posting=[]

	for post in post_listings:
		post_title = post.find(class_='result-title').text
		post_url = post.find('a').get('href')
		if post.find(class_ ='result-price'):
			post_price = post.find(class_ ='result-price').text
		else:
			post_price='N/A'
		



	#print(post_title)
	#print(post_url)
	#print(post_price)

		if post.find(class_='result-image').get('data-ids'):
			post_image_url = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
			#print(post_image_url)
			final_image_url = Base_image_url.format(post_image_url)
			print(final_image_url)
		else:
			final_image_url = 'https://craigslist.org/images/peace.jpg'
		
		final_posting.append((post_title,post_url, post_price, final_image_url))
	#print(post_title[0].text)     
	stuff_for_frontend = {'search': search, 'final_postings':final_posting,}
	return render(request, 'my_app/new_search.html', stuff_for_frontend)
