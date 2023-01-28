import pandas as pd
import numpy as np

def preprocess_json(response_data):

    df = pd.DataFrame(response_data)
    df.to_csv('audit.csv')

#    try:
#        validate_df(df=df)
##        df = df[df['Company'] == 'HABITAT ENERGY LIMITED'] #only interested in Habitat Energy results
#    except: #if there are none then check outputs
#        df.to_csv('output.csv')
#        raise
    
    df = df[['_id', 'Company', 'Unit Name', 'EFA Date', 'Delivery Start', 'Delivery End', 'EFA', 'Service', 'Cleared Volume', 'Clearing Price', 'Technology Type', 'Location', 'Cancelled']]
    df.columns = ['id', 'Company', 'unit_name', 'EFA_date', 'delivery_start', 'delivery_end', 'EFA', 'service', 'cleared_volume', 'clearing_price', 'technology_type', 'Location', 'Cancelled']
    df = df.drop(columns=['id'])

    df['Cancelled'] = df['Cancelled'].map({"" : np.nan}) #would rather a nan than blank space
    df_unit_information = df[['unit_name', 'technology_type', 'Location']]
    df_auction_information = df[['Company', 'unit_name', 'EFA_date', 'delivery_start', 'delivery_end', 'EFA', 'service', 'cleared_volume', 'clearing_price', 'Cancelled']]

    df_unit_information.drop_duplicates(keep = 'last')

    df_auction_information['id'] = create_new_id(df)

    #df.to_json('clean_data.json', orient='records') #for audit purposes
    return df_unit_information.to_dict(orient = 'records'), df_auction_information.to_dict(orient='records')

def validate_df(df): 
    ### TO DO ###
    ### Flesh out validation procedures before writing to db - look at null values, regex patterns and basic dataset statistics (to ensure that data is sensible) ###
    if df.shape[0] == 0:
        
        print('DC Results DataFrame is empty')

    else:
        habitat_count = df[df['Company'] == 'HABITAT ENERGY LIMITED']
        print('\n There are ' + str(df.shape[0]) + ' total results with ' + str(habitat_count) + ' belonging to Habitat Energy \n')

def create_new_id(df): 
    
    ### Create a unique ID for each entry to prevent duplicates ###
    df_new_id = df.copy()

    df_new_id['delivery_start'] = pd.to_datetime(df_new_id['delivery_start']).dt.strftime('%Y%m%d%H%M%S')
    df_new_id['clearing_price'] = df_new_id['clearing_price'].astype(int)
    df_new_id['unit_name'] = df['unit_name'].replace('-', '', regex=True)
    df_new_id['ngeso_id'] = df_new_id['unit_name'] + df_new_id['delivery_start'] + (df_new_id['cleared_volume'].astype(str))

    return df_new_id['ngeso_id']


