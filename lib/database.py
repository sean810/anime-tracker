from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import click

# Database URL (this can be changed if you prefer another database)
DATABASE_URL = "sqlite:///./anime_tracker.db"  # Using SQLite for simplicity

# Create an engine that can communicate with the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Declare the base for the model classes
Base = declarative_base()

# Create a SessionLocal class to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create the database tables
def create_db():
    Base.metadata.create_all(bind=engine)
    click.echo("Database tables created successfully.")
