# Anime Tracker CLI Application
By Sean Daniel Munene
## Description
The **Anime Tracker CLI Application** is a command-line interface tool that allows users to manage their anime watchlist. Built with Python and SQLAlchemy, the app lets users add, list, and organize anime, associate them with tags, and manage users, making it a perfect solution for anime enthusiasts who want to track their watching habits.

## Features
- **User Management**:
  - Add and manage users.
- **Anime Management**:
  - Add anime with details like title, genre, total episodes, and associated users.
  - List all anime in the database.
- **Tag Management**:
  - Add tags to anime for better categorization.
- **Database Management**:
  - Automatically creates SQLite database tables.
  
## Requirements
To run the Anime Tracker app, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package installer)
- The following Python libraries:
  - `Click`
  - `SQLAlchemy`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sean810/anime-tracker
   cd anime-tracker
   ```

2. Create and activate a virtual environment.


3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python -m lib.cli create_db_command
   ```

## Usage
To interact with the Anime Tracker app, use the CLI commands which will be provided
to you once you do:
```bash
python -m lib.cli or python lib/cli.py
```

### Add a User
Add a new user to the database.
```bash
Example: add-user "username"
```
Example:
```bash
Example: add-user "Sean"
```

### Add an Anime
Add a new anime to the database, associating it with a specific user.
```bash
python -m lib.cli add-anime "title" "genre" total_episodes --user_id USER_ID
```
Example:
```bash
Example: add-anime "Naruto" "Action" 500 --user_id 1
```

### Add a Tag
Add a tag to an anime.
```bash
Example: add-tag ANIME_ID "tag_name"
```
Example:
```bash
Example: add-tag 1 "Action"
```

### List All Animes
View a list of all anime in the database.
```bash
Example: list-animes
```
Example output:
```
1: Naruto - Action (500 episodes)
2: One Piece - Adventure (1000 episodes)
```

## Delete Anime
One can delete a specific anime from the database by using it's ID
```bash
Example: delete-anime 1
```

## Delete user
One can delete a specific user from the database by using it's ID
```bash
Example: delete-user 1
```

## Delete tag
One can delete a tag from the database by using it's ID
```bash
Example: delete-tag 1
```
## Assistance
If you need any assistance while in the command line, type in;
```bash
--help
```

If you want to exit the loop type in;
```bash
exit
```

## Project Structure
```
anime-tracker/
|— lib/
   |— __init__.py
   |— cli.py              # CLI commands for interacting with the app
   |— database.py         # Database setup
   |— models/            
       |— __init__.py
       |— anime.py        # Anime model
       |— tag.py          # Tag model
       |— user.py         # User model
|— requirements.txt       # Python dependencies
|— .gitignore             
|— README.md              # Project documentation (this file)
```

## How It Works
1. **Database**:
   - The app uses SQLite as its database.
   - Models (User, Anime, and Tag) are defined using SQLAlchemy's ORM.
   - A one-to-many relationship is established between Users and Anime.
   - A many-to-many relationship is established between Anime and Tags.

2. **CLI Commands**:
   - Built using the `Click` library.
   - Each command interacts with the database via SQLAlchemy sessions.

3. **User Workflow**:
   - Users should be added first.
   - Anime are added and associated with a user.
   - Tags can be applied to anime for categorization.

## Future Improvements
- Implement search functionality to find anime by title or tags.
- Add functionality to update anime details (e.g., completed episodes).
- Add a feature to delete anime, users, or tags.
- Enhance error handling and validation.

## License
This project is licensed under the MIT License.

## Technologies Used
The Anime Tracker CLI Application utilizes the following technologies:

Python: The primary programming language for building the application.
Click: A Python library for creating a user-friendly command-line interface.
SQLAlchemy: An Object-Relational Mapping (ORM) library for database interaction.
SQLite: A lightweight, file-based relational database for data storage.
Virtual Environment: Ensures isolated dependency management for the project.

## Acknowledgments
Special thanks to [Madam Beatrice Wambui] for guidance and support.

