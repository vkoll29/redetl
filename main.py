from etl.extract.extract import extract_blobs_date
from etl.transform.reconcilliation import recon_insert_staging
from etl.transform.sessions import sessions_insert_staging
from etl.transform.scenes import scenes_insert_staging
from etl.transform.actuals import insert_actuals_staging
from etl.transform.metrics import metrics_insert_staging
from etl.transform.inventory import inventory_insert_staging
from etl.transform.mq import mq_insert_staging
from etl.transform.products import insert_products
from src.utils.get_config import __load_config
from src.utils.get_conn import establish_conn
from time import time

config = __load_config("config/config.yml")

conn = establish_conn()

START = time()

def main(etl_days=2, stop_days=-1):
    for i, container in enumerate(config['containers']):

        c_start = time()
        container_name = config['containers'][container]['name']
        sas = config['containers'][container]['sas']

        # 1. Reconciliation
        df_recon = extract_blobs_date((container_name, sas), 'IRReconciliation', etl_days=etl_days, stop_days=stop_days)
        recon_insert_staging(conn, df_recon, container_name)

        # 2. Scenes
        df_scenes = extract_blobs_date((container_name, sas), 'IRScenes', etl_days=etl_days, stop_days=stop_days)
        scenes_insert_staging(conn, df_scenes, container_name)

        # 3. Sessions
        df_sessions = extract_blobs_date((container_name, sas), 'IRSession', etl_days=etl_days, stop_days=stop_days)
        sessions_insert_staging(conn, df_sessions, container_name)

        # # 4. Metrics
        df_metrics = extract_blobs_date((container_name, sas), 'IRMetrics', etl_days=etl_days, stop_days=stop_days)
        metrics_insert_staging(conn, df_metrics, container_name)

        # 5. Actuals
        df_actuals = extract_blobs_date((container_name, sas), 'IRActual', etl_days=etl_days, stop_days=stop_days)
        insert_actuals_staging(conn, df_actuals, container_name)

        # 6. Inventory
        df_inventory = extract_blobs_date((container_name, sas), 'IRInventoryPricing', etl_days=etl_days, stop_days=stop_days)
        inventory_insert_staging(conn, df_inventory, container_name)

        # 7. ManualQuestions
        df_mq = extract_blobs_date((container_name, sas), 'IRMQ', etl_days=etl_days, stop_days=stop_days)
        mq_insert_staging(conn, df_mq, container_name)

        # 8. Products
        df_products = extract_blobs_date((container_name, sas), 'IRProduct', etl_days=etl_days, stop_days=stop_days)
        insert_products(conn, df_products, container_name)

        print(f"Ingesting {container_name.upper()} data took {round((time() - c_start) / 60)} minutes")
    conn.close()
    duration = time() - START
    print(f"ETL COMPLETED IN  {round(duration / 60)} MINUTES")


if __name__ == '__main__':
    main()
