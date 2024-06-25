import pandas as pd

from etl.transform._add_bottler_column import add_bottler_column
from src.utils.load_to_db import load_data
from src.utils.convert_dtypes import get_sql_dtype


def transform_products(conn, df, container_name):

    # step 1: Drop unnecessary columns
    columns_to_drop = [
        'IsEmpty',
        'REId',
        'ThumbnailUrl',
        'ProductMetaData',
        'Width',
        'Depth',
        'Height'
    ]
    df = df.drop(columns_to_drop, axis=1)

    # step 2: Add subclientcode column
    df['SubClientCode'] = ''  # TODO: add subclientcode or ensure true NULL is inserted and not blanks


    # step 2: Add Bottler column
    df = add_bottler_column(df, container_name)

    # step 3: reorder columns
    new_order = [
        'ProductId',
        'ClientCode',
        'SubClientCode',
        'CountryCode',
        'Ban',
        'SKU',
        'UPC',
        'ProductName',
        'ShortName',
        'Manufacturer',
        'BrandName',
        'PackagingType',
        'ProductCategory',
        'ProductCategoryCode',
        'BeverageType',
        'PackageType',
        'FlavourName',
        'LocalProductCategoryName',
        'ProductLocalSubCategoryName',
        'ProductLocalSubCategoryCode',
        'ProductGroup',
        'MeasurementUnit',
        'CCId',
        'PIMId',
        'SubBrandName',
        'Barcode',
        'ArticleCode',
        'SalesUnit',
        'ServingType',
        'SellingPackType',
        'SellingPackSize',
        'IsForeign',
        'Price',
        'CurrencyName',
        'IsUnknown',
        'IsTrained',
        'IsFlagged',
        'IsCompetitor',
        'RESkuCode',
        'CreatedByUserId',
        'CreatedOn',
        'ModifiedByUserId',
        'ModifiedOn',
        'IsActive',
        'Type',
        'SweetnerType',
        'NormalizePackagingSize',
        'SellingPackFrontFacings',
        'SellingPackSideFacings',
        'PackageSize',
        'SKULastSeen',
        'ProductDistributionIdentifier',
        'ProductUID',
        'LabelName',
        'ThirdPartyProduct',
        'Bottler'
    ]
    df = df.loc[:, new_order]

    # step 4: Convert dtypes to SQL types
    df_tf = get_sql_dtype(df)

    # step 4: Insert data to staging table
    load_data(df_tf, conn, 'stg.IRProduct')
