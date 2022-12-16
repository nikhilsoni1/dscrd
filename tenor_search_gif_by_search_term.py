import os
import requests
import sys
import json

tenor_search_term = "winner"
tenor_search_limit = 10

try:
    tenor_search_term = sys.argv[1]
except IndexError:
    pass

try:
    tenor_search_limit = int(sys.argv[2])
except IndexError:
    pass

if tenor_search_limit > 50:
    tenor_search_limit = 50

tenor_key = os.getenv("TENOR_KEY")
tenor_client_key = "all-discord-bot"
tenor_country = "US"
tenor_locale = "en_US"
tenor_media_filter = "gif"
tenor_ar_range = "standard"


tenor_params = dict()
tenor_params.setdefault("q", tenor_search_term)
tenor_params.setdefault("key", tenor_key)
tenor_params.setdefault("client_key", tenor_client_key)
tenor_params.setdefault("limit", tenor_search_limit)
tenor_params.setdefault("country", tenor_country)
tenor_params.setdefault("locale", tenor_locale)
tenor_params.setdefault("media_filter", tenor_media_filter)
tenor_params.setdefault("ar_range", tenor_ar_range)


url = "https://tenor.googleapis.com/v2/search"
response = requests.get(url, params=tenor_params)
response.raise_for_status()
_json = response.json()
results = _json.get("results")
gifs = list()
for r in results:
    media_formats = r.get("media_formats")
    gif = media_formats.get("gif")
    url = gif.get("url")
    gifs.append(url)

f = f"tenor-search-for-term-{tenor_search_term}.json"
with open(f, "w") as fp:
    json.dump(gifs, fp, indent=4)
