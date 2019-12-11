import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from models import *

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

# def make_shell_context():
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    #交互环境用
    manager.run()

