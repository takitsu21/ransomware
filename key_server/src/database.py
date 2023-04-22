from sqlalchemy.orm import sessionmaker
from .models import PrivateKey, Base
import sqlalchemy


class Database:
    def __init__(self, db_url=None) -> None:
        self.db_url = db_url
        engine = sqlalchemy.create_engine(self.db_url)
        SessionLocal = sessionmaker(bind=engine)
        self.session = SessionLocal()
        Base.metadata.create_all(engine)

    def add_record(self, record):
        with self.session as session:
            session.add(record)
            session.commit()
            session.close()

    def get_key(self, uuid):
        with self.session as session:
            key = session.query(PrivateKey).filter(
                PrivateKey.uuid == uuid).first()
            session.close()
            return key
