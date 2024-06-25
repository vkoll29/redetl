from etl.transform._add_bottler_column import add_bottler_column
from src.utils.load_to_db import load_data
from src.utils.convert_dtypes import get_sql_dtype


def transform_inventory(conn, df, container_name):
    # step 1: Drop unnecessary columns
    columns_to_drop = [
        'ID',
        'ReExportStatus',
        'ReExportTime'
    ]
    df = df.drop(columns_to_drop, axis=1)

    # step 2: Rename  columns
    # a) ProductLocalSubCategoryName to LocalProductSubCategoryName
    df = df.rename(columns={'ProductLocalSubCategoryName': 'LocalProductSubCategoryName'})

    # step 2: Add Bottler column
    df = add_bottler_column(df, container_name)

    # step 3: reorder columns
    new_order = [
        'SessionUID',
        'SceneUID',
        'InventoryUnit',
        'Price',
        'ProductID',
        'ProductName',
        'ShortName',
        'SKU',
        'UPC',
        'BAN',
        'Type',
        'BrandName',
        'ProductCategory',
        'BeverageType',
        'Bottler',
        'LocalProductCategoryName',
        'LocalProductSubCategoryName',
        'SellingPackSize',
        'IsForeign',
        'GlobalId',
        'PIMId',
        'REId',
        'FileCreatedTime',
        'SliceStartTime',
        'SliceEndTime',
        'ReProcessedTime',
        'ReProcessedStatus'
    ]
    df_tf = df.loc[:, new_order]
    df_tf = get_sql_dtype(df_tf)

    # step 4: Insert data to staging table
    print(df_tf.columns)
    load_data(df_tf, conn, 'stg.stageIRInventoryPricing')
