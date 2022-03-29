from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///face.sqlite3'
app.config['SECRET_KEY'] = 'E315277807427FFC1CAF0B1040CEC8E84BE32F482377A42290AA301CCD896726'
db = SQLAlchemy(app)

from auth import auth as auth_blueprint
from main import main as main_blueprint
from image_processing import image_processing as image_processing_blueprint
from orm import User, UserImage

from images import images as images_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(images_blueprint)
app.register_blueprint(image_processing_blueprint)

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)
db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(allow_extra_args=True)#:~:text=from%20flask%20import,run(allow_extra_args%3DTrue)
