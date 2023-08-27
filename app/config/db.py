from sqlalchemy import create_engine, MetaData
from app.config.credentials import passDb,userDb

#Production
engine = create_engine(f'postgresql+psycopg2://{userDb}:{passDb}@tuffi.db.elephantsql.com/zwmcuswf')



meta = MetaData()

conn = engine.connect()


