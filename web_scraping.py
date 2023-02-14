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
from insert_into_database import *

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def get_data_from_link(s):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Referer': 'https://www.immoweb.be/'
    }
    count = 0
    #headers = ['id', 'type', 'subtype', 'price', 'transactionType', 'zip', 'visualisationOption',
        #'kitchen_type',
        #'building_constructionYear', 'building_condition',
        #'energy_heatingType', 'certificates_primaryEnergyConsumptionLevel',
        #'bedroom_count', 'land_surface', 'atticExists', 'basementExists',
        #'outdoor_garden_surface', 'outdoor_terrace_exists', 'specificities_SME_office_exists',
        #'wellnessEquipment_hasSwimmingPool', 'parkingSpaceCount_indoor', 'parkingSpaceCount_outdoor',
        #'condition_isNewlyBuilt']
    try:
        url = 'https://' + s[0]
        house_html = requests.get(url, headers=header)
        property_soup = BeautifulSoup(house_html.text, 'html.parser')
        script_text = \
            property_soup.find('script', text=re.compile("\s+window.dataLayer")).text.split('= ', 1)[1]
        json_data = json.loads(script_text[script_text.find('{'):script_text.rfind('}') + 1])
    # print(json_data)
    except:
        pass
    try:
        property_info = json_data["classified"]
        print(property_info)
        flat_property_info = flatten(property_info)
    except:
        pass
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
    except:
        pass
    try:
        insert_into_table_information(required_property_info)
        count = count + 1
        print(count)
    except:  
        pass
    return required_property_info

def get_links_from_sitemap(homepage_url):
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
        for s in urls:
            for value in prop_list:
                substring = (f'https://www.immoweb.be/nl/zoekertje/{value}/te-koop')
                if substring in s:
                        i += 1
                        s = s.strip("https://")
                        print(i)
                else:
                    pass
             insert_into_table_links(s)
        return s
                
Parallel(n_jobs=-3, require="sharedmem", verbose=10)(delayed(get_links_from_sitemap)('https://www.immoweb.be/nl'))
    

get_links_from_sitemap('https://www.immoweb.be/nl')

