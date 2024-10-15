def add_bottler_column(df, container_name):
    bottlers = {
        'ccba-kenya': 'CCBAKE',
        'ccba-botsw': 'CCBABW',
        'ccba-ethio': 'CCBAET',
        'ccba-tanz': 'CCBATZ',
        'ccba-mozam': 'CCBAMOZ',
        'ccbauganda': 'CCBAUG',
        'ccbazambia': 'CCBAZAM',
        'ccba-ghana': 'CCBAGHA',
        'ccbanamibi': 'CCBANAM',
        'ccba-malaw': 'CCBAMWI',
        'cbl': 'CBL'
    }
    df['Bottler'] = bottlers[container_name]
    return df

