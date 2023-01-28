import database.make_connection as make_connection
import database.run_query as run_query
import datetime
from API.make_request import NGESO_Request
import API.Constants as Constants
from API.preprocessing import preprocess_json
import argparse
import json

### Entry point for the code ###
parser = argparse.ArgumentParser()

parser.add_argument('--auction_date', help='get data for a specific date. Takes input in format %Y-%m-%d', type = str)
parser.add_argument('--operation', help='for testing purposes. Takes input INSERT UPDATE DELETE SELECT', choices = ['INSERT', 'UPDATE', 'DELETE', 'SELECT'], default='INSERT')
parser.add_argument('--output_data', help='output pulled data to json for audit purposes')
parser.add_argument('--id', help='for delete and update functions please specify record id', type = str)
args = parser.parse_args()

if args.auction_date:
    auction_date = str(args.auction_date)  #allows for backfilling
else: 
    auction_date = datetime.datetime.today().strftime('%Y-%m-%d')

### Make connection to db ###
connection = make_connection.MakeConnection()
session = connection.create_session()
run_query = run_query.DCRunQuery()

if args.id: ### LOGIC NEEDS REFINING - LOOKS MESSY ###
    
    id_delete = args.id
    id_update = args.id

if args.operation == 'INSERT': #Do datapulls and insert data into db

    response_data = NGESO_Request(Constants.NGESO_DC_ResourceID, auction_date)
    unit_data_to_insert, auction_data_to_insert = preprocess_json(response_data=response_data)

    if args.output_data:

        with open("auction_data.json", "w") as outfile:
            json.dump(auction_data_to_insert, outfile)
        with open("unit_data.json", "w") as outfile:
            json.dump(unit_data_to_insert, outfile)
    
    run_query.insert_dc_data(auction_data=auction_data_to_insert, unit_data=unit_data_to_insert, session=session)


elif args.output_data:

    print("Outputting data only works with insert function! Operation will continue as specified")

elif args.operation == 'SELECT': #Select all data in db and print their ids

    data = run_query.select_all_auction_data(session=session)


elif args.operation == 'DELETE': #delete one record by id
    if args.id: 

        run_query.delete_auction_data_by_id(args.id, session)

    else:
        print('ID not specified. Unsuccessful.')
        
elif args.operation == 'UPDATE': #flag a record as cancelled
    if args.id: 

        run_query.update_cancellation_dc_data(args.id, session)
    
    else:

        print('ID not specified. Unsuccessful.')


