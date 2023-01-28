import database.make_connection as make_connection 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
import datetime


connector = make_connection.MakeConnection()
#Start Engine
engine = connector.connect()
#Use Base Class
Base = declarative_base()
# Auction Results Table
class NGESO_DC(Base): 
    __tablename__ = 'NGESO_DC'
    ### TO DO ###
    # review column types if time allows #
    id = Column(String, primary_key = True, autoincrement = False)
    Company = Column(String)
    unit_name = Column(String, ForeignKey('Unit_Information_DC.unit_name'))
    EFA_date = Column(String)
    delivery_start = Column(String)
    delivery_end = Column(String)
    EFA = Column(Integer)
    service = Column(String)
    cleared_volume = Column(Integer)
    clearing_price = Column(Integer)
    Cancelled = Column(String, nullable = True) #Could make this Boolean but in response this is named as String
    Timestamp = Column('timestamp', TIMESTAMP(timezone=False), nullable = False, default = datetime.datetime.now()) #in a non-local version would use database server's timestamp 
    Last_Updated = Column('Last_updated', TIMESTAMP(timezone=False), nullable = False, default = datetime.datetime.now())

    unit_information_table = relationship('Unit_Information_DC')
# Unit Information Table
class Unit_Information_DC(Base): 

    __tablename__ = 'Unit_Information_DC'

    unit_name = Column(String, primary_key = True)
    technology_type = Column(String)
    Location = Column(String)

    ngeso_dc_table = relationship('NGESO_DC', back_populates="unit_information_table")


if __name__ == '__main__':

     Base.metadata.create_all(engine)

    
