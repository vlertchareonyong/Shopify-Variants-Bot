import time
from dependencies.webhooks import *
from dependencies.functions import *
from requests_html import HTMLSession

def new_balance(message):
    start = time.time()
    session = HTMLSession()
    product_link = message.content[13:]
    if site_name(product_link) != "newbalance.com":
        return invalid_site("New Balance")
    elif "https://www.newbalance.com/pd/" in product_link and "#" not in product_link:
        response = session.get(product_link)
        product_image = str(response.html.search('","image":"{}","url":"')).split("'")[1]
        product_title = str(response.html.search('<title>{}- New Balance</title>')).split("'")[1]
        product_price = str(response.html.search('"master": "{}};')).split("'")[1].split('"')[0].replace("min", "").replace("max", " - ")
        variant_base = product_image.split("/NB/")[1].split("_")[0].upper()
        variants_list, stock_list = new_balance_parser(response, variant_base)
        if len(variants_list) <= 1024 and len(variants_list) != 0:
            return construct(
                "New Balance Variants Command",
                product_title,
                product_price,
                product_link,
                time.time() - start,
                product_image,
                None,
                format(variants_list),
                format(stock_list)
            )
        return response_400("New Balance")
    elif "https://www.newbalance.com/pd/" in product_link and "#" in product_link:
        response = session.get(product_link)
        product_title = str(response.html.search('<title>{}- New Balance</title>')).split("'")[1]
        product_price = str(response.html.search('"master": "{}};')).split("'")[1].split('"')[0].replace("min", "").replace("max", " - ")
        if "&dwvar" in product_link:
            variant_base = product_link.split("&dwvar")[-2].split("=")[-1]
            product_image = f"https://nb.scene7.com/is/image/NB/{variant_base}_nb_02_i?$pdpflexf2$&amp;wid=464&amp"
            variants_list, stock_list = new_balance_parser(response, variant_base)
            if len(variants_list) <= 1024 and len(variants_list) != 0:
                return construct(
                    "New Balance Variants Command",
                    product_title,
                    product_price,
                    product_link,
                    time.time() - start,
                    product_image,
                    None,
                    format(variants_list),
                    format(stock_list)
                )
            return response_400("New Balance")
    elif "https://www.newbalance.com/pd/" not in product_link:
        return invalid_link("New Balance")
    

            

        