import io
from typing import Tuple
from datetime import datetime, timedelta
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
import time

from src.utils.get_config import __load_config

config = __load_config('config/config.yml')
URI = config['account']['uri']


def extract_blobs_date(
        creds: Tuple[str, str],
        ir_type: str,
        etl_days: int = 2,
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
    print(start_date, end_date)

    container, sas = creds
    blobs = []
    blob_dfs = []  # will contain all the dfs generated from each parquet file
    start = time.time()
    try:
        # create blob service client for interacting with blob storage
        # blob_service_client = BlobServiceClient(account_url=URI, credential=sas)
        service_client = DataLakeServiceClient(account_url=URI,credential=sas)
        filesystem_client = service_client.get_file_system_client(container)
        paths = filesystem_client.get_paths(path=f"V2/Data/{ir_type}/", recursive=True)
        for path in paths:
            if path.is_directory:
                continue

            last_modified = path.last_modified.date()
            if not start_date <= last_modified <= end_date:
                continue
            print(f"Reading: {path.name}")
            file_client = filesystem_client.get_file_client(path.name)
            download = file_client.download_file()

            if 'length' in kwargs:
                blob_content = download.read(kwargs['length'])
            else:
                blob_content = download.readall()

            print(f"Downloaded {len(blob_content)} bytes")

            if len(blob_content) == 0:
                print(f"WARNING: Skipping empty file: {path.name}")
                continue

            df = pd.read_parquet(io.BytesIO(blob_content))
            blob_dfs.append(df)

        print(f"Extracted {ir_type} data in {time.time() - start:.2f} seconds")
        return pd.concat(blob_dfs, axis=0,
                         ignore_index=True)  # TODO: Handle cases where there are no blobs found so concat will raise an error

    except Exception as e:
        print(f"Error: {e}")
