import json
import re
from bs4 import BeautifulSoup
import config
import psycopg2
from requests import request
from config_of_connection import *
import collections

def insert_into_table_information(url,data,cursor):
    try:   
        query ="""INSERT INTO information
             (link_id, type, subtype, price, transactionType,
                 zip, visualisationOption, kitchen_type, building_constructionYear, building_condition,
            energy_heatingType, certificates_primaryEnergyConsumptionLevel, bedroom_count, land_surface,
            atticExists, basementExists, outdoor_garden_surface, outdoor_terrace_exists,
            specificities_SME_office_exists, wellnessEquipment_hasSwimmingPool, parkingSpaceCount_indoor,
            parkingSpaceCount_outdoor, condition_isNewlyBuilt) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (data['link_id'], data['type'], data['subtype'], data['price'], data['transactionType'], data['zip'],
                  data['visualisationOption'], data['kitchen_type'], data['building_constructionYear'],
                  data['building_condition'], data['energy_heatingType'],
                  data['certificates_primaryEnergyConsumptionLevel'], data['bedroom_count'], data['land_surface'],
                  data['atticExists'], data['basementExists'], data['outdoor_garden_surface'],
                  data['outdoor_terrace_exists'], data['specificities_SME_office_exists'],
                  data['wellnessEquipment_hasSwimmingPool'], data['parkingSpaceCount_indoor'],
                  data['parkingSpaceCount_outdoor'], data['condition_isNewlyBuilt'])
        cursor.execute(query, values)
        cursor.execute(query, (data,))
        print("Record inserted successfully into links table")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def get_data_from_link(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Referer': 'https://www.immoweb.be/'
    }
    count = 0
    try:
        url = 'https://' + url[0]
        house_html = request.get(url, headers=header)
        property_soup = BeautifulSoup(house_html.text, 'html.parser')
        script_text = \
            property_soup.find('script', text=re.compile("\s+window.dataLayer")).text.split('= ', 1)[1]
        json_data = json.loads(script_text[script_text.find('{'):script_text.rfind('}') + 1])
    except:
        pass
    try:
        property_info = json_data["classified"]
        print(property_info)
        flat_property_info = flatten(property_info)
    except:
        pass
    try:
        key_lst = ['id', 'type', 'subtype', 'price', 'transactionType', 'zip', 'visualisationOption',
                'kitchen_type',
                'building_constructionYear', 'building_condition',
                'energy_heatingType', 'certificates_primaryEnergyConsumptionLevel',
                'bedroom_count', 'land_surface', 'atticExists', 'basementExists',
                'outdoor_garden_surface', 'outdoor_terrace_exists', 'specificities_SME_office_exists',
                'wellnessEquipment_hasSwimmingPool', 'parkingSpaceCount_indoor',
                'parkingSpaceCount_outdoor',
                'condition_isNewlyBuilt']
        data = {key: value
                     for key, value in flat_property_info.items()
                     if key in key_lst}
    except:
        pass
    try:
        insert_into_table_information(data)
        count = count + 1
        print(count)
    except:  
        pass
    return data


def check_links_table(get_conn_params_from_config):
    try:
        # Connect to the database
        host, database, user, password = get_conn_params_from_config()
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        cursor = conn.cursor()
        query = "SELECT l.url FROM links l LEFT JOIN information i ON l.link_id = i.link_id WHERE i.link_id IS NULL"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            url = row[0]
            print(f"Scraping data for link: {url}")
            data = get_data_from_link(url)
            insert_into_table_information(url, data, cursor)

        # Close the database connection
        conn.commit()
        cursor.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)