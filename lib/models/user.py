from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base  # This line was missing

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    animes = relationship("Anime", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"
