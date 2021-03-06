import re
import time
from functools import lru_cache
from dependencies.webhooks import *
from dependencies.functions import *
from requests_html import HTMLSession

@lru_cache
def puma(message):
    start = time.time()
    session = HTMLSession()
    product_link = message.content[5:]
    if site_name(product_link) != "us.puma.com":
        return invalid_site("Puma US")
    elif "https://us.puma.com/us/en/pd/" in product_link:
        response = session.get(product_link)
        sizes_list, variants_list, product_image = list(), list(), list()
        product_title = response.html.search('\\",\\"name\\":\\"{}\\",\\"description\\')[0]
        for string in str(response.html.text).split(",\\"):
            if "productId" in string:
                variants_list.extend(re.findall(r'\d+', string))
            elif '"label\\":\\"' in string and re.findall(r'["label\\":\\"]\d+[.]?\d?[\\]', string):
                sizes_list.extend(re.findall(r'\d+[.]?\d?', string))
            elif "salePrice\\" in string:
                product_price = re.findall(r'\d+', string)[0]
            #elif "https://images.puma.com/image/upload" in string and "preview" in string:
                #product_image = string[13:-1]
        for n in range(len(sizes_list)):
            sizes_list[n] = f"{sizes_list[n]} - {variants_list[n]}"
        if len(format(variants_list)) <= 1024 and len(variants_list) != 0:
            return construct(
                "Puma US Variants Command",
                product_title,
                product_price,
                product_link,
                time.time() - start,
                "https://us.puma.com/",
                None if len(format(sizes_list)) < 10 else format(sizes_list),
                format(variants_list)
            )
        return response_400("Puma US")
    elif "https://us.puma.com/us/en/pd/" not in product_link:
        return invalid_link("Puma US")
