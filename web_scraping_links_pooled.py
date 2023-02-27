from multiprocessing import Pool
import psycopg2.extras
from config_of_connection import *
from usp.tree import sitemap_tree_for_homepage

def insert_into_table_links(urls_to_insert):
    conn = None
    try:
        host, database, user, password = get_conn_params_from_config()
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        query = "INSERT INTO links (url) VALUES %s"
        psycopg2.extras.execute_values(cursor, query, [(url,) for url in urls_to_insert])
        conn.commit()
        print(f"{len(urls_to_insert)} records inserted successfully into links table")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

def process_url(url):
    prop_list = ["huis", "appartement", "industrie", "grond", "handelszaak", "kantoor",
                 "nieuwbouwproject-huizen", "nieuwbouwproject-appartementen", "garage", "vakantiehuis",
                 "opbrengsteigendom", "andere", "bed-and-breakfast", "stacaravan", "hotel", "camping",
                 "woonboot", "vakantiepark", "ander-huis"]
    for value in prop_list:
        substring = f'https://www.immoweb.be/nl/zoekertje/{value}/te-koop'
        if substring in url:
            return url.strip("https://")
    return None

def get_links_from_sitemap(homepage_url):
    tree = sitemap_tree_for_homepage(homepage_url)
    urls = [page.url for page in tree.all_pages()]
    with Pool(processes=8) as pool:
        urls_to_insert = pool.map(process_url, urls)
    urls_to_insert = [url for url in urls_to_insert if url is not None]
    if urls_to_insert:
        print(11111111111111111111111111111111111111111111111)
        insert_into_table_links(urls_to_insert)
        print(22222222222222222222222222222222222222222)
    return urls_to_insert


get_links_from_sitemap('https://www.immoweb.be/nl')