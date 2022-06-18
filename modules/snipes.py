import re
import time
import random
from functools import lru_cache
from dependencies.webhooks import *
from dependencies.functions import *
from requests_html import HTMLSession

@lru_cache
def snipes(message):
    start = time.time()
    session = HTMLSession()
    product_link = message.content[8:]
    user_agents = open("dependencies/user-agents.txt", "r").read().split("\n")
    if site_name(product_link) != "snipesusa.com":
        return invalid_site("Snipes US")
    elif "html" in product_link:
        headers = {
            'User-agent': random.choice(user_agents),
            'Referer': product_link
        }
        response = session.get(product_link, headers=headers)
        product_title = response.html.search('name: "{}",')[0]
        product_price = response.html.search('price: "{}",')[0]
        product_image = response.html.search('data-src="{}" alt="')[0]
        sizes_list, variants_list = list(), list()
        for string in response.html.search_all('<span id="{}" class='):
            sizes_list.extend(string)
        for string in str(response.html.text).split(",\\"):
            if '"page_id_variant\\":' in string:
                variants_list.extend(re.findall(r'\d{11}', string))
        sizes_list = sizes_list[2:]
        for n in range(len(sizes_list)):
            sizes_list[n] = f"{sizes_list[n]} - {sorted(variants_list[:-4])[n]}"
        return construct(
            "Snipes US Variants Command",
            product_title,
            product_price,
            product_link,
            time.time() - start,
            product_image,
            None if len(format(sizes_list)) < 10 else format(sizes_list),
            format(sorted(variants_list[:-4]))
        )
    elif "html" not in product_link:
        return invalid_link("Snipes US")