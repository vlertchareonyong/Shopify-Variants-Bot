import time
import requests
from functools import lru_cache
from dependencies.webhooks import *
from dependencies.functions import *

@lru_cache
def shopify(message):
    start = time.time()
    product_link = message.content[9:]
    response = requests.get(product_link.split("?")[0] + ".json")
    if response.status_code == 404:
        return response_404("Shopify")
    elif shopify_test(site_name(product_link)) is True:
        if "products" in product_link:
            product_data = response.json()
            if "product" in product_data:
                product_title = product_data['product']['title']
                product_price = product_data['product']['variants'][0]['price']
                product_image = product_data['product']['images'][0]['src']
                sizes_list, variants_list, stock_list = list(), list(), list()
                if "inventory_quantity" in product_data['product']['variants'][0]:
                    for size in product_data['product']['variants']:
                        variants_list.append(f"{size['id']}")
                        stock_list.append(f"{abs(size['inventory_quantity'])}")
                        sizes_list.append(f"{size['title']} - {size['id']}")
                    return construct(
                        "Shopify Variants Command",
                        product_title,
                        product_price,
                        product_link,
                        time.time() - start,
                        product_image,
                        format(sizes_list),
                        format(variants_list),
                        format(stock_list), 
                        sum(int(stock) for stock in stock_list) + 1
                    )
                elif "inventory_quantity" not in product_data['product']['variants'][0]:
                    for size in product_data['product']['variants']:
                        variants_list.append(f"{size['id']}")
                        sizes_list.append(f"{size['title']} - {size['id']}")
                    return construct(
                        "Shopify Variants Command",
                        product_title,
                        product_price,
                        product_link,
                        time.time() - start,
                        product_image,
                        format(sizes_list),
                        format(variants_list)
                    )
        elif "products" not in product_link:
            return invalid_link("Shopify")
    elif shopify_test(site_name(product_link)) is False:
        return invalid_site("Shopify")

    
    
