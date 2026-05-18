import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import numpy as np
import logging
from ingestion_db import ingest_db

logging.basicConfig(

    filename= "logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format= "%(asctime)s - %(levelname)s - %(message)s -",
    filemode="a"
)

def create_vendor_summary (engine):
    '''This function will merge the different tables to get the overall vendor summary and adding new columns in the resutant data'''
    vendor_sales_summary= pd.read_sql_query("""
        WITH FreightSummary AS(
        SELECT 
            VendorNumber, 
            SUM(Freight) as FreightCost
        FROM vendor_invoice
        Group BY VendorNumber), 


        PurchaseSummary AS (
        SELECT 
            p.VendorName,
            p.VendorNumber,
            p.Description,
            p.Brand,
            p.PurchasePrice,
            pp.Volume,
            pp.Price as ActualPrice,
            SUM(p.Quantity) as TotalPurchaseQuantity,
            SUM(p.Dollars) as TotalPurchaseDollars
        FROM purchases p
            JOIN purchase_prices pp
            ON p.Brand=pp.Brand
        Where p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName,p.Brand,p.Description, p.PurchasePrice, pp.Price, pp.Volume 
        ),

        SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesDollars) as TotalSalesDollars,
            SUM(SalesPrice) as TotalSalesPrice,
            SUM(SalesQuantity) as TotalSalesQuantity,
            SUM(ExciseTax) as TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand)


        SELECT
            ps.VendorNumber,
            ps.VendorName,
            ps.Brand,
            ps.Description,
            ps.PurchasePrice,
            ps.ActualPrice,
            ps.Volume,
            ps.TotalPurchaseQuantity,
            ps.TotalPurchaseDollars,
            ss.TotalSalesQuantity,
            ss.TotalSalesDollars,
            ss.TotalSalesPrice,
            ss.TotalExciseTax,
            fs.FreightCost
        FROM PurchaseSummary ps
        LEFT JOIN SalesSummary ss
            ON ps.VendorNumber = ss.VendorNo
            AND ps.Brand= ss.Brand
        LEFT JOIN FreightSummary fs
            ON ps.VendorNumber= fs.VendorNumber
        ORDER BY ps.TotalPurchaseDollars DESC
        """,engine)
    return vendor_sales_summary

def clean_data(df):
    '''This function will clean data'''
    # Changing datatype to float
    df['Volume'] = df['Volume'].astype['float']

    # filling missing value with 0
    df.fillna(0,inplace=True)

    # removing spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # Creating new columns for better analysis
    vendor_sales_summary['GrossProfit'] =  vendor_sales_summary['TotalSalesDollars'] - vendor_sales_summary['TotalPurchaseDollars']
    vendor_sales_summary['ProfitMargin'] =  vendor_sales_summary['GrossProfit'] / vendor_sales_summary['TotalSalesDollars']*100
    vendor_sales_summary['StockTurnover'] =  vendor_sales_summary['TotalSalesQuantity'] / vendor_sales_summary['TotalPurchaseQuantity']
    vendor_sales_summary['SalesToPurchaseRatio'] =  vendor_sales_summary['TotalSalesDollars'] / vendor_sales_summary['TotalPurchaseDollars']

    return df

if __name__ =='__main__':
    # Creating database connection
    engine = create_engine(r'mssql+pyodbc://@USAMA\SQLEXPRESS/inventory?driver=ODBC+Driver+17+for+SQL+Server') 

    logging.info('Creating Vendor Summary Table........')
    summary_df= create_vendor_summary(engine)
    logging.info(summary_df.head())

    logging.info('Cleaning Data........')
    clean_df= clean_data(engine)
    logging.info(clean_df.head())

    logging.info('Ingesting Data........')
    ingest_db(clean_df,'vendor_sales_summary',engine)
    logging.info('Completed')
