from fastapi import FastAPI, Depends, HTTPException
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from src.models import PrivateKey, Base
from src.database import Database
import subprocess
import sys
app = FastAPI(debug=True)

# Configure database connection
DB = Database(db_url="postgresql://postgres:postgres@localhost:5432/postgres")


def get_id():
    if sys.platform == 'win32':
        return subprocess.Popen('wmic csproduct get uuid', shell=True,
                                stdout=subprocess.PIPE).stdout.read().decode().split('\n')[1].strip()
    else:
        return subprocess.Popen('sudo cat /sys/class/dmi/id/product_uuid',
                                shell=True, stdout=subprocess.PIPE).stdout.read().decode().strip()


def get_db():
    db = DB.session()
    try:
        yield db
    finally:
        db.close()


@app.get("/private_key/{uuid}")
def get_private_key(uuid: str):
    key = DB.get_key(uuid)
    if key:
        return key.private_key
    else:
        raise HTTPException(status_code=404, detail="Key not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=12001)

    # db_url = "postgresql://postgres:postgres@localhost:5432/postgres"
    # engine = sqlalchemy.create_engine(db_url)
    # SessionLocal = sessionmaker(bind=engine)
    # Base.metadata.create_all(engine)
    # db.add_record(
    #     PrivateKey(
    #         uuid=get_id(),
    #         private_key=b"test",
    #         public_key=b"test"))
    # db.add_record(
    #     PrivateKey(
    #         uuid=get_id(),
    #         private_key=b"test2",
    #         public_key=b"test2"))
