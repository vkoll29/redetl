from etl.transform._add_bottler_column import add_bottler_column
from src.utils.load_to_db import load_data
from src.utils.convert_dtypes import get_sql_dtype


def transform_actuals(conn, df, container_name):
    # step 1: Drop unnecessary columns
    columns_to_drop = [
        'BlockID',
        'IsEmpty',
        'ReExportStatus',
        'ReExportTime',
        'IRGuessedCategory',
        'IRActualID',
        'ProductWidth',
        'ProductHeight',
        'ShelfWidth',
        'ShelfHeight',
        'BlockWidth',
        'BlockHeight'
    ]
    df = df.drop(columns_to_drop, axis=1)

    # step 2: Rename  columns
    # a) orientationId column to Orientation
    df = df.rename(columns={'OrientationId': 'Orientation'})
    # b) ProductLocalSubCategoryName to LocalProductSubCategoryName
    df = df.rename(columns={'ProductLocalSubCategoryName': 'LocalProductSubCategoryName'})
    # c) 'ProductID' to ProductId
    df = df.rename(columns={'ProductID': 'ProductId'})
    # d) 'GlobalId' to GlobalID
    df = df.rename(columns={'GlobalId': 'GlobalID'})
    # e) 'SessionUID' to SessionUid
    df = df.rename(columns={'SessionUID': 'SessionUid'})
    # f) 'SceneUID' to SceneUid
    df = df.rename(columns={'SceneUID': 'SceneUid'})

    # step 2: Add Bottler column
    df = add_bottler_column(df, container_name)

    # step 3: reorder columns
    new_order = [
        'DoorIndex',
        'Orientation',
        'ProductId',
        'ProductName',
        'ShortName',
        'SKU',
        'UPC',
        'BAN',
        'Type',
        'BrandName',
        'ProductCategory',
        'BeverageType',
        'SingleFacings',
        'LocalProductCategoryName',
        'LocalProductSubCategoryName',
        'SellingPackSize',
        'IsForeign',
        'GlobalID',
        'PIMId',
        'REId',
        'FileCreatedTime',
        'SliceStartTime',
        'SliceEndTime',
        'Bottler',
        'SessionUid',
        'SceneUid',
        'Shelf',
        'Position',
        'StockPos',
        'ReProcessedStatus',
        'ReProcessedTime'
    ]
    df_tf = df.loc[:, new_order]
    df_tf = get_sql_dtype(df_tf)

    # step 4: Insert data to staging table
    print(df_tf.columns)
    load_data(df_tf, conn, 'stg.stageIRActualsFacings')
