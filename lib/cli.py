import click
import sys
import os

# Add the project root directory to sys.path so the 'lib' package can be found
if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from lib.database import SessionLocal, create_db
from lib.models.anime import Anime
from lib.models.tag import Tag
from lib.models.user import User

# Ensure the database is created (create tables)
create_db()

# Utility function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@click.group()
def cli():
    """Anime Watchlist Tracker CLI."""
    pass

# Command to create the database tables
@cli.command()
def create_db_command():
    """Creates the database tables."""
    create_db()
    click.echo("Database tables created successfully.")

# Command to add a new user
@cli.command()
@click.argument("name")
def add_user(name):
    """Add a new user to the database."""
    db = next(get_db())
    new_user = User(name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    click.echo(f"User '{new_user.name}' added successfully.")

# Command to add a new anime
@cli.command()
@click.argument("title")
@click.argument("genre")
@click.argument("total_episodes", type=int)
@click.option("--user_id", default=1, help="User ID to associate with this anime")
def add_anime(title, genre, total_episodes, user_id):
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        click.echo(f"User with ID {user_id} not found.")
        return

    new_anime = Anime(title=title, genre=genre, total_episodes=total_episodes, user_id=user_id)
    db.add(new_anime)
    db.commit()
    db.refresh(new_anime)
    click.echo(f"Anime '{new_anime.title}' added successfully.")

# Command to add a tag to an anime
@cli.command()
@click.argument("anime_id", type=int)
@click.argument("tag_name")
def add_tag(anime_id, tag_name):
    db = next(get_db())
    anime = db.query(Anime).filter(Anime.id == anime_id).first()
    if not anime:
        click.echo(f"Anime with ID {anime_id} not found.")
        return

    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        # Create the tag if it doesn't exist
        tag = Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        click.echo(f"Tag '{tag.name}' created and added to anime '{anime.title}'.")
    else:
        # Check if the tag is already associated with the anime
        if tag not in anime.tags:
            anime.tags.append(tag)
            db.commit()
            click.echo(f"Tag '{tag.name}' added to anime '{anime.title}'.")
        else:
            click.echo(f"Tag '{tag.name}' is already associated with anime '{anime.title}'.")

# Command to list all animes
@cli.command()
def list_animes():
    db = next(get_db())
    animes = db.query(Anime).all()
    if not animes:
        click.echo("No animes found.")
        return
    for anime in animes:
        click.echo(f"{anime.id}: {anime.title} - {anime.genre} ({anime.total_episodes} episodes)")

# Command to delete a user
@cli.command()
@click.argument("user_id", type=int)
def delete_user(user_id):
    """Delete a user by their ID."""
    db = next(get_db())
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        click.echo(f"User with ID {user_id} not found.")
        return

    # Delete the user and their associated animes
    db.delete(user)
    db.commit()
    click.echo(f"User with ID {user_id} and their associated anime have been deleted successfully.")

# Command to delete a tag
@cli.command()
@click.argument("tag_id", type=int)
def delete_tag(tag_id):
    """Delete a tag by its ID."""
    db = next(get_db())
    
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        click.echo(f"Tag with ID {tag_id} not found.")
        return

    # Delete the tag
    db.delete(tag)
    db.commit()
    click.echo(f"Tag with ID {tag_id} has been deleted successfully.")

# Command to delete an anime
@cli.command()
@click.argument("anime_id", type=int)
def delete_anime(anime_id):
    """Delete an anime by its ID."""
    db = next(get_db())
    
    anime = db.query(Anime).filter(Anime.id == anime_id).first()
    if not anime:
        click.echo(f"Anime with ID {anime_id} not found.")
        return

    # Delete the anime
    db.delete(anime)
    db.commit()
    click.echo(f"Anime with ID {anime_id} has been deleted successfully.")

# Command to exit the loop
@cli.command()
def exit():
    """Exit the CLI loop."""
    click.echo("Exiting CLI...")
    sys.exit()

# The interactive loop to simulate "staying" in the CLI until 'exit' command is given
from click.testing import CliRunner

def interactive_loop():
    runner = CliRunner()  # Using CliRunner to simulate command execution

    # List all available commands
    click.echo("Available commands:")
    for command in cli.commands:
        click.echo(f"- {command}")

    while True:
        try:
            command = input("Enter command (type 'exit' to quit): ").strip()
            if command == 'exit':
                break

            # Run the command using the CliRunner
            result = runner.invoke(cli, command.split())  # Pass the split command list to CliRunner

            # Print the result
            if result.exit_code == 0:
                click.echo(result.output)
            else:
                click.echo(f"Error: {result.output}")

        except KeyboardInterrupt:
            print("\nExiting CLI...")
            break

if __name__ == "__main__":
    interactive_loop()
