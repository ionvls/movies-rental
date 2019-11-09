import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv, find_dotenv

from commands import SeedCommand
from src.app import create_app, db

load_dotenv(find_dotenv('.env'))

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

migrate = Migrate(app=app, db=db)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)
manager.add_command('seed_db', SeedCommand)

if __name__ == '__main__':
    manager.run()
