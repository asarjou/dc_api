from db import NGESO_DC, Unit_Information_DC
from database.query import NGESO_DCQuery

class DCRunQuery:
# This class runs specific queries that have been put together using the queries created in NGESO_DCQuery #
# idea is that when more complicated procedures are run can do so neatly and robustly #

    def select_all_auction_data(self, session): 

        query_data = NGESO_DCQuery()
        data = query_data.select_all_data(NGESO_DC, session=session)
        for row in data:
            print(row.id, row.Last_Updated, row.clearing_price)
        session.commit()
        session.close()

    def insert_dc_data(self, auction_data, unit_data, session):

        query_data = NGESO_DCQuery()
        query_data.insert_data(NGESO_DC, NGESO_DC.id, auction_data, session)
        query_data.insert_data(Unit_Information_DC, Unit_Information_DC.unit_name, unit_data, session)



        data = query_data.select_all_data(NGESO_DC, session=session) #just to check the database has been updated
        for row in data:
            print(row.id, row.Last_Updated, row.clearing_price)

        print('Successfully operation. Closing Session.')
        
        session.commit()
        session.close()

    def update_cancellation_dc_data(self, id, session):

        query_data = NGESO_DCQuery()
        query_data.update_cancelled_data(NGESO_DC, NGESO_DC.id, id, session)
        session.commit()
        session.close()

    def delete_auction_data_by_id(self, id, session):

        query_data = NGESO_DCQuery()
        query_data.delete_record_by_id(NGESO_DC, NGESO_DC.id, id, session)    
        session.commit()
        session.close()