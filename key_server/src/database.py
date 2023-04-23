from sqlalchemy.orm import sessionmaker
from .models import PrivateKey, Base
import sqlalchemy
import logging
from .schemas import PrivateKeyBase
import traceback
logger = logging.getLogger("key_server")


class CustomSession:
    def __init__(self, session):
        self.session = session

    def add_record(self, record: PrivateKey):
        try:
            self.session.add(record)
            self.session.commit()
            logger.info(f"Record added {record}")
        except Exception as e:
            logger.error(traceback.format_exc())
            self.session.rollback()
            raise e

    # def add_record(self, record: PrivateKeyBase):
    #     """
    #     TODO: Generalise this function to add any record to the database
    #     Add a record to the database"""
    #     model = PrivateKey(
    #         uuid=record.uuid,
    #         private_key=record.private_key,
    #         public_key=record.public_key)
    #     self._add_record(model)

    def get_key(self, uuid):
        key = self.session.query(PrivateKey).filter(
            PrivateKey.uuid == uuid).first()
        return key

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class Database:
    def __init__(self, db_url=None) -> None:
        self.db_url = db_url
        engine = sqlalchemy.create_engine(self.db_url)
        SessionLocal = sessionmaker(bind=engine)
        self.session = SessionLocal()
        Base.metadata.create_all(engine)

    def __call__(self) -> CustomSession:
        session = self.session
        yield CustomSession(session)
