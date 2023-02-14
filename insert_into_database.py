import psycopg2
import configparser

def get_conn_params_from_config():
    config = configparser.ConfigParser()
    config.read('database.ini')
    host = config['postgresql']['host']
    database = config['postgresql']['database']
    user = config['postgresql']['user']
    password = config['postgresql']['password']
    return host, database, user, password

def insert_into_table_links(s):
    try:
        host, database, user, password = get_conn_params_from_config()
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        query = "SELECT url FROM links WHERE url = %s"
        cursor.execute(query, (s,))
        row = cursor.fetchone()
        if row is not None:
            print("Link already exists in links table, skipping...")
        else:     
            query = "INSERT INTO links (url) VALUES (%s)"
            cursor.execute(query, (s,))
            conn.commit()
            print("Record inserted successfully into links table")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

def insert_into_table_information(required_property_info):
    try:
        host, database, user, password = get_conn_params_from_config()
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        query ="""INSERT INTO information
             (link_id, type, subtype, price, transactionType,
                 zip, visualisationOption, kitchen_type, building_constructionYear, building_condition,
            energy_heatingType, certificates_primaryEnergyConsumptionLevel, bedroom_count, land_surface,
            atticExists, basementExists, outdoor_garden_surface, outdoor_terrace_exists,
            specificities_SME_office_exists, wellnessEquipment_hasSwimmingPool, parkingSpaceCount_indoor,
            parkingSpaceCount_outdoor, condition_isNewlyBuilt) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (required_property_info,))
        conn.commit()
        print("Record inserted successfully into links table")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if(conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")