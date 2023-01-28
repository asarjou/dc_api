from db import NGESO_DC, Unit_Information_DC
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import update, delete
import datetime


class NGESO_DCQuery:
# Class holds general queries which can be put together and run #
    def insert_data(self, table_name, index_element, data, session):
        
        try: 
            stmt = insert(table_name).values(data) #uses a function which doesn't allow insert of duplicates based on index
            stmt = stmt.on_conflict_do_nothing(
                index_elements = [index_element]
            )
            session.execute(stmt)
        except:
            session.rollback()
            raise


    def update_cancelled_data(self, table_name, index_element, id, session): #updates whether plant cancelled or not (shows functionality)

        try:
            session.execute(
                update(table_name)
                .where(index_element == id)
                .values({'Cancelled': 1, 'Last_Updated': datetime.datetime.now()})
            )
        except:
            session.rollback()
            raise

    def select_all_data(self, table_name, session): #queries entire table

        data = session.query(table_name).all()

        return data
    
    def delete_record_by_id(self, table_name, index_element, id, session): #deletes a record by id

        try: 
            session.execute(
                delete(table_name)
                .where(index_element == id)
            )
        except: 
            session.rollback()
        