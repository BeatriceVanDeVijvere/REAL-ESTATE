import psycopg2
import configparser
from web_scraping_links import *
from config_of_connection import *


def check_if_link_exists(url, get_conn_params_from_config):
    try:
        # Connect to the database
        host, database, user, password = get_conn_params_from_config()
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        cursor = conn.cursor()
    #read links 

    # Check if the link exists in the links table
        query = "SELECT link_id FROM links WHERE url = %s"
        cursor.execute(query, (url,))
        row = cursor.fetchone()
        if row is not None:
            # If the link exists, fetch the data from the link and insert it into the information table
            link_id = row[0]
            print("Link already exists in links table, fetching data...")
            data = get_data_from_link(url)
            data['link_id'] = link_id
            insert_into_table_information(data)
        else:
            # If the link does not exist, insert it into the links table and fetch the data from the link
            print("Link not found in links table, inserting...")
            query = "INSERT INTO links (url) VALUES (%s) RETURNING link_id"
            cursor.execute(query, (url,))
            link_id = cursor.fetchone()[0]
            data = get_data_from_link(url)
            data['link_id'] = link_id
            insert_into_table_information(data)

        # Close the database connection
        conn.commit()
        cursor.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)