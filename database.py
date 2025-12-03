# database.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, engine

# -------------------------
# USER MODEL
# -------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # relationships
    projects = relationship("Project", back_populates="assigned_user")
    team_id = Column(Integer, ForeignKey("teams.id"))

    def __repr__(self):
        return f"<User {self.id}: {self.name} ({self.role})>"


# -------------------------
# TEAM MODEL (3rd table)
# -------------------------
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship("User", backref="team")

    def __repr__(self):
        return f"<Team {self.id}: {self.name}>"


# -------------------------
# PROJECT MODEL
# -------------------------
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="not_started")

    # FK → User
    user_id = Column(Integer, ForeignKey("users.id"))
    assigned_user = relationship("User", back_populates="projects")

    def __repr__(self):
        assigned = self.assigned_user.name if self.assigned_user else "Unassigned"
        return f"<Project {self.id}: {self.title} - {self.status} ({assigned})>"


# Create all tables
Base.metadata.create_all(engine)
