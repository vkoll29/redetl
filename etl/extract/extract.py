from typing import Tuple
from datetime import datetime, timedelta
import pandas as pd
from azure.storage.blob import BlobServiceClient
import pytz

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
            - length - specify whether you want to extract all data or just a subset of it. Currently, it is imperative to
            extract a subset because it is only used to generate the data schema.
        :return: a pandas dataframe of the extracted blob
    """

    start_date: datetime.date = (datetime.today() - timedelta(days=etl_days)).date()
    end_date: datetime.date = (datetime.today() - timedelta(days=stop_days)).date()

    container, sas = creds
    blobs = []
    try:
        # create blob service client for interacting with blob storage
        blob_service_client = BlobServiceClient(account_url=URI, credential=sas)
        # create a container instance
        container_client = blob_service_client.get_container_client(container)
        ir_blobs = container_client.list_blobs(name_starts_with=f"{ir_type}")

        # this extracts blobs based on last modified date i.e. within the start and end dates exclusive of end date
        for blob in ir_blobs:

            # print(blob)
            if start_date <= blob.last_modified.date() < end_date:
                blobs.append(blob_service_client.get_blob_client(container=container, blob=blob))

        for blob in blobs:
            print(blob.get_blob_properties()['name'], blob.get_blob_properties()['container'])

    except Exception as e:
        print(f"Error: {e}")
