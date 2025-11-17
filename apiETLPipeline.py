import logging
import sqlite3
import requests
import pandas as pd

logging.basicConfig(
    filename=f'python_log',
    filemode='w', # Clears log file every run
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
API_URL = 'https://jsonplaceholder.typicode.com/todos'
DB_PATH = 'etl_database.db'
TABLE_NAME = 'todos'

def extract(url):
    logging.info('Hitting API URL')
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception (f"API request failed with response code {response.status_code}")
    logging.info('Successfully hit API')
    return response.json()

def transform(data):
    logging.info('Transforming data')
    transformed_data=[]
    transformed_dict={}
    for i in data:
        i.pop('userId')
        for k,v in i.items():
            transformed_dict[str(k).upper()]=v
            transformed_data.append(transformed_dict)
    global total_records
    total_records = len(transformed_data)
    logging.info('Successfully transformed data')
    return transformed_data

def load(data, file_path):
    logging.info('Loading data')
    df = pd.DataFrame(data)
    csv_path = file_path
    df.to_csv(csv_path,index=False)
    logging.info(f'data successfully loaded to {csv_path}')

def load_to_sqlLite_db(data, db_path, table_name):
    logging.info('Loading data in DB')
    conn = sqlite3.connect(db_path)
    df = pd.DataFrame(data)
    df.to_sql(table_name, conn, index=False, if_exists='replace')
    conn.close()
    logging.info(f'data successfully loaded to sqLite {db_path} on table {table_name}')

try:
    api_url = API_URL
    data = extract(api_url)
    transformed_data = transform(data)
    load(transformed_data, 'etl_output.csv')
    load_to_sqlLite_db(transformed_data, DB_PATH, TABLE_NAME)
    print(f"Total records processed was {total_records}")
    logging.info(f"Total records processed was {total_records}")
except Exception as e:
    print(f'Error: {e}')

