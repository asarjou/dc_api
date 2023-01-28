from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MakeConnection():

    def connect(self):

        engine = create_engine('sqlite:///dcdb/dc.db', echo=False) #type and name of created sqlite db

        return engine

    def create_session(self):  

        engine = self.connect()

        Session = sessionmaker()
        Session.configure(bind=engine)
        session=Session()

        return session