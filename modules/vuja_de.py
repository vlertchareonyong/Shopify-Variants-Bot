import time
import json
import requests
from functools import lru_cache
from dependencies.webhooks import *
from requests_html import HTMLSession

@lru_cache
def vuja_de(message):
    start = time.time()
    session = HTMLSession()
    product_link = message.content[9:]
    if site_name(product_link) != "vujade-studio.com":
        return invalid_site("VUJA DÉ")
    response = session.get(product_link)
    product_title = response.html.search('<title>{}</title>')[0]
    product_price = response.html.search('"decimalValue":"{}","fractionalDigits"')[0]
    content_json = json.loads(str(response.html.search('"product":{}"showAnnouncementBar"')).replace("<Result ('", "").replace(",',) {}>", ""))
    sizes_list, variants_list, stock_list = list(), list(), list()
    for size in content_json['variants']:
        sizes_list.append(str(size['attributes']['Size']))
        variants_list.append(str(size['sku']))
        stock_list.append(str(size['stock']['quantity']))
    return construct(
        "VUJA DÉ Variants Command",
        product_title,
        product_price,
        product_link,
        time.time() - start,
        "https://www.vujade-studio.com/",
        format(sizes_list),
        format(variants_list), 
        format(stock_list),
        sum(int(stock) for stock in stock_list) + 1
    )