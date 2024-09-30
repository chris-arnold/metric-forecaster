from sqlmodel import Session, SQLModel, create_engine
from .config import settings


dsn = settings.dsn
engine = create_engine(dsn)


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly

def init_db(session: Session) -> None:
    # This works because the models are already imported and registered from app.models
    SQLModel.metadata.create_all(engine)
