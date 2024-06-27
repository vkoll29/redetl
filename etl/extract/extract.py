import io
from typing import Tuple
from datetime import datetime, timedelta
import pandas as pd
from azure.storage.blob import BlobServiceClient
import time

from src.utils.get_config import __load_config

config = __load_config('config/config.yml')
URI = config['account']['uri']


def extract_blobs_date(
        creds: Tuple[str, str],
        ir_type: str,
        etl_days: int = 1,
        stop_days: int = -1,
        **kwargs
) -> pd.DataFrame:
    """
        Extract a specific blob or list of blobs based on last modified date.
        :param creds: the credentials for the container; in order of: container, key
        :param ir_type: the IR blob type to extract
        :param etl_days: the number of days to extract data for into the past from today. defaults to 1
        :param stop_days: how many days to stop at with respect to today. -1 means stop tomorrow


        :param kwargs: include the following keyword params to be more specific about the data to extract:
            - part_file_name - specify this to extract only a specific set of file(s) within a folder.
            - length - specify whether you want to extract all data or just a subset of it. Currently, it is imperative
            to extract a subset because it is only used to generate the data schema.
        :return: a pandas dataframe of the extracted blob
    """

    start_date: datetime.date = (datetime.today() - timedelta(days=etl_days)).date()
    end_date: datetime.date = (datetime.today() - timedelta(days=stop_days)).date()

    container, sas = creds
    blobs = []
    blob_dfs = []  # will contain all the dfs generated from each parquet file
    start = time.time()
    try:
        # create blob service client for interacting with blob storage
        blob_service_client = BlobServiceClient(account_url=URI, credential=sas)
        # create a container instance
        container_client = blob_service_client.get_container_client(container)
        ir_blobs = container_client.list_blobs(name_starts_with=f"V2/Data/{ir_type}/") # added the slash to the end of the folder name to separe IRActual from IRActualPrice

        # this extracts blobs based on last modified date i.e. within the start and end dates exclusive of end date
        for blob in ir_blobs:

            # print(blob)
            if start_date <= blob.last_modified.date() < end_date:
                blobs.append(blob_service_client.get_blob_client(container=container, blob=blob))

        for blob in blobs:
            # print(blob.get_blob_properties()['name'], blob.get_blob_properties()['container'])
            blob_client = blob_service_client.get_blob_client(container=container, blob=blob.blob_name)

            if 'length' in kwargs:
                blob_content = blob_client.download_blob(offset=0, length=kwargs['length']).readall()
            else:
                blob_content = blob_client.download_blob().readall()

            df = pd.read_parquet(io.BytesIO(blob_content))
            blob_dfs.append(df)
            # for i, row in df.iterrows():
            #     print(row)
            #     if i > 10:
            #         break
        print(f"Extracted {ir_type} data in {time.time() - start} seconds")
        return pd.concat(blob_dfs, axis=0, ignore_index=True) # TODO: Handle cases where there are no blobs found so concat will raise an error

    except Exception as e:
        print(f"Error: {e}")
