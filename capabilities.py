from subprocess import Popen, PIPE
from googleapiclient.discovery import build
import pprint
import webbrowser
from time import sleep

import browser_config


browser = webbrowser.get(browser_config.DEFAULT_BROWSER)

search_api_key = "AIzaSyDku6FQCVZLb6B7CiLGkbb1OLUvJiOYXY8"
google_cse_id = "010487569967093575717:by6ahdw4bx8"

def google_search(search_term, api_key=search_api_key, cse_id=google_cse_id, max_res=5, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    count = 0
    for r in res["items"]:
    	if count<max_res:
    		pprint.pprint(r)
    		count += 1
    	else:
    		break
    return res['items']


def copy_to_clipboard(str, p=True, c=True):

    if p:
        p = Popen(['xsel', '-pi'], stdin=PIPE)
        p.communicate(input=str)
    if c:
        p = Popen(['xsel', '-bi'], stdin=PIPE)
        p.communicate(input=str)


def paste_to_active_screen(str):
	sleep(5)
	os.popen('xsel', 'wb').write(str)

def browse(url=browser_config.HOMEPAGE):
    """
    b is the webbrowser instance
    """
    browser.open_new_tab(url)

def open_browser(browser_name):
    wb = webbrowser.get(browser_name)
    wb.open(browser_config.HOMEPAGE)
