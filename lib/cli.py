import click
from sqlalchemy.orm import Session
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
    """Anime Watchlist Tracker CLI"""
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
        tag = Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)

    anime.tags.append(tag)
    db.commit()
    click.echo(f"Tag '{tag.name}' added to anime '{anime.title}'.")

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

if __name__ == "__main__":
    cli()
