from etl.extract.extract import extract_blobs_date
from etl.transform.reconcilliation import insert_staging
from etl.transform._add_bottler_column import add_bottler_column
from src.utils.get_config import __load_config
from src.utils.get_conn import  establish_conn

config = __load_config("../../config/config.yml")
conn = establish_conn()

#1: Extract data from blob storage
for i, container in enumerate(config['containers']):
    container_name = config['containers'][container]['name']
    sas = config['containers'][container]['sas']

    df = extract_blobs_date((container_name, sas), 'IRReconciliation')

    # 2: Transform data
    df = add_bottler_column(df)
    print(df.columns)
    if i == 0:
        break

#3: Load data into staging table
#4: Reconcile data
#5: Load data into final table
#6: Send alert for job conclusion
