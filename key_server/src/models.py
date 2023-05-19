from sqlalchemy.orm import declarative_base
import sqlalchemy


Base = declarative_base()


class KeyPairModel(Base):
    __tablename__ = "private_key"

    uuid = sqlalchemy.Column(sqlalchemy.String, primary_key=True, index=True)
    private_key = sqlalchemy.Column(sqlalchemy.LargeBinary)
    public_key = sqlalchemy.Column(sqlalchemy.LargeBinary)
    # aes_key = sqlalchemy.Column(sqlalchemy.LargeBinary)

    def __repr__(self):
        return f"PrivateKey(uuid={self.uuid}, private_key={self.private_key}, public_key={self.public_key})"
