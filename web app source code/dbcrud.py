import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from dbconfig import *
from dbmodels import *

engine = db.create_engine(ENGINE_URI, pool_size=25, max_overflow=25)
Session = sessionmaker(bind=engine)

def recreate_database(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':

    conn = engine.connect()
    s = Session()
    s.close_all()
    recreate_database(engine)
