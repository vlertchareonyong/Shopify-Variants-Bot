import json
import requests

def site_name(product_link):
    site_name = product_link.split("//")[1].split("/")[0]
    if site_name.startswith("www."):
        return site_name[4:]
    return site_name
    
def shopify_test(site_name): 
    shopify_sites = open("dependencies/shopify-sites.txt", "r+")
    if site_name in shopify_sites.read():
        return True
    test_link = "http://" + site_name + "/admin" 
    responses = requests.get(test_link) 
    for response in responses.history:    
        if "shopify" in response.url:
            shopify_sites.write(f"{site_name}\n")
            return True
    return False

def new_balance_parser(response, variant_base):
    variants_list, status_list  = list(), list()
    variants_json = json.loads(str(response.html.search('<script>productInfo{};</script>')).split("=")[1][:-7]) 
    products_json = json.loads("{" + str(response.html.search('{"messages":{"IN_STOCK":"In Stock","LOW_STOCK":"{0} Item(s) in Stock","NOT_AVAILABLE":""},{}};</script>')).split("'")[3] + "}")
    for product in variants_json['variants']: 
        if variant_base in product['id']:
            variants_list.append(product['id']) 
            try:
                products_json["variants"][product['id']]["isLowInventory"]
            except:
                status_list.append(products_json["variants"][product['id']]["status"])
            else:
                status_list.append("🟡 LOW STOCK")
    status_list = [line.replace('IN_STOCK','🟢 IN STOCK') for line in status_list]
    status_list = [line.replace('NOT_AVAILABLE','🔴 OUT OF STOCK') for line in status_list]
    return variants_list, status_list

def format(list): 
    return "```\n" + "".join(" " + line + " \n" for line in list) + "\n```"