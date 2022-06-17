import re
import time
from dependencies.webhooks import *
from dependencies.functions import *
from requests_html import HTMLSession

def puma(message):
    start = time.time()
    session = HTMLSession()
    product_link = message.content[5:]
    if site_name(product_link) != "us.puma.com":
        return invalid_site("Puma")
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
            elif "https://images.puma.com/image/upload" in string and "preview" in string:
                product_image = string[13:-1]
        for n in range(len(sizes_list)):
            sizes_list[n] = f"{sizes_list[n]} - {variants_list[n]}"
        if len(format(variants_list)) <= 1024 and len(variants_list) != 0:
            return construct(
                "Puma Variants Command",
                product_title,
                product_price,
                product_link,
                time.time() - start,
                product_image,
                format(sizes_list),
                format(variants_list)
            )
        return response_400("Puma")
    elif "https://us.puma.com/us/en/pd/" not in product_link:
        return invalid_link("Puma")
