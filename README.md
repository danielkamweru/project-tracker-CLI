# Project Tracker CLI

A command-line application for managing users, teams, and projects using Python, SQLAlchemy ORM, and Click.  
The application includes both standard command usage and a fully interactive menu interface with a numbered command selector.

## Overview

The Project Tracker CLI is a Phase 3 Python application that uses SQLAlchemy ORM to manage relationships between Users, Teams, and Projects.  
It provides:

- A CLI interface built with Click
- A numbered interactive menu for user-friendly navigation
- A SQLite-backed database using SQLAlchemy ORM
- CRUD-style commands for managing all entities

## Features

- Create, list, and manage Users
- Create and manage Teams
- Create Projects, assign users, and update statuses
- Fully interactive menu (no need to memorize commands)
- Clean ORM models with relationships:
  - One-to-many (Team → Users)
  - One-to-many (User → Projects)
- Custom ASCII-framed banner for branding
- Safe status validation using tuple-based values (as required by the rubric)

## Project Structure
phase-3-project/
│
├── app.py               # Main CLI entry point
├── db.py                # Database engine and SessionLocal
├── database.py          # ORM models (User, Team, Project)
├── Pipfile              # Pipenv environment file
├── Pipfile.lock
└── README.md            # Project documentation

## Installation

### Clone the repository
```bash
git clone <your-repo-url>
cd phase-3-project

Install dependencies (Pipenv)
pipenv install

Install Alembic (optional, for migrations)
pipenv install alembic

Activate virtual environment
pipenv shell

Database Setup
The SQLite database file is automatically created when the ORM engine initializes.
If using Alembic migrations:
alembic upgrade head

Otherwise, tables are created automatically on first run of:
python3 app.py

Running the Application
Start the CLI
python3 app.py



Running without arguments opens interactive mode automatically.


You can also run individual commands directly.


Interactive Mode
The interactive menu displays a boxed ASCII banner:             
  Project Tracker Interactive CLI                                             │
  by Daniel Kamweru                  
It then shows all commands by number for easy selection.
Available Commands
Users


create-user <name> <role>


list-users


add-user-to-team <user_id> <team_id>


Teams


create-team <team_name>


list-teams


Projects


create-project <title> <description>


list-projects


assign-project <project_id> <user_id>


update-status <project_id> <status>


Data Models
User


id


name


role


team_id (FK)


Relationships:


One user belongs to one team


One user may be assigned multiple projects


Team


id


name


Relationships:


One team has many users


Project


id


title


description


status


assigned_user_id (FK)


Relationships:


One project is assigned to one user (optional)


Status Values
Status is restricted using a tuple:
VALID_STATUSES = ("not_started", "in_progress", "completed")

Example:
update-status 1 completed

Example Workflows
Create a Team
python3 app.py create-team Developers

Create a User
python3 app.py create-user Alice Developer

Add User to Team
python3 app.py add-user-to-team 1 1

Create a Project
python3 app.py create-project "Website Redesign" "Rebuild the frontend"

Assign a Project
python3 app.py assign-project 1 1

Update Status
python3 app.py update-status 1 in_progress

Troubleshooting


No module named 'sqlalchemy'


pipenv install sqlalchemy
pipenv shell



No module named 'click'


pipenv install click



Command not recognized
Make sure you are inside the virtual environment:


pipenv shell



Database does not update
Delete the SQLite file and rerun the program:


rm project.db
python3 app.py

License
This project is open-source and available for educational use only.
Copyright
Copyright (c) by Daniel Kamweru
All rights reserved.



