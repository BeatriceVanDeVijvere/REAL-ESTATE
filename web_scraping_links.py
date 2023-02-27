from usp.tree import sitemap_tree_for_homepage
from check_if_link_exists import *
import psycopg2
from config_of_connection import *
from multiprocessing import Pool
import psycopg2.extras



def get_conn_params_from_config():
    config = configparser.ConfigParser()
    config.read('database.ini')
    host = config['postgresql'][host]
    database = config['postgresql'][database]
    user = config['postgresql'][user]
    password = config['postgresql'][password]
    return host, database, user, password



def connect_to_database():
    conn_params= get_conn_params_from_config()
    conn = psycopg2.connect(
        host=host,
        dbname=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    return conn, cursor





def disconnect_from_the_database(conn_params):
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")     

def insert_into_table_links(url,cursor,conn):  
    query = "SELECT url FROM links WHERE url = %s"
    #psycopg2.extras.execute_values(cursor, query, [(url,) for url in urls])
    cursor.execute(query, (url,))
    row = cursor.fetchone()
    if row is None:
        query = "INSERT INTO links (url) VALUES (%s)"
        cursor.execute(query, (url,))
        conn.commit()
        print("Record inserted successfully into links table")
    return url


def get_links_from_sitemap(homepage_url):
    conn_params = get_conn_params_from_config()
    cursor, conn = connect_to_database(conn_params)
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
                    url = s.strip("https://")
                    print(i)
                    insert_into_table_links(url, conn_params)
    disconnect_from_the_database(conn_params)

                
#Parallel(n_jobs=-3, require="sharedmem", verbose=10)(delayed(get_links_from_sitemap)('https://www.immoweb.be/nl'))
    
connect_to_database()
get_links_from_sitemap('https://www.immoweb.be/nl')

