import os

import unittest

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


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('src/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
