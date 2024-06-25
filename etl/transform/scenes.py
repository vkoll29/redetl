from etl.transform._add_bottler_column import add_bottler_column
from src.utils.load_to_db import load_data
from src.utils.convert_dtypes import get_sql_dtype


def scenes_insert_staging(conn, df, container_name):
    # step 1: Drop unnecessary columns
    columns_to_drop = [
        'StitchedImageURL',
        'RawImagePath',
        'RawImageNames',
        'ImageQuality',
        'ReExportStatus',
        'ReExportTime',
        'ParentSceneUid',
        'ImageCount',
        'AssetSerialNumber',
        'AssetEquipmentNumber',
        'SceneCollectionMode',
        'IsFacingAvailable',
        'IsSelfValidated',
        'IsClientValidated',
        'IrImageUsable'
    ]
    df = df.drop(columns_to_drop, axis=1)

    # step 2: Add Bottler column
    df = add_bottler_column(df, container_name)

    # step 3: reorder columns
    new_order = [
        'SessionUID',
        'SceneUID',
        'SceneDateTime',
        'VerifiedOn',
        'Source',
        'SceneType',
        'SubSceneType',
        'CreatedOnTime',
        'LastModifiedTime',
        'FileCreatedTime',
        'SliceStartTime',
        'SliceEndTime',
        'Bottler',
        'ReProcessedTime',
        'ReProcessedStatus',
    ]
    df_tf = df.loc[:, new_order]


    # step 4: Convert dtypes to SQL types
    df_tf = get_sql_dtype(df_tf)
    # print(df_tf.dtypes)
    print(df_tf.dtypes)
    # step 4: Insert data to staging table
    load_data(df_tf, conn, 'stg.stageIRScenes')
