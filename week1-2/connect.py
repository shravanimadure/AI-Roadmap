from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String,Float,DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import pandas as pd
engine = create_engine("sqlite:///example.db",echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,default=lambda:str(uuid.uuid4()))
    upload_date = Column(DateTime)
    media_type = Column(String)
    likes = Column(Integer)
    shares = Column(Integer)
    saves	 = Column(Integer)
    engagement_rate=Column(Float)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv("processed_user.csv")

df["upload_date"] = pd.to_datetime(df["upload_date"])

users = [
    User(
        upload_date=row["upload_date"],
        media_type = row["media_type"],
        likes = row["likes"],
        shares = row["shares"],
        saves = row["saves"],
        engagement_rate = row["engagement_rate"]

    )
    for _, row in df.iterrows()
]

session.add_all(users)
session.commit()

