import collections
import csv
import json
import pprint
import re
import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from urllib3.filepost import writer
from usp.tree import sitemap_tree_for_homepage
import csv

file3 = 'original.csv'
file1 = 'original.csv'
file2 = 'final1.csv'


def get_links_from_sitemap(homepage_url:'https://www.immoweb.be/nl', file3):
        ##use sitemap xml to get all the links on immoweb
        tree = sitemap_tree_for_homepage(homepage_url)
        ##go over all the links in the pages of the sitemap
        urls = [page.url for page in tree.all_pages()]
        ### if the beginning of the link matches  https://www.immoweb.be/nl/zoekertje we keep it
        prop_list = ["huis", "appartement", "industrie", "grond", "handelszaak", "kantoor",
                     "nieuwbouwproject-huizen", "nieuwbouwproject-appartementen", "garage", "vakantiehuis",
                     "opbrengsteigendom", "andere", "bed-and-breakfast", "stacaravan", "hotel", "camping",
                     "woonboot", "vakantiepark", "ander-huis"]
        i = 0
        file2 = open(file2, "w")
        for s in urls:
            print(22222222222222)
            for value in prop_list:
                print(3333333333333333)
                substring = (f'https://www.immoweb.be/nl/zoekertje/{value}/te-koop')
                if substring in s:
                        i += 1
                        s = s.strip("https://")
                        file2.write(f'{s}\n')
                print(i)


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_data_from_link(file1, file2):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Referer': 'https://www.immoweb.be/'
    }
    # options = Options()
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.binary_location =r'C:\Program Files\Mozilla Firefox\firefox.exe'
    count = 0
    with open(file1, "r") as file1:
        with open(file2, 'w', newline="", encoding='utf-8') as file2:
            headers = ['id', 'type', 'subtype', 'price', 'transactionType', 'zip', 'visualisationOption',
                       'kitchen_type',
                       'building_constructionYear', 'building_condition',
                       'energy_heatingType', 'certificates_primaryEnergyConsumptionLevel',
                       'bedroom_count', 'land_surface', 'atticExists', 'basementExists',
                       'outdoor_garden_surface', 'outdoor_terrace_exists', 'specificities_SME_office_exists',
                       'wellnessEquipment_hasSwimmingPool', 'parkingSpaceCount_indoor', 'parkingSpaceCount_outdoor',
                       'condition_isNewlyBuilt']
            writer = csv.DictWriter(file2, fieldnames=headers)
            writer.writeheader()
            reader = csv.reader(file1)
            for url in reader:
                try:
                    url = 'https://' + url[0]
                    house_html = requests.get(url, headers=header)
                    property_soup = BeautifulSoup(house_html.text, 'html.parser')
                    # convert json to dict, add location in the dict
                    script_text = \
                        property_soup.find('script', text=re.compile("\s+window.dataLayer")).text.split('= ', 1)[1]
                    json_data = json.loads(script_text[script_text.find('{'):script_text.rfind('}') + 1])
                # print(json_data)
                except:
                    continue
                try:
                    property_info = json_data["classified"]
                    print(property_info)
                    flat_property_info = flatten(property_info)
                    print(111111111111111)
                except:
                    continue
                try:
                    # get required info from property_info
                    key_lst = ['id', 'type', 'subtype', 'price', 'transactionType', 'zip', 'visualisationOption',
                               'kitchen_type',
                               'building_constructionYear', 'building_condition',
                               'energy_heatingType', 'certificates_primaryEnergyConsumptionLevel',
                               'bedroom_count', 'land_surface', 'atticExists', 'basementExists',
                               'outdoor_garden_surface', 'outdoor_terrace_exists', 'specificities_SME_office_exists',
                               'wellnessEquipment_hasSwimmingPool', 'parkingSpaceCount_indoor',
                               'parkingSpaceCount_outdoor',
                               'condition_isNewlyBuilt']
                    required_property_info = {key: value
                                              for key, value in flat_property_info.items()
                                              if key in key_lst}
                    # print(required_property_info)
                    print(2222222222222222222222222222222222222222222222222222222222)
                except:
                    continue
                try:
                    writer.writerow(required_property_info)
                    print(333333333333333333333333333333333333)
                    #file2.writelines(required_property_info)
                    print(4444444444444444444444444444444444444)
                    count = count + 1
                    print(count)
                except:  
                    continue
                
                

    Parallel(n_jobs=-2, require="sharedmem", verbose=10)(delayed(get_data_from_link)(file1, file2))
    file2.close()

get_links_from_sitemap('https://www.immoweb.be/nl', file2)
get_data_from_link('original.csv', 'final1.csv')

