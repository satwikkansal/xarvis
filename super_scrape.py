import urllib
import urllib2
from bs4 import BeautifulSoup	


def youtube_first_search_result(q):
	textToSearch = q
	query = urllib.quote(textToSearch)
	url = "https://www.youtube.com/results?search_query=" + query
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	vids = soup.findAll(attrs={'class':'yt-uix-tile-link'})
	if vids:
	    return 'https://www.youtube.com' + vids[0]['href']

def quotes_scrape():
	textToSearch = q
	query = urllib.quote(textToSearch)
	url = "https://www.youtube.com/results?search_query=" + query
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	vids = soup.findAll(attrs={'class':'yt-uix-tile-link'})
	if vids:
	    return 'https://www.youtube.com' + vids[0]['href']