from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from DB_Web import app
from exts import db
from models import User, Board, Post, Comment, Favorite, ReportP, ReportC


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
