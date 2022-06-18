import re
import time
import random
import requests
from bs4 import BeautifulSoup
from functools import lru_cache
from dependencies.webhooks import *
from requests_html import HTMLSession

@lru_cache
def ssense(message):
    start = time.time()
    product_link = message.content[8:]
    user_agents = open("dependencies/user-agents.txt", "r").read().split("\n")
    if site_name(product_link) != "ssense.com":
        return invalid_site("SSENSE")
    session = HTMLSession()
    headers = {
        'User-agent': random.choice(user_agents),
        'Referer': product_link
    }
    response = session.get(product_link, headers=headers)
    if response.status_code == 403:
        return response_403("SSENSE")
    product_title = response.html.search('"name": "{}",')[0]
    product_price = response.html.search('"price": {},')[0]
    variant_base = response.html.search('"sku": "{}",')[0]
    soup = BeautifulSoup(requests.get(product_link, headers=headers).content, 'html.parser').find(id="pdpSizeDropdown")
    if soup != None:
        variants_list, sizes_list, stock_list = list(), list(), list()
        sizes_list = [size.replace('\n','').replace('SELECT A SIZE ','') for size in soup.get_text().split("\n\n")]
        for size in sizes_list:
            if "-" in size:
                try:
                    stock_list.append(re.findall(r'\d', size.split("-")[1])[0])
                except:
                    stock_list.append("0")
                sizes_list[sizes_list.index(size)] = size.split(" - ")[0]
            else:
                stock_list.append("1+")
        for variant in str(soup).split('_'):
            if variant_base in variant:
                variants_list.append(variant.split('"')[0])
        return construct(
            "SSENSE Variants Command",
            product_title,
            product_price,
            product_link,
            time.time() - start,
            "https://www.ssense.com/",
            format(sizes_list),
            format(variants_list), 
            format(stock_list)
        )
    return response_400("SSENSE")
