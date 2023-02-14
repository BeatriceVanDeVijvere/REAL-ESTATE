# """ 'id', 'type', 'subtype', 'price', 'transactionType', 'zip', 'visualisationOption',
#         # 'kitchen_type',
#         'building_constructionYear', 'building_condition',
#         'energy_heatingType', 'certificates_primaryEnergyConsumptionLevel',
#         'bedroom_count', 'land_surface', 'atticExists', 'basementExists',
#         'outdoor_garden_surface', 'outdoor_terrace_exists', 'specificities_SME_office_exists',
#         'wellnessEquipment_hasSwimmingPool', 'parkingSpaceCount_indoor', 'parkingSpaceCount_outdoor',
#         'condition_isNewlyBuilt' """
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# Connect to the default database (postgres)
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="bea"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
# Create a cursor object
cur = conn.cursor()
# Create the database
cur.execute("CREATE DATABASE realestate;")
# Commit the changes
conn.commit()
# Connect to the database
conn = psycopg2.connect(
    host="localhost"
    database="realestate"
    user="postgres"
    password="bea"
    )
conn.commit()
# Create a cursor object
cur = conn.cursor()
# Create the first table (links)
cur.execute("""
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL
);
""")
# Create the second table (information)
cur.execute("""
CREATE TABLE information (
    id SERIAL PRIMARY KEY,
    link_id INTEGER REFERENCES links (id),
    type TEXT NOT NULL,
    subtype TEXT NOT NULL,
    price NUMERIC NOT NULL,
    transactionType TEXT NOT NULL,
    zip INTEGER NOT NULL,
    visualisationOption TEXT NOT NULL,
    kitchen_type TEXT NOT NULL,
    building_constructionYear INTEGER NOT NULL,
    building_condition TEXT NOT NULL,
    energy_heatingType TEXT NOT NULL,
    certificates_primaryEnergyConsumptionLevel NUMERIC NOT NULL,
    bedroom_count INTEGER NOT NULL,
    land_surface NUMERIC NOT NULL,
    atticExists BOOLEAN NOT NULL,
    basementExists BOOLEAN NOT NULL,
    outdoor_garden_surface NUMERIC NOT NULL,
    outdoor_terrace_exists BOOLEAN NOT NULL,
    specificities_SME_office_exists BOOLEAN NOT NULL,
    wellnessEquipment_hasSwimmingPool BOOLEAN NOT NULL,
    parkingSpaceCount_indoor INTEGER NOT NULL,
    parkingSpaceCount_outdoor INTEGER NOT NULL,
    condition_isNewlyBuilt BOOLEAN NOT NULL
);
""")
# Commit the changes
conn.commit()
# Close the cursor and connection
cur.close()
conn.close()






