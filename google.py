# from googleapiclient.discovery import build
# import pprint

# my_api_key = ""
# my_cse_id = ""

# def search(search_term, api_key=my_api_key, cse_id=my_cse_id, max_res=5, **kwargs):
#     service = build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
#     count = 0
#     for r in res["items"]:
#     	if count<max_res:
#     		pprint.pprint(r)
#     		count += 1
#     	else:
#     		break
#     return res['items']

# results = google_search(
#     'stackoverflow site:en.wikipedia.org', my_api_key, my_cse_id, num=10)