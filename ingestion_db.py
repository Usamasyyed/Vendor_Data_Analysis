import pandas as pd
import os 
from sqlalchemy import create_engine
import logging
import time
logging.basicConfig(

    filename= "logs/ingestion_db.log",
    level=logging.DEBUG,
    format= "%(asctime)s - %(levelname)s - %(message)s -",
    filemode="a"
)

engine = create_engine (r'mssql+pyodbc://@USAMA\SQLEXPRESS/inventory?driver=ODBC+Driver+17+for+SQL+Server')

def ingest_db(df, table_name, engine):
    '''This function will ingest the dataframe into the database tables'''
    df.to_sql(table_name, con= engine, if_exists='replace', index=False)
    
def load_raw_data():
    '''this function will load CSVs as dataframe and ingest into db'''
    start= time.time()
    folder_path=  r'C:\Users\usama\Downloads\SQL\Projects\Vendor Performance Data Analytics\data\data'

    for file in os.listdir(folder_path):
        if '.csv' in file:
            df = pd.read_csv(folder_path + '\\' + file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4],engine)
    end= time.time()
    total_time= (end - start)/60
    logging.info('------------------Ingestion Complete------------------')
    logging.info(f'Total Time Taken: {total_time} minutes')

if __name__== '__main__':
    load_raw_data()