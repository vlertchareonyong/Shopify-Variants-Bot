import time
import random
import requests
from bs4 import BeautifulSoup
from dependencies.webhooks import *
from requests_html import HTMLSession

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
    product_title = str(response.html.search('type="application/ld+json">{}</script>')).split('"name": "')[1].split('"')[0]
    product_price = str(response.html.search('type="application/ld+json">{}</script>')).split('"price": ')[1].split(',')[0]
    variant_base = str(response.html.search('type="application/ld+json">{}</script>')).split('"sku": "')[1].split('"')[0]
    soup = BeautifulSoup(requests.get(product_link, headers=headers).content, 'html.parser').find(id="pdpSizeDropdown")
    if soup != None:
        variants_list, status_list = list(), list()
        status_list = [size.replace('\n','').replace('SELECT A SIZE ','') for size in soup.get_text().split("\n\n")]
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
            format(status_list),
            format(variants_list), 
        )
    return response_400("SSENSE")
