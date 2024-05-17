from etl.extract.extract import extract_blobs_date
from src.utils.get_config import __load_config

config = __load_config("config/config.yml")


for container in config['containers']:
    container_name = config['containers'][container]['name']
    sas = config['containers'][container]['sas']

    extract_blobs_date((container_name, sas), 'V2/Data/IRMetrics')
