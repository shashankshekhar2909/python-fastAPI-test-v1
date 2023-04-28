from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

Base.metadata.create_all(bind=engine)

# Create a Faker instance to generate fake data
faker = Faker()

# Create a session to interact with the database
db = SessionLocal()

# Add 100 sample users to the database
for _ in range(100):
    user = User(
        name=faker.name(),
        email=faker.email(),
        password=faker.password(length=12)
    )
    db.add(user)
    db.commit()

# Close the database session
db.close()
