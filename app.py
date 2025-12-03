# app.py
import click
from db import SessionLocal
from database import User, Team, Project
from sqlalchemy.orm import joinedload

# Utility: statuses stored in a tuple → required by rubric
VALID_STATUSES = ("not_started", "in_progress", "completed")
# CUSTOM: Numbered command list for Click CLI

class NumberedGroup(click.Group):
    def list_commands(self, ctx):
        # Return commands in definition order, not alphabetical
        return list(self.commands)

    def format_commands(self, ctx, formatter):
        commands = self.list_commands(ctx)
        if not commands:
            return

        with formatter.section('Commands'):
            rows = []
            for i, cmd_name in enumerate(commands, start=1):
                cmd = self.get_command(ctx, cmd_name)
                if cmd is None:
                    continue
                help_str = cmd.short_help or ''
                rows.append((f"{i}) {cmd_name}", help_str))
            formatter.write_dl(rows)

    # Allow lookup by number (for interactive mode)
    def get_command(self, ctx, cmd_name):
        if cmd_name.isdigit():
            commands = self.list_commands(ctx)
            index = int(cmd_name) - 1
            if 0 <= index < len(commands):
                cmd_name = commands[index]
        return super().get_command(ctx, cmd_name)
# MAIN CLI GROUP (NOW NUMBERED)
@click.group(cls=NumberedGroup, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Project Tracker CLI - Manage users, teams, and projects."""

    # If no command was passed → start interactive menu
    if ctx.invoked_subcommand is None:
        interactive_mode()
# INTERACTIVE MODE

def interactive_mode():
    """Interactive menu allowing number-based command selection."""
    click.echo(r"""
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗  │
│  ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝  │
│  ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║     │
│  ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║     │
│  ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║     │
│  ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝     │
│                                                         │
│  ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗    │
│  ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗   │
│     ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝   │
│     ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗   │
│     ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║   │
│     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   │
│                                                         │
│              Interactive CLI by Daniel Kamweru          │
│                                                         │
└─────────────────────────────────────────────────────────┘
""")

    while True:
        commands = cli.list_commands(click.Context(cli))

        click.echo("\nSelect an option:")
        for i, cmd in enumerate(commands, start=1):
            click.echo(f"{i}) {cmd}")

        choice = click.prompt("(\nEnter number (or q to quit)")

        if choice.lower() in ("q", "quit", "exit"):
            click.echo("Goodbye!")
            break

        if not choice.isdigit():
            click.echo("Please enter a number.")
            continue

        index = int(choice) - 1

        if index < 0 or index >= len(commands):
            click.echo("Invalid choice.")
            continue

        cmd_name = commands[index]

        # Load the selected command
        cmd = cli.get_command(click.Context(cli), cmd_name)

        # Collect arguments
        arg_values = []
        for param in cmd.params:
            if isinstance(param, click.Argument):
                value = click.prompt(f"Enter {param.name.upper()}")
                arg_values.append(value)

        # Run command WITHOUT exiting CLI
        try:
            cmd.main(args=arg_values, standalone_mode=False)
        except SystemExit:
            # Ignore click's exit signals to keep menu running
            pass

# ---------------------
# USER COMMANDS
# ---------------------
@cli.command()
@click.argument("name")
@click.argument("role")
def create_user(name, role):
    """Create a new user."""
    db = SessionLocal()
    user = User(name=name, role=role)
    db.add(user)
    db.commit()
    click.echo(f"User '{name}' created successfully!")
    db.close()

@cli.command()
def list_users():
    """List all users."""
    db = SessionLocal()
    users = db.query(User).options(joinedload(User.team)).all()
    db.close()

    if not users:
        click.echo("No users found.")
        return

    for u in users:
        team = u.team.name if u.team else "No Team"
        click.echo(f"[{u.id}] {u.name} - {u.role} | Team: {team}")

# ---------------------
# TEAM COMMANDS
# ---------------------
@cli.command()
@click.argument("team_name")
def create_team(team_name):
    """Create a team."""
    db = SessionLocal()
    team = Team(name=team_name)
    db.add(team)
    db.commit()
    click.echo(f"Team '{team_name}' created!")
    db.close()

@cli.command()
def list_teams():
    """List all teams."""
    db = SessionLocal()
    teams = db.query(Team).options(joinedload(Team.users)).all()
    db.close()

    if not teams:
        click.echo("No teams found.")
        return

    for t in teams:
        members = [u.name for u in t.users]
        click.echo(f"[{t.id}] {t.name} | Members: {members}")

@cli.command()
@click.argument("user_id")
@click.argument("team_id")
def add_user_to_team(user_id, team_id):
    """Assign a user to a team."""
    db = SessionLocal()
    user = db.query(User).filter_by(id=int(user_id)).first()
    team = db.query(Team).filter_by(id=int(team_id)).first()

    if not user or not team:
        click.echo("Invalid user or team ID.")
        return

    user.team = team
    db.commit()
    click.echo(f"User '{user.name}' added to team '{team.name}'!")
    db.close()

# ---------------------
# PROJECT COMMANDS
# ---------------------
@cli.command()
@click.argument("title")
@click.argument("description")
def create_project(title, description):
    """Create a new project."""
    db = SessionLocal()
    project = Project(title=title, description=description)
    db.add(project)
    db.commit()
    click.echo(f"Project '{title}' created.")
    db.close()

@cli.command()
def list_projects():
    """List all projects."""
    db = SessionLocal()
    projects = db.query(Project).options(joinedload(Project.assigned_user)).all()
    db.close()

    if not projects:
        click.echo("No projects found.")
        return

    for p in projects:
        user = p.assigned_user.name if p.assigned_user else "Unassigned"
        click.echo(f"[{p.id}] {p.title} | {p.status} | Assigned: {user}")

@cli.command()
@click.argument("project_id")
@click.argument("user_id")
def assign_project(project_id, user_id):
    """Assign a user to a project."""
    db = SessionLocal()
    project = db.query(Project).filter_by(id=int(project_id)).first()
    user = db.query(User).filter_by(id=int(user_id)).first()

    if not project or not user:
        click.echo("Invalid project or user ID.")
        return

    project.assigned_user = user
    db.commit()
    click.echo(f"Project '{project.title}' assigned to '{user.name}'.")
    db.close()

@cli.command()
@click.argument("project_id")
@click.argument("status")
def update_status(project_id, status):
    """Update project status."""
    if status not in VALID_STATUSES:
        click.echo(f"Invalid status. Choose from: {VALID_STATUSES}")
        return

    db = SessionLocal()
    project = db.query(Project).filter_by(id=int(project_id)).first()

    if not project:
        click.echo("Project not found.")
        return

    project.status = status
    db.commit()
    click.echo(f"Project '{project.title}' updated to {status}.")
    db.close()



if __name__ == "__main__":
    cli()  # This actually starts the CLI







       